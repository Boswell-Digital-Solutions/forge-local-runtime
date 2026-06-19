# Four-Service Interaction Model — Forge Local Runtime

## Purpose

This document describes how the four governed local runtime services interact without collapsing ownership boundaries.

## Interaction model

### DF Local Foundation ↔ NeuronForge Local

DF Local Foundation may provide bounded substrate support for persistence, readiness, local artifact handling, and recovery posture related to local inference activity.

NeuronForge Local remains the owner of local inference routing, task-contract execution, and candidate output posture.

DF Local Foundation does not become inference authority.
NeuronForge Local does not become substrate authority.

### DF Local Foundation ↔ Cortex

DF Local Foundation may provide bounded substrate support for intake-adjacent persistence, index-supporting artifact storage, readiness reporting, and lifecycle mechanics.

Cortex remains the owner of syntax-level extraction, retrieval-preparation support, and handoff packaging.

DF Local Foundation does not become file-intelligence authority.
Cortex does not become substrate or workflow authority.

### DF Local Foundation ↔ FA Local

DF Local Foundation may provide bounded persistence and lifecycle support for execution-adjacent records, readiness, and recovery mechanics.

FA Local remains the owner of requester-trust-gated, policy-before-execution local execution control.

DF Local Foundation does not become execution authority.
FA Local does not become storage or substrate authority.

### Cortex ↔ NeuronForge Local

Cortex may hand off syntax-level, provenance-aware, retrieval-preparation artifacts to NeuronForge Local or other approved downstream consumers.

NeuronForge Local may consume those artifacts under explicit task contracts.

Cortex does not assign semantic meaning.
NeuronForge Local does not retroactively make Cortex a semantic authority.

### Cortex ↔ FA Local

FA Local may invoke Cortex-related preparation routes when policy, requester trust, and capability posture allow.

Cortex remains syntax-before-semantics and does not become execution governor.
FA Local remains execution governor and does not become syntax authority.

### NeuronForge Local ↔ FA Local

FA Local may invoke approved NeuronForge Local routes under policy and capability posture.

NeuronForge Local may produce bounded candidate outputs in response to those routes.

FA Local does not become inference authority.
NeuronForge Local does not become execution authority or final decision authority.

## Cross-service invariants

The following must remain true across all interactions:

1. substrate support does not equal semantic or workflow authority
2. candidate production does not equal accepted truth
3. syntax extraction does not equal semantic interpretation
4. execution coordination does not equal autonomous planning
5. observability does not equal surveillance
6. cross-service integration does not justify ownership drift
7. cloud augmentation does not erase meaningful local baseline responsibility

## Anti-drift interaction rule

If a proposed integration causes one service to inherit the authority of another by convenience, the integration should be narrowed, rejected, or split.