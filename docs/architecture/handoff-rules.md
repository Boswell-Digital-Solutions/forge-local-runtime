# Handoff Rules — Forge Local Runtime

## Purpose

This document defines the rules for bounded cross-service handoff inside the Forge local runtime.

## Rule

Cross-service handoff exists to transfer bounded artifacts and bounded status, not to create hidden orchestration.

## Required posture

A handoff should preserve:

- source service identity
- target service identity
- handoff id
- bounded status
- bounded reason code when rejected
- operator-visible message
- timestamp
- redaction posture

## Reverse signaling rule

Reverse signaling must remain minimal.

Allowed posture includes statuses such as:

- accepted
- rejected_reason_code
- re_prep_required
- stale
- integrity_failed

Reverse signaling must not expand into open-ended downstream workflow control.

## Schema alignment

Handoff posture should align with:

- `schemas/handoff-envelope.schema.json`
- `schemas/runtime-contract.schema.json`

## Service examples

### Cortex → NeuronForge Local
Cortex may hand off syntax-level artifacts prepared for downstream consumption.
NeuronForge Local may accept or reject based on contract and readiness posture.

### FA Local → Review surface
FA Local may emit a review-required result or bounded review package.
That does not make FA Local the long-term review authority.

## Governing question

Does this handoff transfer only the bounded artifact and status needed, or is it trying to smuggle workflow authority?