#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tests/boundaries/fixtures/boundary-manifest.json"


REQUIRED_ASSERTIONS = {
    "df-local-foundation": {
        "workflow_authority",
        "semantic_authority",
        "execution_authority",
        "inference_authority",
    },
    "neuronforge-local": {
        "final_truth_authority",
        "workflow_authority",
        "open_ended_autonomy",
        "execution_governance",
    },
    "cortex": {
        "semantic_interpretation",
        "workflow_control",
        "generic_etl_platform",
        "surveillance_by_default",
    },
    "fa-local": {
        "durable_semantic_memory",
        "app_semantic_authority",
        "open_ended_planning",
        "ungoverned_tool_access",
    },
}


def main() -> int:
    with MANIFEST.open("r", encoding="utf-8") as f:
        data = json.load(f)

    services = data.get("services", [])
    found = {svc["service_id"]: set(svc.get("must_not_claim", [])) for svc in services}

    failures: list[str] = []

    for service_id, required in REQUIRED_ASSERTIONS.items():
        actual = found.get(service_id)
        if actual is None:
            failures.append(f"missing service entry: {service_id}")
            continue

        missing = sorted(required - actual)
        if missing:
            failures.append(
                f"{service_id} missing must_not_claim assertions: {', '.join(missing)}"
            )

    extra_services = sorted(set(found) - set(REQUIRED_ASSERTIONS))
    if extra_services:
        failures.append(
            f"unexpected services present in boundary manifest: {', '.join(extra_services)}"
        )

    if failures:
        print("BOUNDARY CHECK FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("BOUNDARY CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())