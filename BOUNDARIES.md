# BOUNDARIES.md — Forge Local Runtime

## Purpose

This document defines ownership, non-ownership, forbidden drift patterns, and split-trigger posture across the Forge local runtime layer.

## Runtime authority rule

No service inside Forge Local Runtime may silently become product authority.

Services may:

- support
- validate
- prepare
- package
- execute under contract
- report readiness, denial, and degradation

Services may not silently:

- decide canonical business truth
- auto-promote inferred outputs into authority
- redefine app policy by convenience
- collapse candidate output into accepted truth
- become a hidden product backend by accretion
- convert diagnostics into surveillance power

## Service boundaries

### DF Local Foundation

#### Owns
- local database lifecycle
- migrations
- backup / restore / export doctrine
- app registration conventions
- readiness and health state
- bounded recovery and integrity support

#### Does not own
- app business truth
- domain workflow logic
- agent execution logic
- file-intelligence semantics
- shared hidden business logic

### NeuronForge Local

#### Owns
- local inference routing
- bounded task-contract execution
- model/profile routing
- candidate production
- truthful degraded inference status
- trust-surface visibility for inference routes

#### Does not own
- final business authority
- hidden autonomous action loops
- unbounded memory claims
- file-intelligence ownership
- governed execution across all services

### Cortex

#### Owns
- local intake
- syntax-level extraction
- extraction provenance and completeness signaling
- indexing preparation
- retrieval preparation
- packaging handoff support
- privacy-preserving operational diagnostics for its own surfaces

#### Does not own
- semantic interpretation
- model lifecycle authority
- general execution routing
- canonical business truth
- downstream workflow control
- raw-content surveillance by default

### FA Local

#### Owns
- trusted execution request intake
- request validation
- requester trust resolution
- policy-gated execution
- capability admission checks
- bounded execution-plan validation
- execution coordination across approved local routes
- truthful execution-state reporting
- bounded forensic event generation under minimization rules

#### Does not own
- app business semantics
- durable semantic memory
- file intelligence ownership
- inference authority
- hidden persistence authority
- open-ended planning
- hidden surveillance

### Bellows

Admitted as the fifth governed local service per ADR 0010, scoped to audio capture and
device-level audio transport only.

#### Owns
- audio capture and microphone/speaker device control
- audio device readiness
- voice-activity (VAD) segmentation
- duplex (capture/playback) arbitration
- device-level playback transport of an already-produced, hash-validated audio asset
- capture and playback receipts (audio by ref + hash)
- visible recording-state signaling

#### Does not own
- audio generation / TTS (NeuroForge audiobook router)
- transcription or interpretation of captured audio (NeuronForge ASR/text lanes)
- playback UX, voice selection, or audio-asset acceptance (AuthorForge)
- always-listening, wake-word, or continuous background capture
- canonical business truth

## Forbidden drift patterns

The project must explicitly resist:

- DF Local Foundation becoming shared business logic
- NeuronForge Local becoming authority rather than candidate producer
- Cortex drifting into semantics, workflow control, or retrieval-policy authority
- Cortex observation drifting into broad always-on surveillance
- FA Local drifting into open-ended autonomy or stealth orchestration monolith behavior
- Bellows drifting into always-listening, wake-word, or secret-listening capture
- Bellows absorbing audio generation, transcription, or playback UX from its owners
- diagnostics becoming content inspection tooling
- service UIs becoming parallel application identities
- convenience coupling replacing explicit contracts
- fake local/cloud symmetry justifying unnecessary subsystems

## Split-trigger rule

A new subsystem should not be created for symmetry alone.

A split becomes justified only when a concern has:

- distinct ownership
- distinct failure posture
- distinct schema/control language
- distinct observability requirements
- repeated cross-service reuse
- real anti-drift value

## Cloud handoff rule

Cloud services may extend local capability.
They may not redefine local minimum constitutional responsibility.

## Visibility rule

All five services remain service-only runtime systems.
They are never peer products beside AuthorForge, VibeForge, or future Forge applications.