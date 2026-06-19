# Service-Only Visibility Rule — Forge Local Runtime

## Purpose

This document defines how the four governed local runtime services may appear inside consuming applications without becoming parallel products.

## Rule

DF Local Foundation, NeuronForge Local, Cortex, and FA Local are service-only runtime systems.

They may be visible only through bounded application-embedded surfaces such as:

- status indicators
- bounded diagnostics
- review and approval surfaces
- constrained controls
- operator-facing runtime health views

They must not be framed as standalone destination products by default.

## Why this rule exists

Without explicit visibility constraints, infrastructure systems often drift into:

- pseudo-products
- parallel workflows
- hidden control planes
- user-facing identities that blur authority boundaries

This repository prohibits that drift by default.

## Allowed visibility

Allowed visibility is bounded and role-specific.

Examples include:

- a readiness or degraded-state indicator for Cortex inside an app
- an approval-required panel for FA Local inside a governed workflow
- a local model-route status surface for NeuronForge Local
- a migration/restore health surface for DF Local Foundation

## Disallowed visibility drift

Disallowed visibility includes:

- independent product positioning for the four runtime services
- broad user workflow surfaces that bypass consuming applications
- standalone app identity for service-only runtime subsystems
- convenience dashboards that imply broader authority than the service actually owns

## Cross-reference to schema posture

Visibility surfaces should derive state from shared runtime schemas where possible, including:

- `schemas/service-status.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/readiness-summary.schema.json`

## Governing question

Before adding a new UI or operator surface, ask:

Does this make the runtime service more understandable inside the consuming application, or does it accidentally make the service look like an independent product?