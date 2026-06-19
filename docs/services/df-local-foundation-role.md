# DF Local Foundation — Service Role

## Role

DF Local Foundation is the bounded local data and control substrate for the Forge local runtime layer.

It exists to provide local substrate mechanics that multiple consuming applications and governed local runtime services can rely on without turning DF Local Foundation into application authority.

## Owns

DF Local Foundation owns:

- local database lifecycle
- migrations and migration posture
- backup, restore, and export support
- app and service registration support
- readiness and state support for substrate concerns
- bounded integrity and recovery support
- local storage conventions for governed runtime artifacts
- substrate-level retention and maintenance support where explicitly assigned

## Explicitly does not own

DF Local Foundation does not own:

- application business truth
- domain semantics
- workflow authority
- file-intelligence authority
- inference authority
- execution authority
- durable semantic memory for applications by default
- hidden cross-app business logic
- product policy authority

## Why the boundary exists

A local substrate is necessary, but it is also a common place for architecture drift.

Without an explicit boundary, substrate layers often accumulate:

- shared business rules
- hidden coordination logic
- semantic interpretation
- workflow routing
- pseudo-platform authority

DF Local Foundation must remain substrate, not silent application control plane.

## Local baseline requirement

DF Local Foundation is part of the constitutional minimum local baseline.

The local runtime is not meaningful without a bounded local substrate for persistence lifecycle, integrity posture, readiness support, and recovery mechanics.

## Cloud augmentation line

Cloud services may augment durability, synchronization, federation, multi-device posture, or remote evidence/storage workflows.

Cloud augmentation does not remove the requirement for a meaningful local substrate baseline.

## Authority status

DF Local Foundation is not an authority layer for application truth.

It may maintain runtime artifacts, state summaries, migration records, and bounded operational metadata, but that does not make it the authority for semantic or workflow meaning.

## Privacy sensitivity

DF Local Foundation may touch sensitive local artifacts because it supports storage and recovery surfaces.

It must therefore follow privacy-preserving observability and minimization posture.
Diagnostics and forensic surfaces must avoid unnecessary content capture.

## Readiness and degraded behavior

DF Local Foundation must report substrate truthfully, including states such as:

- ready
- degraded
- stale where applicable
- migration blocked
- restore constrained
- integrity warning
- unavailable

It must not flatten substrate problems into vague healthy/unhealthy language when more truthful reduced-state reporting is available.

## Split-trigger relevance

A split away from DF Local Foundation is justified only if a new concern demonstrates distinct:

- ownership
- schema/control language
- failure posture
- observability needs
- anti-drift value

No split should occur for naming symmetry or completeness theater alone.

## Interaction posture with other services

### With NeuronForge Local
DF Local Foundation may provide bounded persistence and runtime artifact support for local inference surfaces.
It does not own inference routes or candidate judgment.

### With Cortex
DF Local Foundation may support bounded storage/indexing substrate needs.
It does not own extraction semantics or retrieval-preparation meaning.

### With FA Local
DF Local Foundation may support execution-adjacent persistence, records, and bounded recovery surfaces.
It does not own requester trust, policy evaluation, or execution authority.

## Governing rule

DF Local Foundation must remain a substrate role with explicit non-ownership lines.
If a proposed feature implies semantic, workflow, or execution authority drift, it should be rejected or split.