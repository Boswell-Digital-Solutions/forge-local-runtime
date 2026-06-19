# Requester Trust Model — Forge Local Runtime

## Purpose

This document defines the requester-trust posture used for governed execution and related runtime decisions.

## Rule

Requests are not uniformly trusted.

Requester posture must be resolved explicitly before trust-gated runtime behavior proceeds.

## Shared requester classes

The runtime supports at least:

- trusted_operator
- trusted_application_surface
- constrained_internal_caller
- unknown
- untrusted

## Core implications

### trusted_operator
May be eligible for broader review and approval paths, but not for bypassing constitutional constraints.

### trusted_application_surface
May initiate approved bounded runtime actions, but not hidden policy bypass.

### constrained_internal_caller
May operate within narrow machine-governed limits only.

### unknown
Fails closed by default where trust-gated behavior matters.

### untrusted
Denied from trust-gated paths unless explicitly mediated through allowed review posture.

## Schema alignment

Requester trust posture should align with:

- `schemas/runtime-contract.schema.json`
- `schemas/forensic-event-envelope.schema.json`

## Primary service implication

This model is especially load-bearing for FA Local, but it may also inform related runtime handoff and observability posture.

## Governing question

Has requester posture been resolved explicitly, or is the runtime assuming trust that was never actually granted?