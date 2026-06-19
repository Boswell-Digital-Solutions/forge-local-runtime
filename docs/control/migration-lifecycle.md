# Migration Lifecycle — Forge Local Runtime

## Purpose

This document defines the migration posture for the Forge local runtime substrate.

## Rule

Migrations are substrate lifecycle events, not opportunities to broaden ownership or quietly reshape application truth.

## Primary owner

DF Local Foundation is the primary owner of migration posture within Forge Local Runtime.

## Migration stages

Migration posture should distinguish at least:

- pending
- in_progress
- completed
- migration_blocked
- rollback_required
- completed_with_constraints

Exact operational implementation may vary, but substrate truth must remain explicit.

## Migration constraints

Migration operations must preserve:

- bounded substrate ownership
- integrity verification
- explicit failure/degraded truth
- privacy-preserving observability
- non-expansion into semantic or workflow authority

## Failure posture

When migrations cannot safely proceed, the runtime should report blocked or constrained posture rather than pretending readiness.

## Schema alignment

Migration lifecycle posture should surface through:

- `schemas/service-status.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/readiness-summary.schema.json`
- `schemas/forensic-event-envelope.schema.json`

## Governing question

Is the migration reporting truthful about substrate readiness and integrity, or is it hiding a blocked state behind generic availability language?