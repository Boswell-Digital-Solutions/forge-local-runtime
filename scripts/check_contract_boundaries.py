#!/usr/bin/env python3
"""Cross-service boundary assertions for Forge Local Runtime.

This repo owns the shared schemas and the contract registry, so the boundaries it
can enforce in CI are the ones expressed in those artifacts:

1. **Registry posture invariants** — candidate-producing services (Cortex,
   NeuronForge Local) are never registered with an authority/observational/
   governance posture; observational and governance postures are owned only by
   forge-local-runtime. This encodes the candidate-only and non-authority
   doctrine at the catalog level.

2. **Orchestration firewall** — the shared handoff / status schemas must not
   define orchestration fields (retry/workflow/queue/executor/dispatch/agent
   assignment). Status and handoff are transfer-truth, not control planes.

Exit codes:
  0 — all boundary assertions hold
  1 — one or more violations
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/local-runtime-contract-registry.json"
SCHEMAS = ROOT / "schemas"

# Schemas that are transfer-truth / status surfaces and must stay control-plane free.
FIREWALLED_SCHEMAS = (
    "handoff-envelope.schema.json",
    "runtime-service-matrix.schema.json",
    "runtime-pressure.schema.json",
    "service-status.schema.json",
)

FORBIDDEN_ORCHESTRATION_FIELDS = frozenset(
    {
        "retry_count",
        "retry_policy",
        "workflow_id",
        "queue_name",
        "executor",
        "dispatch_plan",
        "orchestration_state",
        "agent_assignment",
    }
)

CANDIDATE_ONLY_OWNERS = frozenset({"cortex", "neuronforge-local"})
RUNTIME_ONLY_POSTURES = frozenset({"observational", "governance"})


def property_names(schema: Any) -> set[str]:
    """Collect every declared object-property name anywhere in a JSON Schema."""
    names: set[str] = set()
    if isinstance(schema, dict):
        props = schema.get("properties")
        if isinstance(props, dict):
            names.update(props.keys())
        for value in schema.values():
            names |= property_names(value)
    elif isinstance(schema, list):
        for item in schema:
            names |= property_names(item)
    return names


def registry_posture_violations(registry: dict) -> list[str]:
    violations: list[str] = []
    for seam in registry.get("seams", []):
        owner = seam.get("owner")
        posture = seam.get("posture")
        seam_id = seam.get("seam_id", "<unknown>")
        if owner in CANDIDATE_ONLY_OWNERS and posture != "candidate":
            violations.append(
                f"{seam_id}: {owner} is a candidate-only producer but posture is {posture!r}"
            )
        if posture in RUNTIME_ONLY_POSTURES and owner != "forge-local-runtime":
            violations.append(
                f"{seam_id}: posture {posture!r} may only be owned by forge-local-runtime, not {owner!r}"
            )
    return violations


def orchestration_violations() -> list[str]:
    violations: list[str] = []
    for name in FIREWALLED_SCHEMAS:
        path = SCHEMAS / name
        if not path.exists():
            continue
        schema = json.loads(path.read_text(encoding="utf-8"))
        leaked = sorted(property_names(schema) & FORBIDDEN_ORCHESTRATION_FIELDS)
        if leaked:
            violations.append(f"{name}: orchestration fields present: {', '.join(leaked)}")
    return violations


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    failures = registry_posture_violations(registry) + orchestration_violations()

    if failures:
        print("CONTRACT BOUNDARY CHECK FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONTRACT BOUNDARY CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
