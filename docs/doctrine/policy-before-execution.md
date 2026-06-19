# Policy Before Execution — Forge Local Runtime

## Purpose

This document formalizes the execution doctrine that policy posture must be resolved before side-effect-capable execution proceeds.

## Rule

No side-effect-capable runtime path should execute without resolved policy posture.

If policy is required and missing, execution must deny or route to review rather than continue.

## Primary implication for FA Local

FA Local must treat policy posture as a first-class gate alongside:

- requester class
- capability admission
- bounded-plan validation
- approval posture

## Required execution posture

Execution governance should preserve explicit statements for:

- requester class
- policy posture
- capability id
- plan hash where applicable
- approval posture
- denial or degraded state when execution cannot proceed normally

## Review-path implication

When direct execution is not permitted, the runtime may emit a bounded review package or review-required result.

That handoff exists to preserve human review and fail-closed posture.
It must not become hidden autonomous planning.

## Schema alignment

This doctrine should align with:

- `schemas/denial-state.schema.json`
- `schemas/service-status.schema.json`
- `schemas/runtime-contract.schema.json`
- `schemas/forensic-event-envelope.schema.json`

## Anti-patterns

The following are disallowed:

- executing because the route exists even though policy is unresolved
- treating trusted origin as a substitute for capability admission
- bypassing plan validation because the action seems small
- converting review-required posture into silent execution retry

## Governing question

Has policy posture been resolved before the runtime reaches a side-effect-capable path?