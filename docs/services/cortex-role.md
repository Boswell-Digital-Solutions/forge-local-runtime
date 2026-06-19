# Cortex — Service Role

## Role

Cortex is the bounded local file-intelligence and retrieval-preparation boundary for the Forge local runtime layer.

It exists to transform local files and related artifacts into syntax-level, provenance-aware, handoff-ready structures without becoming a semantic, orchestration, or surveillance authority.

## Owns

Cortex owns:

- local file intake
- syntax-level extraction
- structure detection
- extraction provenance and completeness signaling
- retrieval-preparation support
- packaging and handoff support
- integrity-aware intake and extraction status
- privacy-preserving diagnostics for its own bounded surfaces
- freshness invalidation and explicit stale signaling where applicable

## Explicitly does not own

Cortex does not own:

- semantic interpretation
- authorial meaning
- thematic judgment
- final retrieval authority
- downstream workflow control
- generic ETL platform behavior
- model lifecycle authority
- open-ended orchestration
- surveillance-by-default observation
- canonical business truth

## Why the boundary exists

File intelligence is a common drift zone.

A service that can read structure often gets pushed toward:

- meaning assignment
- ranking authority
- workflow routing
- broad ingestion ownership
- always-on watch power

The constitutional boundary exists to keep Cortex useful without letting it become silent semantics or invisible orchestration.

## Syntax-before-semantics rule

Cortex is constitutionally bound to syntax-before-semantics posture.

It may identify structure such as sections, headings, metadata fields, tables, chunk boundaries, and extraction completeness posture.

It must not assign semantic meaning, business conclusions, authorial judgment, or downstream action authority as part of its owned role.

## Retrieval posture

Cortex is retrieval infrastructure support, not retrieval authority.

It may prepare artifacts for downstream retrieval and handoff use.
It may not decide what downstream systems should believe, prioritize, or conclude from those artifacts.

## Handoff posture

Cortex may emit bounded handoff packages and receive bounded reverse signaling.

Reverse signaling must remain minimal and anti-orchestration in posture, such as:

- accepted
- rejected_reason_code
- re_prep_required
- stale
- integrity_failed

Cortex must not expand reverse signaling into workflow coordination or downstream authority capture.

## Observation posture

Observation is default-denied unless explicitly enabled and scoped.

Cortex must not become an always-on local surveillance surface.
Operational truth should be delivered through privacy-preserving metrics, status, counts, hashes, scope-limited metadata, and redacted summaries rather than raw content capture.

## Freshness posture

Cortex must prefer explicit invalidation over assumed freshness.

When freshness cannot be established, Cortex should report stale or equivalent truthful state rather than silently presenting old extraction posture as current.

## Privacy sensitivity

Cortex may access highly sensitive local content.

Therefore:

- diagnostics must minimize content exposure
- persistent content capture is prohibited by default
- watch surfaces require explicit scope and doctrine alignment
- forensic posture must remain content-sparing unless explicitly justified

## Readiness and degraded behavior

Cortex should report truthful operational states such as:

- ready
- degraded
- stale
- partial_success
- integrity_failed
- extraction_incomplete
- unavailable

Reduced-state truth must be specific enough for consuming systems to reason about handoff quality without inventing semantics.

## Anti-drift warnings

The following drift moves are constitutionally disallowed unless the architecture is explicitly reworked:

- adding semantic summarization as owned Cortex behavior
- turning Cortex into a workflow router
- turning Cortex into general ETL infrastructure
- broadening reverse signaling into orchestration control
- enabling broad background observation by default
- storing raw file content for diagnostics convenience

## Interaction posture with other services

### With DF Local Foundation
Cortex may rely on bounded substrate support for persistence and state reporting.
That does not transfer semantic or retrieval authority.

### With NeuronForge Local
Cortex may hand off syntax-level packages to NeuronForge Local or other approved downstream systems.
That handoff does not make Cortex the semantic authority and does not make NeuronForge Local retroactively part of Cortex.

### With FA Local
Cortex may participate in approved execution paths when explicitly invoked under policy-governed conditions.
It does not become execution authority, and FA Local does not become syntax authority.

## Governing rule

Cortex must remain a syntax-before-semantics, retrieval-preparation, privacy-preserving file-intelligence boundary.
If a proposal implies semantics, orchestration, ETL drift, or surveillance expansion, it should be rejected or split.