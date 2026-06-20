#!/usr/bin/env python3
"""Emit a runtime service-matrix + pressure snapshot from published statuses.

Reads each service's last-published ``service-status`` JSON from a directory,
composes the four-service matrix, derives the pressure indicator, and prints a
schema-valid snapshot. Services that did not publish are represented fail-closed
as ``unavailable`` by the aggregator.

The emitted snapshot is validated against its schemas before output: this tool
never emits a non-conforming snapshot (fail-closed).

Usage:
  python scripts/emit_runtime_status.py --status-dir examples/status-sample
  python scripts/emit_runtime_status.py --status-dir <dir> --out snapshot.json --pretty
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

# Allow direct invocation (python scripts/emit_runtime_status.py) by putting the
# repo root on the path before importing the local package.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime_status import build_service_matrix, derive_pressure, load_status_directory  # noqa: E402


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def build_snapshot(
    status_dir: str | Path,
    *,
    generated_at: str | None = None,
    correlation_id: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Build a {service_matrix, pressure} snapshot and any collection warnings."""
    generated_at = generated_at or _utc_now()
    collected = load_status_directory(status_dir)
    matrix = build_service_matrix(
        collected.statuses,
        generated_at=generated_at,
        correlation_id=correlation_id,
    )
    pressure = derive_pressure(matrix, correlation_id=correlation_id)
    return {"service_matrix": matrix, "pressure": pressure}, collected.errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--status-dir",
        required=True,
        help="Directory of per-service service-status JSON files.",
    )
    parser.add_argument("--out", default="-", help="Output path, or - for stdout.")
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Override snapshot timestamp (RFC3339). Defaults to now (UTC).",
    )
    parser.add_argument("--correlation-id", default=None)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    try:
        snapshot, warnings = build_snapshot(
            args.status_dir,
            generated_at=args.generated_at,
            correlation_id=args.correlation_id,
        )
    except ValueError as exc:  # unknown / duplicate service_id
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    # Fail-closed: never emit a non-conforming snapshot.
    errors = list(_validator("runtime-service-matrix.schema.json").iter_errors(snapshot["service_matrix"]))
    errors += list(_validator("runtime-pressure.schema.json").iter_errors(snapshot["pressure"]))
    if errors:
        for error in errors:
            print(f"error: emitted snapshot invalid: {error.message}", file=sys.stderr)
        return 3

    text = json.dumps(snapshot, indent=2 if args.pretty else None)
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote snapshot: {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
