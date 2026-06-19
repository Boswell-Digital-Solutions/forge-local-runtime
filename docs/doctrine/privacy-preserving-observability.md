# Privacy-Preserving Observability — Forge Local Runtime

## Purpose

This document defines the observability doctrine for the Forge local runtime layer.

## Rule

Operational truth is required.
Content collapse is prohibited.

The runtime must provide enough visibility for readiness, degraded-state truth, denial, review posture, integrity issues, and forensic accountability without normalizing raw content inspection.

## Default posture

Observability is minimized, scoped, and content-sparing by default.

Preferred signals include:

- state labels
- degraded subtypes
- denial reason classes
- hashes
- counts
- timestamps
- route identifiers
- requester class
- capability ids
- plan hashes
- retention labels
- redaction markers

## Disallowed defaults

The following must not become default posture:

- raw file capture
- prompt transcript retention
- broad always-on watchers
- full payload logging
- convenience copies of sensitive content in forensic events
- persistent surveillance by default

## Service-specific posture

### DF Local Foundation
Should expose readiness, migration, restore, integrity, and retention posture without broad artifact-content exposure.

### NeuronForge Local
Should expose route, contract, readiness, degraded, and fallback truth without default prompt/content retention.

### Cortex
Should expose intake, extraction, freshness, integrity, and handoff quality posture without broad raw-content capture.

### FA Local
Should expose denial, approval, capability, requester-class, and minimized forensic posture without default tool-payload capture.

## Schema alignment

Observability doctrine should align with:

- `schemas/service-status.schema.json`
- `schemas/denial-state.schema.json`
- `schemas/degraded-state.schema.json`
- `schemas/forensic-event-envelope.schema.json`
- `schemas/handoff-envelope.schema.json`

## Governing question

Does the proposed observable surface preserve runtime truth while minimizing content exposure and surveillance power?