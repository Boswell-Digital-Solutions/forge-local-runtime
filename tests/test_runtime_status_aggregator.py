"""Tests for the runtime status aggregator (service matrix + pressure)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from runtime_status import build_service_matrix, derive_pressure

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"

GENERATED_AT = "2026-06-20T12:00:00Z"


def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _status(service_id: str, state: str, **extra) -> dict:
    status = {
        "service_id": service_id,
        "state": state,
        "operator_visible_message": f"{service_id} reporting {state}.",
        "last_updated_at": "2026-06-20T11:59:00Z",
    }
    status.update(extra)
    return status


def _ready(service_id: str) -> dict:
    return _status(
        service_id,
        "ready",
        readiness_summary={"readiness_class": "ready", "summary": "ready"},
    )


# ── build_service_matrix ─────────────────────────────────────────────────────


def test_matrix_always_represents_all_four_services():
    matrix = build_service_matrix(
        [_ready("cortex")], generated_at=GENERATED_AT
    )
    ids = {s["service_id"] for s in matrix["services"]}
    assert ids == {"df-local-foundation", "neuronforge-local", "cortex", "fa-local"}
    assert len(matrix["services"]) == 4


def test_missing_service_is_fail_closed_unavailable():
    matrix = build_service_matrix([_ready("cortex")], generated_at=GENERATED_AT)
    by_id = {s["service_id"]: s for s in matrix["services"]}
    missing = by_id["fa-local"]
    assert missing["state"] == "unavailable"
    assert missing["readiness_class"] == "not_ready"
    assert missing["observation"] == "missing"
    assert missing["blocking_reasons"] == ["dependency_unavailable"]


def test_matrix_conforms_to_schema():
    statuses = [
        _ready("df-local-foundation"),
        _status(
            "neuronforge-local",
            "degraded",
            degraded_subtype="degraded_fallback_limited",
            readiness_summary={"readiness_class": "ready_with_constraints", "summary": "limited"},
        ),
        _ready("cortex"),
        # fa-local omitted on purpose -> filled fail-closed
    ]
    matrix = build_service_matrix(statuses, generated_at=GENERATED_AT, correlation_id="run-1")
    errors = list(_validator("runtime-service-matrix.schema.json").iter_errors(matrix))
    assert errors == [], [e.message for e in errors]


def test_unknown_service_id_rejected():
    with pytest.raises(ValueError):
        build_service_matrix([_ready("rake")], generated_at=GENERATED_AT)


def test_duplicate_service_rejected():
    with pytest.raises(ValueError):
        build_service_matrix(
            [_ready("cortex"), _ready("cortex")], generated_at=GENERATED_AT
        )


# ── derive_pressure ──────────────────────────────────────────────────────────


def _matrix(*statuses: dict) -> dict:
    return build_service_matrix(list(statuses), generated_at=GENERATED_AT)


def test_pressure_low_when_all_ready():
    matrix = build_service_matrix(
        [_ready(s) for s, _ in
         (("df-local-foundation", 0), ("neuronforge-local", 0), ("cortex", 0), ("fa-local", 0))],
        generated_at=GENERATED_AT,
    )
    pressure = derive_pressure(matrix)
    assert pressure["pressure_class"] == "low"
    assert pressure["contributing_reasons"] == []


def test_pressure_elevated_on_degraded():
    matrix = _matrix(
        _ready("df-local-foundation"),
        _status(
            "neuronforge-local",
            "degraded",
            degraded_subtype="degraded_partial",
            readiness_summary={"readiness_class": "degraded", "summary": "partial"},
        ),
        _ready("cortex"),
        _ready("fa-local"),
    )
    pressure = derive_pressure(matrix)
    assert pressure["pressure_class"] == "elevated"
    assert pressure["contributing_reasons"] == [
        {"service_id": "neuronforge-local", "signal": "degraded", "raised_to": "elevated"}
    ]


def test_pressure_critical_on_unavailable():
    # fa-local omitted -> fail-closed unavailable -> critical
    matrix = _matrix(_ready("df-local-foundation"), _ready("neuronforge-local"), _ready("cortex"))
    pressure = derive_pressure(matrix)
    assert pressure["pressure_class"] == "critical"
    assert any(r["service_id"] == "fa-local" and r["raised_to"] == "critical"
               for r in pressure["contributing_reasons"])


def test_pressure_takes_max_across_services():
    matrix = _matrix(
        _status("df-local-foundation", "stale",
                readiness_summary={"readiness_class": "ready_with_constraints", "summary": "stale"}),
        _ready("neuronforge-local"),
        _ready("cortex"),
        # fa-local missing -> critical
    )
    pressure = derive_pressure(matrix)
    assert pressure["pressure_class"] == "critical"


def test_pressure_is_deterministic_and_schema_valid():
    matrix = _matrix(
        _ready("df-local-foundation"),
        _status("neuronforge-local", "degraded", degraded_subtype="degraded_partial"),
        _ready("cortex"),
    )
    first = derive_pressure(matrix)
    second = derive_pressure(matrix)
    assert first == second
    errors = list(_validator("runtime-pressure.schema.json").iter_errors(first))
    assert errors == [], [e.message for e in errors]
