# CODEX.md — Forge Local Runtime Operating Instructions for Codex

## Purpose

This file tells Codex how to work inside the Forge Local Runtime repository.

This repository is a constitutional authority repo for the Forge local runtime layer.
It is not a product repo and not a service implementation repo.

Codex must preserve that distinction at all times.

## Repo identity

Forge Local Runtime governs the local runtime layer above these four service-only systems:

- DF Local Foundation
- NeuronForge Local
- Cortex
- FA Local

This repo owns:

- doctrine
- boundaries
- decision records
- shared schemas
- fixtures
- lightweight validation
- machine-readable anti-drift artifacts

This repo does not own:

- service executables
- application logic
- product workflows
- runtime daemons
- orchestrator implementations
- UI applications
- broad business logic libraries

## Hard constraints

Codex must not:

- add a Tauri app
- add a Svelte UI
- add a service runner or daemon
- add implementation code for Cortex, FA Local, NeuronForge Local, or DF Local Foundation
- add generic ETL abstractions
- add hidden orchestration logic
- add semantic authority surfaces
- add surveillance-oriented observability tools
- broaden handoff into workflow control
- treat this repo like a normal feature repo

## What Codex may do

Codex may:

- improve documentation clarity without broadening ownership
- add or refine ADRs
- refine service role docs
- refine doctrine/control docs
- add or refine shared schemas
- add valid and invalid fixtures
- add lightweight validation checks
- add machine-readable anti-drift artifacts
- improve repo-local validation ergonomics

## Required synchronization rules

If Codex changes a service capability boundary, it must also check and update:

- the relevant `docs/services/*.md` file
- `docs/architecture/boundary-matrix.md`
- any affected doctrine/control docs
- any affected schemas
- fixtures and validators if schema behavior changes

If Codex changes denial, degraded, readiness, handoff, trust, approval, or forensic vocabulary, it must also update the corresponding docs, schemas, fixtures, and validation expectations.

## ADR rules

Codex should create or update an ADR when a change materially affects:

- repo framing
- ownership or non-ownership lines
- local vs cloud constitutional boundary
- authority posture
- runtime-wide state vocabulary
- observability posture
- handoff semantics
- split-trigger policy
- what this repo is allowed to own

## Boundary matrix rules

Codex must update `docs/architecture/boundary-matrix.md` whenever a change affects:

- capability ownership
- explicit non-ownership
- local baseline requirement
- cloud augmentation posture
- authority status
- privacy sensitivity
- degraded behavior
- split-trigger relevance

## Validation rules

Before considering work complete, Codex must run:

```bash
make validate