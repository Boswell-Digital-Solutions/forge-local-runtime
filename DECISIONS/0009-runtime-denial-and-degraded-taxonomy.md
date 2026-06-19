# ADR 0009 — Runtime Denial and Degraded Taxonomy

## Status
Accepted

## Context

The runtime layer needs a shared language for denial, degraded operation, stale outputs, partial success, unavailable dependencies, and other reduced-trust states.

Without a shared taxonomy, each service will invent incompatible language and consuming applications will not be able to interpret operational truth consistently.

## Decision

Forge Local Runtime defines a shared runtime-wide denial and degraded-state taxonomy.

This taxonomy must be explicit, reusable, and machine-testable through shared schemas.
It must preserve subtype truth rather than flattening all reduced states into a single generic degraded label.

## Consequences

- Cross-service operational truth becomes consistent.
- Applications can interpret runtime state without service-specific guesswork.
- Denial and degraded schemas become first-class control surfaces.
- Future enum expansion should be governed and reviewed rather than improvised.