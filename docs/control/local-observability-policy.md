# Local Observability Policy — Forge Local Runtime

## Purpose

This document turns privacy-preserving observability doctrine into operational policy.

## Policy

All observability inside the Forge local runtime must be:

- scoped
- minimized
- content-sparing
- role-appropriate
- retention-aware

## Default policy rules

1. Raw content capture is prohibited by default.
2. Broad watchers are disabled by default.
3. Logs and state surfaces should prefer labels, counts, hashes, ids, and summaries.
4. Service-specific diagnostics must remain inside owned boundaries.
5. Observation scope expansions require explicit doctrine review.

## Minimum required visibility

The runtime must still surface enough truth for:

- readiness
- degraded states
- denied states
- handoff rejection
- integrity failures
- review-required posture
- bounded forensic accountability

## Schema alignment

Operational policy should align with:

- `schemas/service-status.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/forensic-event-envelope.schema.json`
- `schemas/handoff-envelope.schema.json`

## Governing question

Is the observable signal the minimum needed to preserve operational truth?