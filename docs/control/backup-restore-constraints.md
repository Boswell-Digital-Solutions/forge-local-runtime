# Backup Restore Constraints — Forge Local Runtime

## Purpose

This document defines the bounded backup and restore constraints for Forge Local Runtime.

## Rule

Backup and restore support exists to preserve substrate integrity and recoverability, not to justify broad authority or content duplication.

## Primary owner

DF Local Foundation is the primary owner of backup, restore, and export support posture in the local runtime.

Other services may participate only within their owned boundaries.

## Constraints

Backup and restore behavior must preserve:

- integrity verification
- bounded ownership
- minimized cross-service assumptions
- truthful degraded and constrained-state reporting
- privacy-preserving handling of sensitive artifacts

## Restore-constrained posture

A restore path should report constrained or degraded posture when:

- integrity cannot be fully verified
- schema expectations are mismatched
- migrations are required but not safely satisfied
- dependent service artifacts are stale or incomplete
- restore would broaden authority boundaries by convenience

## Anti-drift rule

Backup and restore support must not become:

- a hidden semantic merge engine
- a broad cross-service truth reconciler
- a convenience layer for bypassing contract and boundary discipline

## Schema alignment

Backup and restore constraints should surface through:

- `schemas/service-status.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/forensic-event-envelope.schema.json`

## Governing question

Does the restore preserve substrate integrity and bounded ownership, or is it trying to reconstruct more authority than the runtime actually owns?