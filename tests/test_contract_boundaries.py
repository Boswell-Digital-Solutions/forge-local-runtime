"""Tests for the cross-service contract boundary assertions."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_contract_boundaries", ROOT / "scripts/check_contract_boundaries.py"
)
cb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(cb)


def test_gate_passes_on_current_artifacts():
    assert cb.main() == 0


def test_property_names_walks_nested_schema():
    schema = {
        "properties": {
            "a": {"type": "string"},
            "b": {"properties": {"executor": {"type": "string"}}},
        },
        "items": {"properties": {"workflow_id": {"type": "string"}}},
    }
    assert cb.property_names(schema) == {"a", "b", "executor", "workflow_id"}


def test_orchestration_field_is_detected():
    leaked = cb.property_names(
        {"properties": {"retry_count": {"type": "integer"}}}
    ) & cb.FORBIDDEN_ORCHESTRATION_FIELDS
    assert leaked == {"retry_count"}


def test_candidate_owner_with_authority_posture_is_flagged():
    registry = {
        "seams": [
            {
                "seam_id": "cortex/bad",
                "owner": "cortex",
                "posture": "authority",
            }
        ]
    }
    violations = cb.registry_posture_violations(registry)
    assert len(violations) == 1
    assert "candidate-only producer" in violations[0]


def test_observational_posture_owned_by_non_runtime_is_flagged():
    registry = {
        "seams": [
            {
                "seam_id": "cortex/obs",
                "owner": "cortex",
                "posture": "observational",
            }
        ]
    }
    violations = cb.registry_posture_violations(registry)
    # cortex is candidate-only AND observational is runtime-only → two violations
    assert any("may only be owned by forge-local-runtime" in v for v in violations)


def test_clean_registry_has_no_violations():
    registry = {
        "seams": [
            {"seam_id": "x", "owner": "forge-local-runtime", "posture": "observational"},
            {"seam_id": "y", "owner": "neuronforge-local", "posture": "candidate"},
        ]
    }
    assert cb.registry_posture_violations(registry) == []
