# ARCHITECTURE.md — Forge Local Runtime

## Architectural purpose

Forge Local Runtime defines the governed local service substrate used by Forge applications.

It is the authority layer above five separate service domains:

- DF Local Foundation
- NeuronForge Local
- Cortex
- FA Local
- Bellows

## Service interaction model

### DF Local Foundation
Provides bounded local substrate mechanics:

- registration
- persistence lifecycle
- readiness support
- migrations
- backup / restore / export support
- bounded integrity and recovery support

### NeuronForge Local
Provides bounded local inference and candidate production:

- task-contract execution
- model/profile routing
- candidate artifact production
- degraded inference truth

### Cortex
Provides bounded local file intelligence and retrieval-preparation support:

- intake
- syntax-level extraction
- extraction provenance
- indexing preparation
- retrieval preparation
- packaging and handoff support
- bounded operational truth

### FA Local
Provides bounded governed execution across approved local routes:

- trusted request intake
- requester trust resolution
- policy evaluation
- capability admission checks
- bounded execution-plan validation
- execution coordination
- truthful denial / degraded / partial / completed state reporting

### Bellows
Provides bounded local audio capture and device-level transport (ADR 0010):

- audio capture and device readiness
- VAD segmentation
- duplex arbitration
- device-level playback transport of already-produced, hash-validated assets
- capture / playback receipts by ref + hash
- visible recording-state signaling

## Cross-service interpretation rule

- DF Local may persist bounded runtime artifacts; it must not become workflow or semantic authority.
- NeuronForge Local may produce candidates; it must not silently promote them into truth.
- Cortex may prepare structure; it must not assign meaning.
- FA Local may execute under policy; it must not absorb semantics or become the hidden planner.
- Bellows may capture and play audio at the device seam; it must not generate, transcribe, or own playback UX, and must never listen silently or continuously.

## Local versus cloud boundary

The local runtime must remain meaningful without cloud.

Cloud services may amplify:

- research depth
- connector breadth
- async workflow scale
- larger orchestration surfaces
- broader memory/sync patterns

But cloud services must not redefine the minimum local baseline.

## Runtime control model

The runtime layer must define shared posture for:

- readiness
- degraded state
- denied state
- stale state
- partial-success state
- handoff envelope status
- requester trust posture
- privacy-preserving diagnostics
- forensic minimization

## Service-only visibility rule

The five governed local services may be visible only through consuming application surfaces such as:

- application HUD status
- embedded diagnostics
- bounded embedded controls
- bounded review/approval surfaces where justified

They must not become separate destination products or parallel workflow applications.

## Anti-drift architecture rule

This repository exists to stabilize:

- ownership lines
- non-ownership lines
- cross-service contracts
- handoff rules
- schema posture
- observability limits

It must not centralize implementation authority by convenience.