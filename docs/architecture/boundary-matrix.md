# Boundary Matrix — Forge Local Runtime

## Purpose

This matrix is the primary anti-drift artifact for the Forge Local Runtime repository.

It exists to make ownership, non-ownership, local baseline requirements, cloud augmentation posture, authority limits, privacy sensitivity, degraded behavior, and split-trigger relevance explicit across the four governed local runtime services.

This matrix should be updated whenever a governed service gains a new capability, loses a capability, or changes its denial, degraded, observability, or authority posture.

## Reading rule

Every row must be read in full.

A capability is not governed correctly unless all of the following are explicit:

- who owns it
- who does not own it
- whether it is part of the required local baseline
- whether cloud augmentation is allowed
- whether it implies authority
- what privacy sensitivity it introduces
- how degraded truth should surface
- whether the capability creates split-trigger pressure

## Matrix

| Service | Capability | Owned by | Explicitly not owned by | Local baseline required | Cloud augmentation available | Authority status | Privacy sensitivity | Degraded behavior | Split-trigger relevance |
|---|---|---|---|---|---|---|---|---|---|
| DF Local Foundation | local database lifecycle | DF Local Foundation | NeuronForge Local, Cortex, FA Local, consuming apps as shared substrate authority | yes | yes | substrate authority only, not semantic or workflow authority | medium to high | migration_blocked, integrity_warning, unavailable, restore_constrained | medium |
| DF Local Foundation | migrations and migration posture | DF Local Foundation | NeuronForge Local, Cortex, FA Local | yes | limited | substrate control only, not app/business authority | medium | migration_blocked, degraded_pre_start, unavailable | low |
| DF Local Foundation | backup / restore / export support | DF Local Foundation | Cortex, NeuronForge Local, FA Local as primary owners | yes | yes | operational substrate authority only | high | restore_constrained, partial_success, integrity_warning, unavailable | medium |
| DF Local Foundation | app / service registration support | DF Local Foundation | Cortex, NeuronForge Local, FA Local as registration authority for all services | yes | limited | registration support only, not semantic identity authority | low to medium | partial_success, stale, unavailable | low |
| DF Local Foundation | readiness and substrate state support | DF Local Foundation | Cortex, NeuronForge Local, FA Local as substrate readiness owners | yes | limited | bounded substrate reporting authority only | low | degraded, stale, unavailable | low |
| DF Local Foundation | local runtime artifact persistence support | DF Local Foundation | NeuronForge Local as final inference authority, Cortex as semantic file authority, FA Local as policy authority | yes | yes | storage support only, not truth authority | high | stale, partial_success, integrity_warning | medium |
| NeuronForge Local | local model routing and profile selection | NeuronForge Local | DF Local Foundation, Cortex, FA Local | yes | yes | bounded inference-route authority only | medium | degraded_fallback_equivalent, degraded_fallback_limited, unavailable_dependency_block | medium |
| NeuronForge Local | task-contract execution for local inference | NeuronForge Local | DF Local Foundation, Cortex, FA Local as inference owner | yes | yes | candidate-production authority only, not final decision authority | high | degraded_pre_start, degraded_in_flight, partial_success, unavailable_dependency_block | high |
| NeuronForge Local | candidate output production | NeuronForge Local | DF Local Foundation, Cortex, FA Local, consuming apps as automatic acceptance authorities | yes | yes | candidate-only, never silent truth authority | high | degraded_fallback_limited, partial_success, stale | high |
| NeuronForge Local | route-class posture and inference readiness | NeuronForge Local | DF Local Foundation, Cortex, FA Local | yes | yes | bounded local inference reporting authority only | low to medium | degraded, stale, unavailable | low |
| NeuronForge Local | contract-shaped output discipline | NeuronForge Local | Cortex, DF Local Foundation, FA Local | yes | yes | structure/contract authority for its outputs only | medium | partial_success, degraded_in_flight | medium |
| Cortex | local file intake | Cortex | DF Local Foundation as syntax owner, NeuronForge Local, FA Local | yes | yes | intake authority only within syntax/file boundary | high | partial_success, integrity_failed, unavailable | medium |
| Cortex | syntax-level extraction | Cortex | NeuronForge Local, FA Local, DF Local Foundation as extraction owner | yes | yes | syntax authority only, never semantic authority | high | extraction_incomplete, partial_success, stale, integrity_failed | high |
| Cortex | structure detection | Cortex | NeuronForge Local, FA Local, DF Local Foundation | yes | yes | syntax/structure authority only | high | extraction_incomplete, degraded, stale | medium |
| Cortex | extraction provenance and completeness signaling | Cortex | NeuronForge Local, FA Local, DF Local Foundation | yes | yes | bounded provenance/reporting authority only | medium | extraction_incomplete, stale, partial_success | medium |
| Cortex | retrieval-preparation support | Cortex | NeuronForge Local as inference authority, FA Local as execution authority | yes | yes | retrieval infrastructure support only, not retrieval authority | medium to high | stale, partial_success, degraded | high |
| Cortex | packaging and bounded handoff support | Cortex | FA Local as execution authority, NeuronForge Local as semantic authority | yes | yes | handoff-packaging authority only | medium | re_prep_required, integrity_failed, stale, rejected_reason_code | high |
| Cortex | privacy-preserving diagnostics for bounded surfaces | Cortex | all services as broad surveillance authority | yes | limited | diagnostics authority only for its owned surfaces | high | degraded, stale, unavailable | high |
| FA Local | execution request intake | FA Local | Cortex, NeuronForge Local, DF Local Foundation as execution-intake owners | yes | yes | intake authority only within execution boundary | medium to high | denied, review_required, unavailable_dependency_block | medium |
| FA Local | requester identity / requester-class resolution | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | trust-resolution authority only within execution boundary | medium | denied, review_required, degraded_pre_start | medium |
| FA Local | requester trust posture evaluation | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | trust-gating authority only, not semantic authority | medium | denied, review_required, waiting_explicit_approval | medium |
| FA Local | policy artifact enforcement before side effects | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | execution-policy authority only within approved boundary | high | denied, review_required, admitted_not_started | high |
| FA Local | capability admission checks | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | capability-admission authority only | medium | denied, review_required, admitted_not_started | high |
| FA Local | bounded execution-plan validation | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | bounded execution validation authority only | medium to high | denied, review_required, degraded_pre_start | high |
| FA Local | approval posture ladder enforcement | FA Local | Cortex, NeuronForge Local, DF Local Foundation | yes | limited | bounded execution approval authority only | medium | denied, waiting_explicit_approval, review_required | high |
| FA Local | controlled execution coordination for approved local routes | FA Local | Cortex as workflow authority, NeuronForge Local as execution governor, DF Local Foundation | yes | yes | execution coordination authority only, never open-ended orchestration authority | high | degraded_in_flight, partial_success, unavailable_dependency_block, completed_with_constraints | high |
| FA Local | truthful denial / degraded / partial-success reporting | FA Local | Cortex, NeuronForge Local, DF Local Foundation as execution-state owners | yes | limited | execution-state reporting authority only | medium | denied, degraded_pre_start, degraded_in_flight, partial_success, completed_with_constraints | medium |
| FA Local | review-package handoff support | FA Local | Cortex as review authority, NeuronForge Local as review authority, DF Local Foundation | yes | yes | bounded handoff authority only | medium to high | review_required, waiting_explicit_approval, re_prep_required | medium |
| FA Local | bounded forensic event generation under minimization rules | FA Local | Cortex, NeuronForge Local, DF Local Foundation as broad forensic-content owners | yes | yes | forensic event authority only within minimized execution boundary | high | partial_success, degraded_in_flight, unavailable_dependency_block | high |

