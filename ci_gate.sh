#!/usr/bin/env bash
# Forge Local Runtime CI gate — proving-slice contract participation
#
# Forge Local Runtime is the governance + shared-schema repository for the
# local service substrate, and governs FA Local — the execution_consumer
# (fa-local) in the forge-contract-core repo role matrix. This gate wires the
# repo into the canonical contract-core gate runner and enforces the repo's
# own schema validation posture.
#
# Gate 1 (contract-core): validates schemas, fixture corpus, validator
# correctness, compatibility notes, and forbidden patterns — using the shared
# contract library, under the fa-local participation label.
#
# Gate 2 (schema posture): validates that every populated JSON Schema under
# schemas/ is well-formed. Empty stub schemas are reported as pending (not yet
# authored) and do not fail the gate, so enforcement grows as schemas land.
#
# Exit codes:
#   0 — all gates pass
#   1 — one or more gates failed
#
# Usage (from the Forge Local Runtime root):
#   bash ci_gate.sh
#
# Usage (explicit contract-core location):
#   CONTRACT_CORE_PATH=/path/to/forge-contract-core bash ci_gate.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="$SCRIPT_DIR/reports"

# ── Resolve forge-contract-core (override-friendly) ──────────────────────────
resolve_contract_core() {
    if [[ -n "${CONTRACT_CORE_PATH:-}" ]]; then
        printf '%s\n' "$CONTRACT_CORE_PATH"
        return 0
    fi
    local candidates=(
        "$SCRIPT_DIR/../../contracts/forge-contract-core"
        "$SCRIPT_DIR/../contracts/forge-contract-core"
        "$SCRIPT_DIR/contracts/forge-contract-core"
        "$SCRIPT_DIR/../forge-contract-core"
        "$SCRIPT_DIR/../forge_contract_core"
    )
    local c
    for c in "${candidates[@]}"; do
        if [[ -f "$c/forge_contract_core/gates/run_all.py" ]]; then
            (cd "$c" && pwd)
            return 0
        fi
    done
    return 1
}

if ! CONTRACT_CORE_PATH="$(resolve_contract_core)"; then
    echo "ERROR: forge-contract-core gate runner not found."
    echo "       Set CONTRACT_CORE_PATH to a forge-contract-core checkout."
    exit 1
fi

echo "Forge Local Runtime CI gate — proving-slice contract participation"
echo "  contract core path: $CONTRACT_CORE_PATH"
echo ""

PYTHON_CONTRACT="$CONTRACT_CORE_PATH/.venv/bin/python"
if [[ ! -x "$PYTHON_CONTRACT" ]]; then
    PYTHON_CONTRACT="python3"
fi

PYTHON_LOCAL="$SCRIPT_DIR/.venv/bin/python"
if [[ ! -x "$PYTHON_LOCAL" ]]; then
    PYTHON_LOCAL="$SCRIPT_DIR/venv/bin/python"
fi
if [[ ! -x "$PYTHON_LOCAL" ]]; then
    PYTHON_LOCAL="python3"
fi

echo "  python (contract gate): $PYTHON_CONTRACT"
echo "  python (schema gate):   $PYTHON_LOCAL"
echo ""

mkdir -p "$REPORT_DIR"

# ── Gate 1: forge-contract-core canonical gate runner ────────────────────────
echo "=== Gate 1: forge-contract-core canonical gate ==="
GATE_REPORT="$REPORT_DIR/contract_core_gate_$(date +%Y%m%d_%H%M%S).json"
PYTHONPATH="$CONTRACT_CORE_PATH" "$PYTHON_CONTRACT" -m forge_contract_core.gates.run_all \
    --repo "fa-local" \
    --report-out "$GATE_REPORT"

echo ""
# ── Gate 2: local schema validation posture ──────────────────────────────────
echo "=== Gate 2: local schema validation ==="
cd "$SCRIPT_DIR"
# Schema-file well-formedness gate. The instance-validation harness
# (scripts/validate_schemas.py, wired into the Makefile) is a separate concern.
"$PYTHON_LOCAL" scripts/validate_schema_wellformedness.py

echo ""
echo "Forge Local Runtime CI gate: PASSED"
echo "  contract core gate report: $GATE_REPORT"
