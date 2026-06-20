# AuthorForge ↔ Forge Local Runtime — Status Read Contract

How a consumer (AuthorForge's RuntimeStatusCard) reads the runtime status surfaces
this repo produces. The intent is that AuthorForge **renders** these surfaces and
performs no cross-service aggregation of its own (AuthorForge V1 §2.1/§2.3).

This is a read contract: AuthorForge consumes; Forge Local Runtime owns the truth,
the schemas, and the degraded semantics described here.

## Surfaces

| Surface | Schema | Producer |
| --- | --- | --- |
| Service matrix | `schemas/runtime-service-matrix.schema.json` | `runtime_status.build_service_matrix` |
| Pressure indicator | `schemas/runtime-pressure.schema.json` | `runtime_status.derive_pressure` |
| Contract registry | `schemas/contract-registry.schema.json` | `registry/local-runtime-contract-registry.json` |

## Service matrix (`runtime-service-matrix`)

- Always contains **exactly four** entries — `df-local-foundation`,
  `neuronforge-local`, `cortex`, `fa-local`. A consumer can rely on every service
  being present every time.
- A service that did not report is **not omitted**. It appears with
  `observation` ∈ {`missing`, `unreachable`, `timeout`}, `state: unavailable`, and
  `readiness_class: not_ready`. Render these as down/unknown, never as healthy.
- `state`, `degraded_subtype`, `readiness_class`, and `blocking_reasons` reuse the
  shared `service-status` / `readiness-summary` vocabularies — no AuthorForge-private
  status enums.
- `generated_at` is the snapshot time; `details_redacted` indicates whether operator
  detail was withheld. Do not infer freshness per-service beyond `last_updated_at`.

## Pressure indicator (`runtime-pressure`)

- `pressure_class` is one of `low` / `elevated` / `critical` — a deterministic pure
  function of a single matrix snapshot. The same matrix always yields the same
  pressure; there is no sampled/time-series state to reconcile.
- `contributing_reasons[]` names the per-service signals that raised pressure above
  `low` (empty when `low`). Use it to explain the indicator, not to recompute it.
- Rollup summary (for display copy, authoritative rule lives in
  `runtime_status/aggregator.py`):
  - **critical** — any service `unavailable`/`denied`, `not_ready`, or carrying an
    integrity/dependency block.
  - **elevated** — any service degraded/stale/partial/review/approval-waiting, or
    readiness reduced.
  - **low** — otherwise.
- This is intentionally three classes, not a metrics dashboard (V1 §2.3 guardrail).

## Contract registry (`contract-registry`)

- The seam catalog: for each live seam, its `owner`, `consumers`, `contract_id` +
  `contract_version`, `posture`, `maturity`, and `degraded_behavior`.
- Consumers must honor `maturity`: a `planned` seam is **not** callable. For example
  `analyze.continuity.scene_window.v1` is `planned`; the live continuity contract is
  `analyze.continuity.adjacent_scene.v1`. Binding to a `planned` contract is a drift
  bug.

## Degraded semantics (producer-defined)

- Absent producer → the consumer shows the fail-closed `unavailable` entry from the
  matrix, not a blank or optimistic state.
- Absent matrix entirely → no pressure indicator is derivable; show "runtime status
  unavailable", do not synthesize one.
- The consumer never invents a service state the producer did not assert.
