"""Tests for the runtime status snapshot CLI."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "emit_runtime_status", ROOT / "scripts/emit_runtime_status.py"
)
emit = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(emit)

GENERATED_AT = "2026-06-20T12:00:00Z"


def _write_status(directory: Path, service_id: str, service_class: str, state: str, **extra) -> None:
    payload = {
        "service_id": service_id,
        "service_class": service_class,
        "state": state,
        "operator_visible_message": f"{service_id} {state}",
        "last_updated_at": "2026-06-20T11:59:00Z",
    }
    payload.update(extra)
    (directory / f"{service_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_build_snapshot_fills_missing_and_validates(tmp_path):
    _write_status(tmp_path, "cortex", "file_intelligence", "ready")
    snapshot, warnings = emit.build_snapshot(tmp_path, generated_at=GENERATED_AT)
    assert warnings == []
    ids = {s["service_id"] for s in snapshot["service_matrix"]["services"]}
    assert ids == {"df-local-foundation", "neuronforge-local", "cortex", "fa-local"}
    # missing services -> fail-closed unavailable -> critical pressure
    assert snapshot["pressure"]["pressure_class"] == "critical"


def test_build_snapshot_reports_collection_errors(tmp_path):
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    _write_status(tmp_path, "cortex", "file_intelligence", "ready")
    _, warnings = emit.build_snapshot(tmp_path, generated_at=GENERATED_AT)
    assert any("invalid JSON" in w for w in warnings)


def test_cli_writes_schema_valid_snapshot(tmp_path):
    _write_status(tmp_path, "df-local-foundation", "substrate", "ready")
    _write_status(tmp_path, "neuronforge-local", "inference", "ready")
    _write_status(tmp_path, "cortex", "file_intelligence", "ready")
    _write_status(tmp_path, "fa-local", "execution", "ready")
    out = tmp_path / "snapshot.json"
    rc = emit.main(
        ["--status-dir", str(tmp_path), "--out", str(out), "--generated-at", GENERATED_AT]
    )
    assert rc == 0
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["pressure"]["pressure_class"] == "low"


def test_cli_runs_on_shipped_example():
    rc = emit.main(["--status-dir", str(ROOT / "examples/status-sample"), "--generated-at", GENERATED_AT])
    assert rc == 0
