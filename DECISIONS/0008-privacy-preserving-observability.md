# ADR 0008 — Privacy-Preserving Observability

## Status
Accepted

## Context

The local runtime needs truthful health, readiness, degraded-state, denial, and forensic visibility.

But local systems often have access to sensitive content, prompts, files, intermediate artifacts, or execution context.
A broad observability model would create surveillance power inconsistent with local trust.

## Decision

Forge Local Runtime adopts privacy-preserving observability as a constitutional requirement.

Operational visibility must default to minimized, scoped, and content-sparing posture.
Raw content capture, broad watch surfaces, and persistent inspection by default are prohibited unless explicitly justified and governed.

## Consequences

- Readiness and degraded truth remain available without content collapse.
- Diagnostics should prefer metadata, counts, hashes, classifications, and redacted summaries over raw payloads.
- Forensic events must follow minimization and retention rules.
- Any expansion of observation scope requires explicit doctrine and boundary review.