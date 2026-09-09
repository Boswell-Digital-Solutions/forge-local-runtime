# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

forge-local-runtime is the governance-first constitutional repository for the shared local service substrate of the Forge ecosystem. It governs — but does not implement — the **public-app** local services: DF Local Foundation, NeuronForge Local, Cortex, FA Local, and Bellows. It defines runtime doctrine, cross-service boundaries, ownership/non-ownership lines, readiness/degraded/denial posture, handoff rules, privacy-preserving observability constraints, and the shared schemas those services must speak.

**Not `forge-local-systems-runtime`.** Near-identical names, and both are doctrine repos that implement nothing. This one governs the public-app local services; `ecosystem/local-systems/forge-local-systems-runtime` governs the business-side local services. Applying one side's doctrine to the other side's services is the failure mode.

## Common Commands

- `make validate` — runs `validate-schemas` + `check-boundaries` + `check-contract-boundaries`
- `python scripts/validate_schemas.py` — checks the contract corpus
- `python scripts/check_boundaries.py` — checks that declared ownership boundaries hold
- `python scripts/check_contract_boundaries.py` — checks contract boundary rules
- `python -m pytest tests -q` — the suites under `tests/boundaries/`, `tests/contracts/`, and `tests/observability/` are where a doctrine change proves itself
- `bash doc/system/BUILD.sh` — assembles the canonical `doc/FOLSYSTEM.md` from `doc/system/`
- `./scripts/context-bundle.sh --list`

## Architecture

The doctrine is expressed as schemas, not prose — [`schemas/`](schemas/) defines `runtime-contract`, `service-status`, `readiness-summary`, `handoff-envelope`, `degraded-state`, `denial-state`, and `forensic-event-envelope`. A local service that reports readiness, degradation, or denial does it in these shapes.

Five governed local services, each with a bounded role:
- **DF Local Foundation** — local data/control substrate: registration, persistence lifecycle, migrations, backup/restore/export, bounded integrity/recovery
- **NeuronForge Local** — local inference/candidate production: task-contract execution, model/profile routing, candidate output, degraded-inference truth
- **Cortex** — local file intelligence/retrieval prep: intake, syntax-level extraction, provenance, indexing/retrieval/packaging prep, bounded operational truth
- **FA Local** — governed local execution: trusted request intake, requester trust resolution, policy evaluation, capability admission, bounded execution-plan validation, execution coordination, truthful status reporting
- **Bellows** — local audio capture/device transport (ADR 0010): capture and device readiness, VAD segmentation, duplex arbitration, device-level playback of already-produced hash-validated assets, capture/playback receipts by ref+hash, visible recording-state signaling; never listens silently or continuously

Cross-service interpretation rule: each service may do its bounded job but must not absorb another's authority (e.g. DF Local may persist artifacts but must not become workflow/semantic authority; NeuronForge Local may produce candidates but must not silently promote them into truth; FA Local may execute under policy but must not become the hidden planner).

Standing doctrine also lives in `BOUNDARIES.md`, `ARCHITECTURE.md`, and `DECISIONS/`. Canonical assembled reference: `doc/FOLSYSTEM.md` (see Common Commands to build it).

## Notes

- **Degraded and denied are declared states, never silent fallbacks.** `degraded-state` and `denial-state` exist so a service cannot quietly pretend to be healthy.
- Runtime promotion is receipted: `runtime_promotion/` and `receipts/` carry the evidence, and promotion policy is enforced, not assumed.
- Do not add service implementation here to "make it work" — the boundary is the product. This repo is a governance-and-contracts authority repo; it does not exist to absorb implementation from the service repos by convenience.
- The local runtime must remain meaningful without cloud — cloud services may amplify capability (research depth, connector breadth, orchestration scale) but must not redefine the minimum local baseline.
- `AGENTS.md`, `CODEX.md`, and `GEMINI.md` in this repo are generated from `repo.manifest.yaml` via `scripts/generate_agent_instructions.py`; this `CLAUDE.md` is hand-maintained rather than regenerated, so keep it in sync with real doctrine changes by hand rather than running the generator over it.
