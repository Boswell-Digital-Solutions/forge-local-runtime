# Readiness Model — Forge Local Runtime

## Purpose

This document defines how readiness should be represented across the four governed local runtime services.

## Rule

Readiness is a bounded statement about whether a service can currently perform its owned role under present constraints.

Readiness is not a vague health color.

## Shared readiness classes

The runtime uses these readiness classes:

- ready
- ready_with_constraints
- degraded
- not_ready

## Readiness factors

Readiness may be affected by:

- dependency availability
- migration posture
- integrity posture
- policy posture
- approval posture
- route availability
- capacity limits
- stale artifacts
- review requirements

## Schema alignment

Readiness posture should align with:

- `schemas/readiness-summary.schema.json`
- `schemas/service-status.schema.json`

## Service-specific examples

### DF Local Foundation
Ready if substrate lifecycle and integrity posture support owned functions.
Not ready if migration or restore posture blocks safe operation.

### NeuronForge Local
Ready if local inference routes are available within contract posture.
Ready with constraints if only fallback routes remain.

### Cortex
Ready if intake, extraction, integrity, and packaging posture are sufficient.
Degraded if extraction is incomplete or stale.

### FA Local
Ready if requester trust, policy posture, capability admission, and bounded-plan posture allow owned execution paths.
Not ready if required trust or policy gates are unresolved.

## Governing question

Does the readiness summary tell the operator whether the service can perform its owned role now, and under what constraints?