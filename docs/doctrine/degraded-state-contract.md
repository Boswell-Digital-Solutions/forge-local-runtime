# Degraded-State Contract — Forge Local Runtime

## Purpose

This document defines the runtime-wide rules for truthful degraded-state reporting.

## Rule

A degraded state must be specific enough to preserve operational truth.

The runtime must not flatten all reduced-trust or reduced-capability states into a single vague degraded label when subtype truth is available.

## Required posture

Where applicable, reduced-state reporting should distinguish among conditions such as:

- stale
- partial_success
- unavailable_dependency_block
- degraded_pre_start
- degraded_in_flight
- degraded_fallback_equivalent
- degraded_fallback_limited
- degraded_partial
- migration_blocked
- restore_constrained
- integrity_warning
- integrity_failed
- extraction_incomplete
- re_prep_required
- admitted_not_started
- waiting_explicit_approval
- completed_with_constraints

## Truthfulness classes

The runtime should prefer `specific` truthfulness when a concrete subtype is known.

Only use bounded approximation posture when the service cannot yet safely determine a more exact subtype.

## Schema alignment

Degraded-state reporting should align with:

- `schemas/degraded-state.schema.json`
- `schemas/service-status.schema.json`

If `state = degraded`, a `degraded_subtype` must be supplied in the shared service-status envelope.

## Service posture

### DF Local Foundation
Should distinguish migration, restore, integrity, and readiness issues rather than collapsing all substrate trouble into unavailable.

### NeuronForge Local
Should distinguish fallback equivalence, fallback limitation, in-flight degradation, dependency block, and partial-success conditions.

### Cortex
Should distinguish extraction incompleteness, stale artifacts, integrity failure, and re-prep required posture where applicable.

### FA Local
Should distinguish pre-start denial-adjacent constraints, in-flight degradation, waiting approval, review-required posture, completed-with-constraints, and dependency blocks.

## Governing question

Does the reported degraded state preserve what an operator or consuming application actually needs to know about runtime trust and capability reduction?