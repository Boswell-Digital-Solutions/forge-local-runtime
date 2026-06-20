"""Service-matrix aggregation and pressure derivation for Forge Local Runtime.

This module implements the producer side of two control surfaces:

* ``build_service_matrix`` composes the per-service ``service-status`` envelopes
  for the four local services into one ``runtime-service-matrix`` snapshot. A
  service that does not report is represented explicitly as ``unavailable`` /
  ``not_ready`` (fail-closed), never dropped.
* ``derive_pressure`` maps a matrix snapshot to a bounded three-class
  ``runtime-pressure`` indicator (``low`` / ``elevated`` / ``critical``). It is a
  pure function of the matrix — the same snapshot always yields the same result.

No I/O, no app/workflow logic: this repo stays a producer that composes and
exposes truthful state.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

# Canonical service identity and class, in deterministic order. The matrix always
# represents exactly these four services.
CANONICAL_SERVICES: tuple[tuple[str, str], ...] = (
    ("df-local-foundation", "substrate"),
    ("neuronforge-local", "inference"),
    ("cortex", "file_intelligence"),
    ("fa-local", "execution"),
)

_SERVICE_CLASS = dict(CANONICAL_SERVICES)
_SERVICE_ORDER = {service_id: i for i, (service_id, _) in enumerate(CANONICAL_SERVICES)}

_PRESSURE_RANK = {"low": 0, "elevated": 1, "critical": 2}
_RANK_PRESSURE = {rank: name for name, rank in _PRESSURE_RANK.items()}

# States that, when observed, are at minimum elevated pressure.
_ELEVATED_STATES = (
    "degraded",
    "stale",
    "partial_success",
    "review_required",
    "waiting_explicit_approval",
)


def _readiness_class_for(status: Mapping[str, Any]) -> str:
    """Resolve a readiness class, preferring the explicit embedded summary."""
    embedded = status.get("readiness_summary")
    if isinstance(embedded, Mapping) and embedded.get("readiness_class"):
        return str(embedded["readiness_class"])
    # Fallback: derive a truthful readiness class from the reported state.
    state = status.get("state")
    if state == "ready":
        return "ready"
    if state in ("unavailable", "denied"):
        return "not_ready"
    if state == "degraded":
        return "degraded"
    return "ready_with_constraints"


def _summary_for(status: Mapping[str, Any]) -> str | None:
    embedded = status.get("readiness_summary")
    if isinstance(embedded, Mapping) and embedded.get("summary"):
        return str(embedded["summary"])[:300]
    message = status.get("operator_visible_message")
    if message:
        return str(message)[:300]
    return None


def _observed_entry(service_id: str, status: Mapping[str, Any]) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "service_id": service_id,
        "service_class": _SERVICE_CLASS[service_id],
        "state": status["state"],
        "readiness_class": _readiness_class_for(status),
        "observation": "observed",
        "last_updated_at": status["last_updated_at"],
    }
    if status.get("degraded_subtype") is not None:
        entry["degraded_subtype"] = status["degraded_subtype"]
    blocking = status.get("blocking_reasons")
    if blocking:
        entry["blocking_reasons"] = sorted(set(blocking))
    summary = _summary_for(status)
    if summary:
        entry["summary"] = summary
    return entry


def _missing_entry(service_id: str, generated_at: str) -> dict[str, Any]:
    """Fail-closed placeholder for a service that did not report."""
    return {
        "service_id": service_id,
        "service_class": _SERVICE_CLASS[service_id],
        "state": "unavailable",
        "readiness_class": "not_ready",
        "blocking_reasons": ["dependency_unavailable"],
        "observation": "missing",
        "summary": "No status reported; treated as unavailable (fail-closed).",
        "last_updated_at": generated_at,
    }


def build_service_matrix(
    statuses: Iterable[Mapping[str, Any]],
    *,
    generated_at: str,
    correlation_id: str | None = None,
    details_redacted: bool = True,
) -> dict[str, Any]:
    """Compose per-service status envelopes into a runtime-service-matrix snapshot.

    ``statuses`` is any collection of ``service-status``-shaped mappings. Each must
    carry at least ``service_id``, ``state`` and ``last_updated_at``. Services that
    are absent from ``statuses`` are filled with an explicit fail-closed
    ``unavailable`` entry. Unknown ``service_id`` values are rejected, and a service
    reporting twice is rejected — both are producer-truth violations.
    """
    by_id: dict[str, Mapping[str, Any]] = {}
    for status in statuses:
        service_id = status.get("service_id")
        if service_id not in _SERVICE_CLASS:
            raise ValueError(f"unknown service_id in status: {service_id!r}")
        if service_id in by_id:
            raise ValueError(f"duplicate status for service_id: {service_id!r}")
        by_id[service_id] = status

    services: list[dict[str, Any]] = []
    for service_id, _ in CANONICAL_SERVICES:
        status = by_id.get(service_id)
        if status is None:
            services.append(_missing_entry(service_id, generated_at))
        else:
            services.append(_observed_entry(service_id, status))

    matrix: dict[str, Any] = {
        "matrix_version": "v1",
        "generated_at": generated_at,
        "details_redacted": details_redacted,
        "services": services,
    }
    if correlation_id is not None:
        matrix["correlation_id"] = correlation_id
    return matrix


def _critical_signal(entry: Mapping[str, Any]) -> str | None:
    """Return the critical signal for an entry, or None if not critical."""
    state = entry.get("state")
    blocking = set(entry.get("blocking_reasons") or ())
    if state == "unavailable":
        return "unavailable"
    if state == "denied":
        return "denied"
    if entry.get("degraded_subtype") == "integrity_failed" or "integrity_failed" in blocking:
        return "integrity_failed"
    if "dependency_unavailable" in blocking:
        return "dependency_unavailable"
    if entry.get("readiness_class") == "not_ready":
        return "not_ready"
    return None


def _elevated_signal(entry: Mapping[str, Any]) -> str | None:
    """Return the elevated signal for an entry, or None if not elevated."""
    state = entry.get("state")
    if state in _ELEVATED_STATES:
        return state
    readiness = entry.get("readiness_class")
    if readiness == "ready_with_constraints":
        return "ready_with_constraints"
    if readiness == "degraded":
        return "degraded"
    return None


def derive_pressure(
    matrix: Mapping[str, Any],
    *,
    generated_at: str | None = None,
    correlation_id: str | None = None,
    details_redacted: bool = True,
) -> dict[str, Any]:
    """Derive a runtime-pressure indicator from a service-matrix snapshot.

    Deterministic rollup (pure function of ``matrix``):

    * An entry is **critical** if its state is ``unavailable``/``denied``, its
      readiness is ``not_ready``, or it carries an integrity/dependency block.
    * Otherwise an entry is **elevated** if its state is degraded/stale/partial/
      review/approval-waiting, or its readiness is reduced.
    * ``pressure_class`` is the maximum contribution across all entries; ``low``
      when nothing contributes.
    """
    contributions: list[dict[str, Any]] = []
    highest = 0

    entries = sorted(
        matrix.get("services", []),
        key=lambda e: _SERVICE_ORDER.get(e.get("service_id"), len(_SERVICE_ORDER)),
    )
    for entry in entries:
        critical = _critical_signal(entry)
        if critical is not None:
            highest = max(highest, _PRESSURE_RANK["critical"])
            contributions.append(
                {
                    "service_id": entry["service_id"],
                    "signal": critical,
                    "raised_to": "critical",
                }
            )
            continue
        elevated = _elevated_signal(entry)
        if elevated is not None:
            highest = max(highest, _PRESSURE_RANK["elevated"])
            contributions.append(
                {
                    "service_id": entry["service_id"],
                    "signal": elevated,
                    "raised_to": "elevated",
                }
            )

    pressure: dict[str, Any] = {
        "pressure_version": "v1",
        "pressure_class": _RANK_PRESSURE[highest],
        "contributing_reasons": contributions,
        "details_redacted": details_redacted,
        "generated_at": generated_at or matrix.get("generated_at"),
    }
    if correlation_id is not None:
        pressure["correlation_id"] = correlation_id
    return pressure
