# Runtime Control Surfaces — Forge Local Runtime

## Purpose

This document defines the bounded control surfaces that Forge Local Runtime owns across the four governed local services.

## Rule

A control surface is valid only if it is:

- constitutionally owned
- bounded
- reviewable
- privacy-preserving where applicable
- non-expansive in authority

The runtime must not create broad convenience control planes that silently centralize authority.

## Shared runtime control surfaces

The runtime owns shared control language for:

- service status
- readiness summary
- degraded-state reporting
- denial-state reporting
- handoff result posture
- requester trust posture
- policy posture
- approval posture
- capability admission posture
- forensic event minimization posture

## Service-specific control surfaces

### DF Local Foundation
Owns substrate-facing control surfaces for:

- migration posture
- restore posture
- backup/export posture
- readiness and integrity posture
- bounded retention and maintenance posture

### NeuronForge Local
Owns inference-facing control surfaces for:

- route class
- contract-shaped execution posture
- candidate-production posture
- degraded and fallback truth
- inference readiness

### Cortex
Owns file-intelligence-facing control surfaces for:

- intake posture
- syntax extraction completeness
- freshness/staleness posture
- integrity posture
- bounded handoff posture
- privacy-preserving diagnostics for owned surfaces

### FA Local
Owns execution-facing control surfaces for:

- requester trust resolution
- policy posture
- capability admission
- approval posture
- bounded-plan validation posture
- denial/review/degraded/completed-with-constraints reporting
- minimized forensic event posture

## Anti-drift rule

A runtime control surface must not become:

- a hidden workflow engine
- a semantic authority surface
- a broad surveillance surface
- a substitute for application truth
- an unbounded orchestration layer

## Schema alignment

Runtime control surfaces align with:

- `schemas/service-status.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/handoff-envelope.schema.json`
- `schemas/readiness-summary.schema.json`
- `schemas/forensic-event-envelope.schema.json`
- `schemas/runtime-contract.schema.json`

## Governing question

Does this control surface preserve bounded runtime governance, or is it quietly trying to become broader authority?