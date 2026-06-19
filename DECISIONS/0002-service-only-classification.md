# ADR 0002 — Service-Only Classification

## Status
Accepted

## Context

The four local runtime systems governed by Forge Local Runtime are internal service layers:

- DF Local Foundation
- NeuronForge Local
- Cortex
- FA Local

These systems support Forge applications, but they are not peer products or destination experiences.

Without explicit classification, local services can drift into parallel app identities, hidden workflow surfaces, or pseudo-products that confuse authority and ownership boundaries.

## Decision

All four governed local runtime systems are classified as service-only internal runtime systems.

They may be surfaced through consuming applications as bounded embedded capabilities, diagnostics, or review surfaces, but they must not be framed or implemented as standalone peer products by default.

## Consequences

- The runtime layer stays subordinate to consuming applications.
- Visibility may exist without product identity drift.
- UX surfaces for these systems must remain bounded and role-specific.
- Architectural planning must treat the runtime as service substrate, not as an app portfolio.