# AuthorForge Local Runtime Integration — Forge Local Runtime Producer Work Plan

Status: planning artifact
Scope: producer-side obligations that land in **this repo** (Forge Local Runtime)
Upstream: `Author-Forge/doc/plans/authorforge_local_runtime_integration_plan_v_1.md`
and its substrate-application review
(`authorforge_local_runtime_integration_v1_substrate_application.md`).

## Why this exists

The AuthorForge Local Runtime Integration Plan V1 asks AuthorForge to build three
cross-service control surfaces inside the app: a Local Runtime Contract Registry
(V1 §0.1), a RuntimeStatusCard **service matrix** (V1 §2.1), and a runtime **pressure
indicator** Low/Elevated/Critical (V1 §2.3).

Forge Local Runtime is the governance + shared-schema authority layer over the four
local services (DF Local Foundation, NeuronForge Local, Cortex, FA Local). These
surfaces are cross-service aggregation and therefore belong **here**, produced once
and consumed by AuthorForge — not reimplemented per app. The schemas needed already
exist; what is missing is the aggregation layer, a pressure rollup, a registry
artifact, and cross-service boundary assertions in the gate.

This repo stays a **producer**: it composes and exposes truthful state. It does not
own product workflow, and it does not invent runtime behavior beyond the bounded
contracts below. Fail-closed posture is preserved throughout — absent/unreadable
service state is reported as `not_ready` / `unavailable`, never silently omitted.

---

## Ticket T1 — Runtime service-status aggregator (service matrix)

Satisfies: V1 §2.1 (RuntimeStatusCard service matrix), §2.4 (DF Local visibility).

**Builds on:** `schemas/service-status.schema.json`, `schemas/readiness-summary.schema.json`
(already carries `service_id`, `readiness_class`, `blocking_reasons`).

**Deliverable:**
- A `runtime-service-matrix.schema.json` envelope that composes the per-service
  `service-status` / `readiness-summary` envelopes for the four services into one
  bounded snapshot (each entry: `service_id`, `readiness_class`, `degraded_subtype?`,
  `blocking_reasons[]`, `last_updated_at`, `details_redacted`).
- An aggregator module under `runtime_promotion/` siblings (e.g. `runtime_status/`)
  that collects each service's status and emits the matrix. A service that does not
  answer is recorded as `not_ready` with `blocking_reason: dependency_unavailable` —
  never dropped.

**Acceptance:**
- Matrix represents all four services every time, with explicit unavailable entries.
- No app/business logic; only composition of declared service envelopes.
- Schema passes `ci_gate.sh` Gate 2 (well-formedness) and contract-core Gate 1.

**Out of scope:** rendering, alerting, history/retention.

---

## Ticket T2 — Runtime pressure indicator (Low / Elevated / Critical)

Satisfies: V1 §2.3.

**Builds on:** `schemas/runtime/promotion/local_state_event.schema.json` (4-level
`severity`: low/moderate/high/critical) and the T1 matrix.

**Deliverable:**
- A `runtime-pressure.schema.json` with a bounded `pressure_class`
  (`low` / `elevated` / `critical`) plus the `contributing_reasons[]` that produced
  it (drawn from `readiness_class` + `blocking_reasons` + recent `severity`).
- A deterministic, documented rollup rule (e.g. any `not_ready` → at least
  `elevated`; any `critical` severity or integrity/dependency block → `critical`).
  The rule must be a pure function of T1 state, not a sampled metric.

**Acceptance:**
- Pressure is reproducible from a given matrix snapshot (no hidden state).
- Mapping rule documented inline and covered by fixtures.
- Explicitly **not** a noisy ops dashboard (V1 §2.3 guardrail) — three classes only.

**Out of scope:** time-series, thresholds tuning UI, per-process metrics.

---

## Ticket T3 — Local Runtime Contract Registry (seam catalog)

Satisfies: V1 §0.1.

**Builds on:** `schemas/runtime-contract.schema.json` (seam envelope with
`source_service_id`, `target_service_id`, `capability_id`, `contract_class`) and
`doc/runtime/Forge Local Runtime — Data Ownership Matrix v1.md`.

**Deliverable:**
- A `contract-registry.schema.json` and a checked-in registry artifact cataloging
  each live local-runtime seam: seam name, owner service, consumer(s),
  contract id + version, candidate-vs-authority posture, degraded behavior, and
  maturity (`implemented` / `partial` / `planned`).
- Seed it from current truth, including known cross-app drift, e.g.:
  - Cortex `handoff-envelope` / `GnatSemanticHandoff.v1` (candidate-only).
  - NeuronForge `analyze.continuity.adjacent_scene.v1` **implemented**;
    `analyze.continuity.scene_window.v1` **planned** (records the AuthorForge
    binding-drift the substrate review flagged).
  - FA Local `GnatDispatchEnvelope.v1` implemented; callable admission seam `planned`.

**Acceptance:**
- One artifact shows what is actually live between each service and its consumers.
- Maturity field makes planned-vs-served unambiguous (prevents recurrence of the
  scene_window binding drift).

**Out of scope:** runtime registry persistence/mutation; this is a governance catalog.

---

## Ticket T4 — Cross-service boundary assertions in the CI gate

Satisfies: V1 §0.2 (Boundary Assertion Test Plan), at the cross-service tier.

**Builds on:** `ci_gate.sh` (contract-core + schema-wellformedness) and the existing
doctrine docs under `docs/doctrine/`.

**Deliverable:** gate checks that fail on boundary drift, e.g.:
- Cortex handoff envelopes carry no orchestration fields (no `retry_*`, `workflow_id`,
  `executor`, `dispatch_plan`, …) — syntax-vs-semantics firewall.
- NeuronForge outputs declare `trust_posture: candidate_only` (no authority leak).
- FA Local routes that are non-executable carry no execution plan
  (policy-before-execution).
- Every populated service exposes a `service-status` conforming to the shared schema
  (so T1 can always aggregate it).

**Acceptance:**
- Boundary rules are testable in CI, not just documented.
- Gate stays green on current truth; new violations fail closed.

**Out of scope:** consumer-side (AuthorForge) boundary tests — those stay in the app.

---

## Ticket T5 — Consumer read-contract for AuthorForge

Ties T1/T2/T3 to the consumer so AuthorForge renders rather than recomputes.

**Deliverable:**
- A short read-contract doc describing how AuthorForge's RuntimeStatusCard consumes
  the T1 matrix and T2 pressure (shape, refresh expectations, degraded semantics),
  and how it reads the T3 registry. Cross-link from
  `docs/architecture/runtime-control-surfaces.md`.

**Acceptance:**
- AuthorForge can implement V1 §2.1/§2.3 by consuming these surfaces with no
  cross-service logic of its own.
- Degraded/unavailable semantics are defined by the producer, not guessed by the app.

---

## Sequencing

T1 → T2 (pressure depends on the matrix) → T5 (consumer contract).
T3 and T4 are independent and can land in parallel.

## Non-goals (whole work plan)

- No product/workflow authority moves into this repo.
- No runtime behavior beyond bounded composition + truthful state exposure.
- No silent fallbacks: unavailable substrate state is always explicit
  (`not_ready` / `unavailable` / `denied`), consistent with the repo's fail-closed
  posture.
