# Runtime Governance Primitives — Forge Local Runtime

## Purpose

This document defines the reusable governance primitives that appear across the runtime layer.

## Core primitives

The Forge local runtime uses the following primitives across service boundaries:

- ownership
- non-ownership
- readiness
- denial
- degraded truth
- requester class
- capability admission
- policy posture
- handoff envelope
- review package
- correlation id
- plan hash
- retention class
- privacy scope
- redaction status

## Why primitives matter

Without common primitives, each service invents incompatible control language.
That leads to hidden authority drift, inconsistent operator surfaces, and brittle integrations.

## Primitive definitions

### Ownership
The bounded domain a service is constitutionally allowed to control.

### Non-ownership
The explicit list of domains a service must not silently absorb.

### Readiness
A bounded statement of whether the service can perform its owned role now.

### Denial
An explicit statement that a requested action, route, artifact, or capability cannot proceed under current contract, policy, safety, or trust posture.

### Degraded truth
A truthful statement that service capability is reduced or constrained, with subtype detail where possible.

### Requester class
The bounded trust-facing identity category of the caller or initiating surface.

### Capability admission
The rule that a route or tool is not usable just because it exists; it must be explicitly admitted for the current posture.

### Policy posture
The statement of whether policy is not required, present, missing, or review-gated.

### Handoff envelope
The bounded package or reverse signal used to transfer artifacts or status between governed services without hidden orchestration expansion.

### Review package
A bounded artifact emitted when automated execution cannot proceed directly and operator review is required.

### Correlation id
A shared identifier used to trace related runtime events without broad content exposure.

### Plan hash
A fingerprint used to bind execution or review posture to a specific bounded plan artifact.

### Retention class
A bounded retention label governing how long minimized records or forensic envelopes should survive.

### Privacy scope
The permitted observational boundary for a diagnostic or event surface.

### Redaction status
The explicit statement of whether sensitive details were excluded or redacted.

## Schema alignment

These primitives appear across:

- `schemas/service-status.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/handoff-envelope.schema.json`
- `schemas/readiness-summary.schema.json`
- `schemas/forensic-event-envelope.schema.json`
- `schemas/runtime-contract.schema.json`