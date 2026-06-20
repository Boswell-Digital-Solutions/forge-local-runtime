"""Status sources for the runtime aggregator.

A status source supplies the per-service ``service-status`` envelopes that
``build_service_matrix`` composes. This repo ships a file-backed source that
reads whatever each service last published to a directory — the honest meaning
of "live" status without inventing a transport this repo does not own.

A network transport (each service answering a status probe) is intentionally a
documented future seam, not stubbed here, per the repo rule against inventing
undocumented routes.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CollectedStatuses:
    """Statuses gathered from a source, plus non-fatal collection errors.

    Errors are surfaced (never swallowed); affected services simply do not appear
    in ``statuses`` and are filled fail-closed by the aggregator.
    """

    statuses: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def load_status_directory(path: str | Path) -> CollectedStatuses:
    """Load ``service-status`` envelopes from ``*.json`` files in a directory.

    A file that is not valid JSON, or is not a ``service-status`` object, is
    recorded as a collection error and excluded — it is never partially trusted.
    """
    directory = Path(path)
    collected = CollectedStatuses()

    if not directory.is_dir():
        collected.errors.append(f"status dir not found: {directory}")
        return collected

    for json_path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            collected.errors.append(f"{json_path.name}: invalid JSON: {exc}")
            continue
        if not isinstance(data, dict) or "service_id" not in data:
            collected.errors.append(f"{json_path.name}: not a service-status object")
            continue
        collected.statuses.append(data)

    return collected
