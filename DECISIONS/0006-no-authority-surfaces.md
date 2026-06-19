# ADR 0006 — No Authority Surfaces

## Status
Accepted

## Context

The local runtime includes services that prepare, validate, execute, persist, and report.

Those roles can accidentally accumulate authority if candidate outputs, diagnostics, coordination functions, or persistence layers are allowed to become canonical decision surfaces.

## Decision

Forge Local Runtime must not create hidden authority surfaces.

No governed service may silently become the final authority for:

- semantic interpretation
- business truth
- workflow truth
- autonomous decision loops
- inferred acceptance
- silent candidate promotion

Authority must remain explicit, externalized, and intentionally assigned.

## Consequences

- Candidate outputs remain candidates until explicitly promoted elsewhere.
- Service coordination does not equal service authority.
- Runtime artifacts must distinguish support, execution, reporting, and authority.
- New abstractions must be rejected if they imply hidden authority accumulation.