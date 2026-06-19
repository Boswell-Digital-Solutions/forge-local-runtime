# Local Runtime Principles — Forge Local Runtime

## Purpose

This document defines the constitutional principles that govern the Forge local runtime layer.

These principles apply across:

- DF Local Foundation
- NeuronForge Local
- Cortex
- FA Local

## Principle 1 — Local baseline must be meaningful

The local runtime must remain useful without cloud access.

Local services are not placeholders for eventual cloud replacement.
They are a real constitutional baseline.

## Principle 2 — Service-only classification is mandatory

The four governed runtime systems are service-only internal systems.

They may surface through consuming applications as bounded embedded capabilities or review surfaces, but they are not peer products.

## Principle 3 — Boundaries outrank convenience

No service may absorb additional responsibility merely because it is nearby, already running, or easy to extend.

Ownership and non-ownership lines outrank implementation convenience.

## Principle 4 — Support is not authority

Substrate support, candidate production, syntax extraction, diagnostics, packaging, coordination, or execution reporting do not equal final semantic or business authority.

Authority must remain explicit.

## Principle 5 — Fail closed where trust or side effects matter

When policy, requester trust, capability admission, integrity, or bounded-plan posture is insufficient, the runtime must narrow, deny, or route to review rather than continue optimistically.

## Principle 6 — Privacy-preserving observability is required

Operational truth is required.
Surveillance-by-default is forbidden.

Observability must prefer metadata, counts, hashes, classifications, bounded summaries, and minimized event envelopes over raw content capture.

## Principle 7 — Truthful reduced-state reporting is mandatory

The runtime must distinguish denied, degraded, stale, partial-success, unavailable, review-required, and similar states explicitly rather than flattening them into vague generic failure language.

## Principle 8 — Cloud augmentation is additive only

Cloud services may amplify local breadth, scale, or depth.
They must not redefine the constitutional minimum responsibilities of the local runtime.

## Principle 9 — Anti-drift review is part of normal governance

Every new capability, schema, control surface, or integration should be reviewed for:

- hidden authority drift
- hidden orchestration drift
- privacy collapse
- fake symmetry
- local baseline erosion

## Principle 10 — This repository is constitutional infrastructure

Forge Local Runtime is a governance-and-contracts authority repository.

It is not a destination implementation monolith, app backend, or hidden product-control repo.