#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = ROOT / "schemas"
TESTS_DIR = ROOT / "tests"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_file(instance_path: Path, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    instance = load_json(instance_path)

    validator = Draft202012Validator(schema)

    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    messages: list[str] = []

    for error in errors:
        loc = ".".join(str(part) for part in error.path) or "<root>"
        messages.append(f"{instance_path}: {loc}: {error.message}")

    return messages


def expect_valid(instance_path: Path, schema_path: Path) -> list[str]:
    return validate_file(instance_path, schema_path)


def expect_invalid(instance_path: Path, schema_path: Path) -> list[str]:
    errors = validate_file(instance_path, schema_path)
    if errors:
        return []
    return [f"{instance_path}: expected invalid but validation passed"]


def main() -> int:
    failures: list[str] = []

    valid_cases = [
        (
            TESTS_DIR / "contracts/fixtures/valid/service-status-cortex-degraded.json",
            SCHEMAS_DIR / "service-status.schema.json",
        ),
        (
            TESTS_DIR / "observability/fixtures/forensic-event-minimized.json",
            SCHEMAS_DIR / "forensic-event-envelope.schema.json",
        ),
    ]

    invalid_cases = [
        (
            TESTS_DIR / "contracts/fixtures/invalid/service-status-degraded-missing-subtype.json",
            SCHEMAS_DIR / "service-status.schema.json",
        ),
        (
            TESTS_DIR / "observability/fixtures/forensic-event-content-without-reference.json",
            SCHEMAS_DIR / "forensic-event-envelope.schema.json",
        ),
    ]

    for instance_path, schema_path in valid_cases:
        failures.extend(expect_valid(instance_path, schema_path))

    for instance_path, schema_path in invalid_cases:
        failures.extend(expect_invalid(instance_path, schema_path))

    if failures:
        print("VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())