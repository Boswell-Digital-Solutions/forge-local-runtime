# BUILD.md — Forge Local Runtime Repo Build and Change Rules

## Purpose

This document defines how work is allowed to proceed inside the Forge Local Runtime repository.

This repository is a constitutional authority surface for the local runtime layer.
It is not a convenience implementation repo.

All future changes in this repository must preserve that posture.

## What this repository is allowed to contain

This repository may contain:

- top-level constitutional documents
- architecture and boundary documents
- decision records
- doctrine and control documents
- shared JSON schemas
- fixtures for schema and boundary validation
- lightweight validation scripts
- machine-readable anti-drift artifacts
- narrowly justified repo-local tooling that supports validation of the above

## What this repository must not become

This repository must not become:

- a Tauri app
- a Svelte frontend
- a runtime daemon
- a service executable
- a shared implementation monolith
- a hidden orchestrator
- a semantic authority layer
- a generic ETL platform
- a broad observability or surveillance tool
- a convenience sink for service implementation code

## Governing build rule

Implementation must not outrun authority artifacts.

If a change would expand runtime behavior, the required constitutional and control artifacts must be updated first or in the same change set.

## Required change bundles

The following changes must be updated together.

### 1. New capability added to a governed service

Must update:

- the relevant `docs/services/*.md` role file
- `docs/architecture/boundary-matrix.md`
- any affected doctrine or control docs
- any affected schemas
- fixtures and validation scripts if schema/control language changes

### 2. New denial or degraded state introduced

Must update:

- `docs/doctrine/degraded-state-contract.md` and/or `docs/control/denial-taxonomy.md`
- `schemas/degraded-state.schema.json` and/or `schemas/denial-state.schema.json`
- `schemas/service-status.schema.json` if envelope behavior changes
- valid and invalid fixtures
- validator expectations if needed
- ADR if the new state changes runtime-wide vocabulary significantly

### 3. New handoff status or reverse signal introduced

Must update:

- `docs/architecture/handoff-rules.md`
- `docs/doctrine/syntax-vs-semantics-firewall.md` if Cortex or bounded reverse signaling posture is affected
- `schemas/handoff-envelope.schema.json`
- fixtures
- validation script coverage
- ADR if the change broadens control language materially

### 4. New requester class, policy posture, approval posture, or capability-admission concept introduced

Must update:

- `docs/control/requester-trust-model.md`
- `docs/doctrine/policy-before-execution.md`
- `docs/architecture/runtime-control-surfaces.md`
- `schemas/runtime-contract.schema.json`
- `schemas/forensic-event-envelope.schema.json` if forensic posture changes
- fixtures and validation coverage
- ADR if the change materially expands execution governance language

### 5. Privacy or observability posture expanded

Must update:

- `docs/doctrine/privacy-preserving-observability.md`
- `docs/control/local-observability-policy.md`
- `docs/control/forensic-retention.md` if retention is affected
- affected schemas
- affected fixtures
- boundary matrix rows if privacy sensitivity changes
- ADR if the change expands observational power in a meaningful way

### 6. Backup, restore, migration, or integrity behavior changes

Must update:

- `docs/control/backup-restore-constraints.md`
- `docs/control/migration-lifecycle.md`
- relevant DF Local Foundation role sections
- `docs/architecture/boundary-matrix.md`
- affected schemas and fixtures if state language changes

## ADR trigger rules

Create or update an ADR when a change does any of the following:

- changes repo framing
- changes service-only classification
- changes local-versus-cloud constitutional boundary
- changes authority boundaries
- changes runtime-wide denial or degraded vocabulary materially
- changes privacy-preserving observability posture materially
- broadens handoff semantics materially
- introduces a new split-trigger-worthy subsystem
- creates a new reusable runtime governance primitive
- changes what this repository is allowed to own

## Boundary matrix trigger rules

`docs/architecture/boundary-matrix.md` must be updated whenever:

- a new governed capability is introduced
- a capability changes owner
- a capability changes non-ownership lines
- privacy sensitivity changes
- degraded behavior changes
- cloud augmentation posture changes
- authority pressure changes
- split-trigger relevance changes

## Schema change rules

A schema change is not complete unless all of the following are true:

1. the schema file is updated
2. at least one valid fixture covers the intended behavior
3. at least one invalid fixture covers a relevant failure mode
4. `python scripts/validate_schemas.py` still passes
5. any affected prose docs are updated to match

## Boundary manifest rules

The boundary manifest is an anti-drift artifact.

If a service gains a new forbidden authority claim, the manifest must be updated and `python scripts/check_boundaries.py` must still pass.

New services must not be added casually.
A new service entry requires architectural justification and likely an ADR.

## Validation rules

Before merging or accepting a meaningful repo change, run:

```bash
make validate