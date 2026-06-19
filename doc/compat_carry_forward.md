Use this as the **replacement carry-forward**.

---

# Forge Local Runtime → DataForge Promotion — Carry-Forward Context (Compact)

## Current state

The first real local-runtime-to-DataForge runtime-promotion proving slice is now materially working end to end.

A true Postgres-backed and HTTP-delivered path has now been proven across the local runtime and DataForge seam.

This is no longer only a local queue/worker proof.
A real delivery seam now exists from local runtime promotion artifacts into durable DataForge receipt storage. 

---

## What is now proven

### 1. Local persistence path

Already proven:

* candidate signal creation
* promotion envelope normalization
* policy gate review
* queue-plan creation
* DB write planning
* persistence into `runtime_promotion.outbound_artifacts`
* persistence into `runtime_promotion.policy_events`
* direct DB verification confirming queued records were real, not inferred

### 2. Worker typing blocker resolved

Resolved:

* `runtime_promotion/worker.py` updated so `WorkerCursor` is `@runtime_checkable`
* worker mypy passes for:

  * `runtime_promotion/connection.py`
  * `runtime_promotion/worker.py`
  * `scripts/run_runtime_promotion_worker.py`

### 3. Worker success-path proof completed

Proven flow:

* queued artifact claimed safely
* row moved into `delivery_in_progress`
* `delivery_attempt_count` incremented
* worker marked artifact `delivered`
* Postgres verification confirmed:

  * `status = delivered`
  * non-null `last_attempted_at`
  * non-null `acknowledged_at`

### 4. Worker retry-path proof completed

Proven flow:

* queued artifact with delivery failure claimed safely
* row moved into `delivery_in_progress`
* `delivery_attempt_count` incremented
* worker scheduled retry through retry-release logic
* Postgres verification confirmed:

  * `status = retry_scheduled`
  * non-null `last_attempted_at`
  * non-null `next_attempt_at`
  * null `acknowledged_at`
  * populated `rejection_reason_class`

### 5. DataForge receipt slice is now real

A bounded DataForge receipt slice is now proven:

* DataForge accepts runtime-promotion receipt payloads
* DataForge writes durable receipt rows
* DataForge receipt ingest supports idempotent replay behavior
* local runtime only transitions to `delivered` after DataForge acceptance

### 6. Real transport seam is now proven

Proven end-to-end flow:

* local artifact seeded as `queued`
* worker claims artifact
* worker performs real HTTP POST to DataForge
* DataForge accepts and persists receipt
* local artifact transitions to `delivered`
* local `acknowledged_at` is populated

### 7. Dual-DB verification is now proven

Confirmed on the local runtime side:

* successful artifact rows reach `delivered`
* failed attempts can reach `retry_scheduled`
* delivery metadata is durably persisted

Confirmed on the DataForge side:

* receipt row exists for the delivered artifact
* receipt matches the artifact dedupe key
* receipt is stored as accepted ingest

### 8. Repo-native integration proof now exists

A repeatable integration proof is now in place for the seam:

* seed queueable artifact
* run worker
* verify local delivered transition
* verify DataForge receipt exists

This proof now passes end to end when:

* local runtime env is loaded
* DataForge is running
* `DATAFORGE_DATABASE_URL` is available in the test shell

---

## Important issues encountered during this pass

### 1. Env loading remains a recurring blocker

Both repos still require explicit env loading in the active shell.

Common pattern:

```bash
set -a
source .env
set +a
```

### 2. Repo-specific DB variable names matter

Forge Local Runtime uses:

* `FORGE_LOCAL_RUNTIME_DATABASE_URL`

DataForge verification required:

* `DATAFORGE_DATABASE_URL`

### 3. Proof scaffolding had to be aligned to repo truth

The first integration scaffold needed correction to match actual repo truth, including:

* real outbound table columns
* real payload JSON shape expected by the worker/DataForge seam
* actual local env variable names
* actual DataForge verification path

### 4. DataForge availability is a hard seam dependency for full proof

The integration proof correctly fails if DataForge is not running on the expected local endpoint.

That is now a real verified dependency rather than an inferred one.

---

## Current immediate next step

The next correct step is:

## Preserve the passing proof, clean the test posture, then move to the next operational layer

Recommended order:

1. register the custom pytest marks so the proof runs cleanly without warnings
2. preserve this milestone in carry-forward context
3. treat this passing integration test as the new transport proof baseline
4. move to the next bounded slice:

   * DataForge shaping accepted receipts into governed recommendation candidates
   * recommendation-candidate storage/read model
   * later ForgeCommand review-surface integration

---

## Important posture to preserve

Keep these boundaries intact:

* normalization does not do policy
* policy does not do DB persistence
* persistence does not decide policy
* worker transport does not redefine queue meaning
* local runtime does not become cloud-dependent by stealth
* DataForge receipt ingest remains bounded to receipt acceptance
* DataForge receipt ingest does not yet become recommendation generation
* ForgeCommand remains the future governed review surface, not the transport layer 

---

## Compact summary

You now have:

* doctrine
* reviewed schemas
* local Postgres queue schema
* Python promotion package boundaries
* policy and persistence tests
* worker tests
* real local persistence proof
* real worker success-path proof
* real worker retry-path proof
* real HTTP delivery into DataForge
* real DataForge receipt persistence
* dual-DB verification
* a passing repo-native integration proof for the seam

The first runtime-promotion delivery seam is now real and repeatable.

The next move is **not** more transport debugging.
The next move is to preserve this proof baseline and begin the next slice where accepted DataForge receipts are shaped into governed recommendation candidates for later ForgeCommand review. 