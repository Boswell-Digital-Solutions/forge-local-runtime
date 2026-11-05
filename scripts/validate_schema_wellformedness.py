#!/usr/bin/env python3
"""Validate Forge Local Runtime JSON Schemas against their declared drafts.

Forge Local Runtime owns shared schemas and a validation posture (see README
and BOUNDARIES). This harness enforces that posture: every *populated* schema
under ``schemas/`` must be well-formed JSON and a valid JSON Schema. Empty stub
files are reported as pending (not yet authored) and do not fail the gate, so
the check grows with the repo as schemas are filled in.

Exit codes:
  0 — all populated schemas are well-formed (empty stubs allowed, reported)
  1 — one or more populated schemas are malformed JSON or invalid schemas
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def main() -> int:
    schema_files = sorted(SCHEMA_DIR.glob("*.schema.json"))
    if not schema_files:
        print(f"ERROR: no *.schema.json files found under {SCHEMA_DIR}")
        return 1

    validated: list[str] = []
    pending: list[str] = []
    failures: list[tuple[str, str]] = []

    for path in schema_files:
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            pending.append(path.name)
            continue
        try:
            schema = json.loads(raw)
        except json.JSONDecodeError as exc:
            failures.append((path.name, f"invalid JSON: {exc}"))
            continue
        validator_cls = validator_for(schema)
        try:
            validator_cls.check_schema(schema)
        except SchemaError as exc:
            failures.append((path.name, f"invalid JSON Schema: {exc.message}"))
            continue
        validated.append(path.name)

    print(f"schemas dir: {SCHEMA_DIR}")
    print(f"  validated: {len(validated)}")
    for name in validated:
        print(f"    ✓ {name}")
    print(f"  pending (empty stub, not yet authored): {len(pending)}")
    for name in pending:
        print(f"    · {name}")

    if failures:
        print(f"  FAILURES: {len(failures)}")
        for name, why in failures:
            print(f"    ✗ {name}: {why}")
        return 1

    print("schema validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
