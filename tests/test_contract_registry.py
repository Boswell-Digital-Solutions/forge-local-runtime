"""Tests for the Local Runtime Contract Registry artifact."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/contract-registry.schema.json"
REGISTRY = ROOT / "registry/local-runtime-contract-registry.json"

KNOWN_OWNERS = {
    "df-local-foundation",
    "neuronforge-local",
    "cortex",
    "fa-local",
    "forge-local-runtime",
}


def _registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_registry_conforms_to_schema():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(_registry()))
    assert errors == [], [e.message for e in errors]


def test_seam_ids_unique():
    seams = _registry()["seams"]
    ids = [s["seam_id"] for s in seams]
    assert len(ids) == len(set(ids))


def test_owners_are_known():
    for seam in _registry()["seams"]:
        assert seam["owner"] in KNOWN_OWNERS


def test_scene_window_drift_is_recorded_as_planned():
    seams = {s["contract_id"]: s for s in _registry()["seams"]}
    assert seams["analyze.continuity.adjacent_scene.v1"]["maturity"] == "implemented"
    assert seams["analyze.continuity.scene_window.v1"]["maturity"] == "planned"


def test_runtime_status_surfaces_present_and_implemented():
    by_contract = {s["contract_id"]: s for s in _registry()["seams"]}
    for contract_id in ("runtime-service-matrix", "runtime-pressure"):
        assert by_contract[contract_id]["owner"] == "forge-local-runtime"
        assert by_contract[contract_id]["maturity"] == "implemented"
        assert by_contract[contract_id]["posture"] == "observational"
