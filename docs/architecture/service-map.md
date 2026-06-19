# Service Map — Forge Local Runtime

## Purpose

This document provides the top-level map of the four governed local runtime services and the bounded role each one plays in the local-first service substrate.

## Service map summary

| Service | Primary Role | Core Output | Primary Risk if Unbounded |
|---|---|---|---|
| DF Local Foundation | Local data/control substrate | persistence, readiness, migration/recovery posture | silent accumulation of app/workflow authority |
| NeuronForge Local | Local inference and candidate-production substrate | candidate outputs under contract | silent promotion from candidate to authority |
| Cortex | Local file-intelligence and retrieval-preparation boundary | syntax-level packages and handoff artifacts | drift into semantics, ETL, or surveillance |
| FA Local | Governed local execution boundary | policy-gated execution outcomes | drift into hidden orchestrator or autonomy surface |

## Dependency posture

These four services are co-governed within the local runtime, but they are not interchangeable and must not collapse into one another.

Their interaction model is complementary:

- DF Local Foundation provides bounded substrate mechanics
- NeuronForge Local provides bounded local inference
- Cortex provides bounded syntax-level file intelligence and retrieval preparation
- FA Local provides bounded local execution under trust and policy

## Authority rule

None of the four services is the final authority for overall application truth.

Each service has bounded authority only within its explicit owned role, and each service has explicit non-ownership lines that must be preserved.

## Visibility rule

These services are service-only runtime systems.

They may be surfaced inside consuming applications through bounded controls, diagnostics, or review surfaces, but they are not destination products or peer applications.

## Cloud augmentation line

Cloud services may amplify local capabilities, but they must not erase or redefine the constitutional local baseline represented by these four services.