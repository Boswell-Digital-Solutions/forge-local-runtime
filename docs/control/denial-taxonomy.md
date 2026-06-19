# Denial Taxonomy — Forge Local Runtime

## Purpose

This document defines the shared runtime denial vocabulary for Forge Local Runtime services.

## Rule

Denial must be explicit, typed, and operationally useful.

A denied action should explain enough for the operator or consuming application to understand whether the issue is remediable, reviewable, policy-based, contract-based, or safety-based.

## Shared denial reason classes

The runtime supports at least:

- `unknown_requester`
- `untrusted_requester`
- `missing_policy`
- `policy_denied`
- `capability_not_admitted`
- `contract_invalid`
- `integrity_failed`
- `dependency_unavailable`
- `privacy_scope_violation`
- `review_required`
- `unsupported_route`
- `disabled_by_operator`

## Shared denial scopes

The runtime supports at least:

- `request`
- `capability`
- `route`
- `service`
- `artifact`
- `operation`

## Shared denial posture

Every denial should preserve:

- denied state
- reason class
- scope
- whether denial arose from contract, policy, both, or runtime safety
- whether the issue is remediable
- whether a review path is available
- operator-visible summary
- timestamp

## Schema alignment

Denial taxonomy aligns with:

- `schemas/denial-state.schema.json`
- `schemas/service-status.schema.json`

## Service examples

### FA Local
Most likely to emit trust, policy, capability-admission, approval, and bounded-plan denial posture.

### Cortex
May emit denial-like handoff or privacy-scope rejection posture where integrity or observation constraints are violated.

### DF Local Foundation
May deny migration, restore, or integrity-sensitive operations when substrate constraints make safe continuation invalid.

### NeuronForge Local
May deny invalid or unsupported contract routes or report unavailable dependency posture when local inference routes are not admissible.

## Governing question

Does the denial communicate the real reason and scope, or is it hiding runtime truth behind generic failure wording?