# ADR 0007 — Split Trigger Policy

## Status
Accepted

## Context

Architectures can become fragmented by symmetry theater, or can become monolithic by refusing to separate genuinely distinct concerns.

Forge Local Runtime needs a disciplined rule for when a new subsystem or shared surface is justified.

## Decision

A split is justified only when a concern demonstrates distinct:

- ownership
- failure posture
- control language
- schema needs
- observability constraints
- anti-drift value
- repeated cross-service reuse

No new subsystem may be created for naming symmetry, aesthetic completeness, or speculative future convenience alone.

## Consequences

- The runtime stays bounded.
- New repos, modules, or services need explicit architectural justification.
- Anti-monolith discipline is preserved without fragmenting into theater.
- Boundary reviews must evaluate whether a proposed split is real or cosmetic.