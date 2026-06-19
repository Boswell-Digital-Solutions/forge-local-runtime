# ADR 0004 — Cortex Boundary

## Status
Accepted

## Context

Cortex is the local file-intelligence and retrieval-preparation boundary in the runtime layer.

Its value comes from disciplined scope:
intake, syntax-level extraction, structure, packaging, retrieval preparation, and truthful operational reporting.

The major risk is drift into semantic interpretation, workflow control, generic ETL, or broad content-observation power.

## Decision

Cortex is constrained to syntax-before-semantics file intelligence and retrieval-preparation support.

Cortex may extract structure, package handoff artifacts, and report bounded operational truth about its own surfaces.
Cortex must not become semantic authority, workflow authority, generic ETL infrastructure, or surveillance-by-default diagnostics infrastructure.

## Consequences

- Syntax and semantics remain constitutionally separated.
- Cortex may support downstream systems without controlling them.
- Observation and diagnostics must remain privacy-preserving and explicitly scoped.
- Reverse signaling from downstream systems must remain minimal and anti-orchestration in posture.