v# ADR 0001 — Project Framing

## Status
Accepted

## Context

Forge Local Runtime needs to exist as a standalone governance-and-contracts authority repository rather than remaining implicit inside broader Forge planning.

The local runtime is already a distinct architecture layer with its own doctrine, trust boundaries, degraded-state posture, handoff rules, and anti-drift requirements.

## Decision

Forge Local Runtime is established as the constitutional and integration authority for the local service substrate of the Forge ecosystem.

It is a governance-first repository, not an implementation sink.

## Consequences

- Runtime doctrine can be stabilized independently of service implementation.
- Boundary lines become easier to test and audit.
- Cross-service control language can be defined once and reused.
- Implementation must not outrun doctrine, decisions, schemas, and anti-drift surfaces.