## Matrix interpretation notes

### Local baseline required

A value of `yes` means the capability is part of the constitutional minimum local runtime and cannot be treated as optional cloud-only functionality.

A value of `limited` or `yes` under cloud augmentation means cloud systems may extend or amplify the capability, but may not redefine its local constitutional boundary.

### Authority status

Authority in this matrix is always bounded.

A service may hold authority for its own narrow control surface without becoming the authority for application truth, semantic truth, workflow truth, or silent candidate promotion.

### Privacy sensitivity

Privacy sensitivity indicates how easily a capability could become a content-exposure or surveillance risk if observability is implemented carelessly.

High-sensitivity rows require especially strict minimization, redaction, retention, and default-denied observation posture.

### Degraded behavior

Degraded behavior must remain truthful and specific.

Rows should never collapse all reduced-trust states into a single vague unhealthy condition when more accurate terms are available.

### Split-trigger relevance

Split-trigger relevance indicates how likely the capability is to justify future separation if it develops a materially distinct:

- control language
- trust model
- failure posture
- schema posture
- observability regime
- anti-drift need

High relevance does not mean split immediately.
It means pay attention to drift pressure.

## Boundary maintenance rules

The matrix must be updated when any of the following occur:

- a new governed capability is introduced
- a capability changes ownership
- a capability gains new denial or degraded states
- a capability changes privacy posture
- a capability starts implying new authority pressure
- a service begins showing split-trigger signals

## Anti-drift review questions

Use these review questions before accepting boundary changes:

1. Does this capability create semantic authority where only syntax, substrate, candidate, or execution authority was intended?
2. Does this capability broaden observability into content inspection or surveillance?
3. Does this capability make a service look like a hidden orchestrator or stealth monolith?
4. Does this capability silently transfer ownership from one service to another?
5. Does this capability create a new control language that deserves a split review?
6. Does this capability weaken the meaningful local baseline by assuming cloud dependence?