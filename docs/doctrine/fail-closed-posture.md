# Fail-Closed Posture — Forge Local Runtime

## Purpose

This document defines the fail-closed doctrine for the local runtime layer.

## Rule

When trust, policy, integrity, readiness, or bounded-plan requirements are not satisfied, the runtime should narrow, deny, or route to review rather than proceed optimistically.

## Where fail-closed matters most

Fail-closed posture is especially required when:

- side effects are possible
- requester trust is unknown
- policy artifacts are missing
- capability admission is unclear
- integrity checks fail
- freshness cannot be established
- reverse handoff signaling indicates rejection or re-prep need

## Service posture

### DF Local Foundation
Should fail closed on integrity-critical, migration-blocking, and restore-constrained paths rather than pretend substrate readiness.

### NeuronForge Local
Should not silently promote degraded or fallback candidate production into equivalent trust when equivalence is not justified.

### Cortex
Should prefer explicit stale or integrity-failed signaling over assumed freshness or silent package reuse.

### FA Local
Should deny or route to review when requester trust, policy, capability admission, or plan validation posture is insufficient.

## Schema alignment

Fail-closed posture should be visible through shared runtime schemas, including:

- `schemas/service-status.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/handoff-envelope.schema.json`

## Anti-patterns

The following are fail-open anti-patterns:

- silently retrying into a broader authority surface
- substituting candidate output for approved authority
- using stale artifacts without explicit stale marking
- executing on missing policy because the request looks safe
- broadening handoff semantics into hidden orchestration

## Governing question

If the runtime cannot honestly justify continued action, does it stop, narrow, or route to review?