# NeuronForge Local Authority Spec

**Document version:** 1.0
**Status:** Active — authority upgrade specification
**Designation:** standalone authority spec (not assembled into `FOLSYSTEM.md`; referenced by it)
**Supersedes:** nothing — extends `docs/services/neuronforge-local-role.md`, `BOUNDARIES.md`, and the Boundary Matrix
**Scope:** NeuronForge Local within the Forge Local Runtime layer

---

## 1. Why this document exists

NeuronForge Local today is a narrow proving slice: proofreading evaluation,
controlled local model evaluation, controlled prompts, and AuthorForge task
routing. That slice is correct, but it is narrower than the role NeuronForge
Local must eventually hold in the local-first runtime.

This spec is the **authority upgrade**. It states, in advance of broad
implementation, exactly what NeuronForge Local is allowed to become, what it is
never allowed to become, and where its authority ends and another service's
begins. It exists so that the expansion from "seed" to "local-first moat"
happens **under contract**, without silent authority drift.

This document does not grant new runtime behavior by itself. It bounds the
behavior that future implementation work may add.

---

## 2. The core authority rule

> **NeuronForge Local owns local execution decisions and local candidate
> generation. DataForge Local owns local persistence. NeuroForge (cloud) owns
> cloud reasoning. Forge_Command owns operator review.**

This four-party split is the constitutional rule of this spec. Every capability
below resolves to exactly one of these four owners. No capability may quietly
relocate across this line.

| Authority | Owner | What it covers |
|---|---|---|
| Local AI execution & candidate generation | **NeuronForge Local** | local model execution, local routing, escalation decision prep, candidate output, local evaluation, local shaping |
| Local persistence | **DataForge Local / DF Local Foundation** | local records, local receipts, local vector/cache storage, local queue durability |
| Cloud reasoning | **NeuroForge (cloud)** | large-model inference, cloud provider orchestration, cloud RAG, cloud evaluation, heavy async reasoning |
| Operator governance & review | **Forge_Command** | promotion approval, operator review of candidates, governance authority, audited authority-changing actions |

NeuronForge Local **decides locally and produces candidates**; it does not
persist canonical truth, it does not orchestrate cloud providers, and it does
not grant operator authority. Those belong to DataForge, NeuroForge, and
Forge_Command respectively.

---

## 3. Current state (proving slice)

NeuronForge Local is presently centered on:

- proofreading evaluation
- local model evaluation
- controlled prompt execution
- AuthorForge task routing
- candidate-only output requiring manual review before promotion
- cloud assist as **visible escalation**, never silent default

These remain valid and are the foundation the upgrade builds on. The cloud-assist
posture — *escalation is visible, never a silent default* — is retained
unchanged and reinforced in §6.

---

## 4. Target authority — what NeuronForge Local owns

NeuronForge Local **owns** the local customer-side AI execution lane. The future
role broadens the seed into the following owned capabilities:

1. **Local inference lane** — bounded local model execution on realistic local
   hardware, the constitutional local baseline that must remain meaningful when
   cloud services are unavailable.
2. **Local AI task routing** — task-contract execution and route-class selection
   for local inference paths (baseline / preferred / degraded fallback /
   unavailable).
3. **Local/cloud escalation decision prep** — preparing and surfacing the
   *decision* to escalate to cloud reasoning. NeuronForge Local decides whether
   escalation is warranted and prepares the request; it does not execute cloud
   provider orchestration.
4. **Candidate generation** — production of candidate outputs that remain
   candidates until an external authority promotes them.
5. **Local evaluation** — local quality/proofreading evaluation of candidates,
   producing a confidence/quality posture, never a promotion.
6. **Local shaping** — bounded local transformation, ranking, comparison, and
   refinement of candidates under contract.
7. **Local RAG** — local retrieval-augmented grounding for local inference,
   consuming bounded retrieval-preparation artifacts (e.g. from Cortex) without
   becoming the retrieval-policy authority or the canonical memory authority.
8. **Local vector / cache memory (operational)** — local operational inference
   memory and caches used to serve the local lane. This is operational memory,
   not canonical systems memory (see §5).
9. **Local receipt creation** — generation of local receipts/records for local
   execution and escalation events. NeuronForge Local *creates* receipt content;
   **DataForge Local persists** it (see §5 and §7).
10. **Cloud escalation policy engine (local-side)** — the local policy that
    decides *when* escalation is allowed/required, under what constraints, and
    with what visibility. This is the local decision engine, distinct from cloud
    provider orchestration which NeuronForge (cloud) owns.
11. **Offline-safe queue behavior** — local queue/deferral posture so that work
    requested while cloud is unavailable is held safely and surfaced truthfully,
    never silently dropped and never silently auto-executed on reconnect.
12. **Local customer authority boundary** — the customer-side execution lane
    boundary: NeuronForge Local runs customer-side AI execution locally and keeps
    sensitive customer content within the local privacy posture.

---

## 5. Target non-authority — what NeuronForge Local must never own

NeuronForge Local **does not own**, and must never silently acquire:

1. **Canonical system memory** — owned by **DataForge Cloud** (canonical) and
   **DataForge Local / DF Local Foundation** (local durable persistence).
   NeuronForge Local's vector/cache memory is operational only; durable local
   truth is persisted by DataForge Local, not by NeuronForge Local.
2. **Cloud provider orchestration** — owned by **NeuroForge (cloud)**.
   NeuronForge Local prepares and decides escalation; it does not select cloud
   providers, manage cloud circuit breakers, or run cloud fallback chains.
3. **Shared contracts** — owned by **forge_contract_core**. NeuronForge Local
   conforms to shared contracts; it does not define or version them.
4. **Public AuthorForge UX** — owned by **AuthorForge**. NeuronForge Local is a
   service-only runtime substrate, never a peer product surface.
5. **Operator governance authority** — owned by **Forge_Command**. NeuronForge
   Local never promotes its own candidates, never performs authority-changing
   actions, and never substitutes for operator review.

It also continues to not own (carried forward from the existing role):

- final semantic, workflow, or application business truth
- hidden autonomous decision loops or silent candidate promotion
- broad execution authority across the runtime
- policy authority for side effects
- durable semantic memory authority by default

---

## 6. Escalation posture (local → cloud)

Escalation from NeuronForge Local to NeuroForge cloud reasoning is governed by
these invariants:

1. **Escalation is visible, never a silent default.** Any cloud assist is an
   explicit, surfaced escalation event with a recorded reason. The local lane
   must never quietly route to cloud as a hidden default.
2. **NeuronForge Local owns the escalation *decision*; NeuroForge owns the
   escalation *execution*.** The local-side policy engine decides whether and
   under what constraints to escalate and prepares the request. Cloud provider
   selection, health gating, circuit breaking, and fallback are NeuroForge's
   authority.
3. **Degraded equivalence must not be faked.** When cloud is unavailable and the
   local lane substitutes, the result must be reported with truthful degraded
   state (`degraded_fallback_equivalent` only when equivalence is genuinely
   justified; otherwise `degraded_fallback_limited`).
4. **Offline-safe by construction.** If escalation cannot proceed (cloud
   unavailable, policy denial, dependency block), work is queued or denied
   truthfully — never silently dropped, never silently auto-promoted on
   reconnect.
5. **Escalation events produce receipts.** Each escalation decision (and its
   outcome) creates a local receipt persisted via DataForge Local.

---

## 7. Persistence and receipts boundary

NeuronForge Local **creates** local execution and escalation receipts; it does
**not** own where durable truth lives.

- NeuronForge Local generates receipt/record *content* for local execution,
  evaluation, and escalation decisions.
- **DataForge Local / DF Local Foundation persists** that content as local
  durable operational memory.
- Canonical/cross-system records and promotion application results are
  **DataForge Cloud** truth, reached only through promotion (see §8), never
  written directly by NeuronForge Local.
- NeuronForge Local's local vector/cache memory is operational substrate for the
  inference lane and is not a durable-truth authority.

This preserves the runtime rule that a candidate-producing service never becomes
a persistence authority by accretion.

---

## 8. Promotion boundary

NeuronForge Local outputs are **candidates**. Promotion to truth is external and
governed:

- A candidate becomes truth only when an external authority promotes it.
  Operator-facing promotion review is **Forge_Command** authority; canonical
  application of a promotion is a **DataForge Cloud** result.
- Promotable NeuronForge Local signal classes are already bounded in the **Data
  Ownership Matrix** (`neuronforge_local.contract_structure_failure_pattern`,
  `neuronforge_local.degraded_ai_mode_frequency`,
  `neuronforge_local.lane_local_eval_result`,
  `neuronforge_local.route_profile_regression_signal`). No NeuronForge Local
  signal is promotion-eligible unless it appears there, and all such promotion is
  `strict_no_content` redaction class.
- NeuronForge Local never promotes its own candidates and never writes canonical
  systems memory.

---

## 9. Privacy posture

NeuronForge Local processes sensitive customer content locally and therefore:

- follows privacy-preserving observability and minimized diagnostics
- never makes prompt/content capture a default observability behavior
- keeps the customer-side execution lane within the local privacy boundary
- promotes only `strict_no_content` bounded signals (per §8), never raw prompts,
  candidate content, or customer-owned material

---

## 10. Interaction posture (authority resolution)

| Counterpart | NeuronForge Local may | NeuronForge Local may not |
|---|---|---|
| **DataForge Local / DF Local Foundation** | rely on it for local persistence, receipts, local readiness artifacts | transfer inference authority to it; persist canonical truth itself |
| **NeuroForge (cloud)** | escalate visibly for cloud reasoning; prepare escalation requests | orchestrate cloud providers; own cloud health/circuit/fallback |
| **Cortex** | consume bounded syntax/retrieval-preparation artifacts for local RAG | treat Cortex as semantic authority; own retrieval policy |
| **FA Local** | be invoked through approved policy-gated runtime paths | become the execution governor; bypass policy gating |
| **Forge_Command** | surface candidates and receipts for operator review | perform promotion or any authority-changing action itself |
| **AuthorForge** | serve the customer-side local AI execution lane under contract | own or render public AuthorForge UX |
| **forge_contract_core** | conform to shared contracts | define or version shared contracts |

---

## 11. Governing rule

NeuronForge Local must remain a bounded, contract-disciplined, candidate-producing
local inference substrate **even as its surface broadens** to the full local-first
lane. The upgrade adds capability; it must never add silent authority.

If a proposal implies any of the following, it must be rejected:

- silent authority promotion of candidates into truth
- NeuronForge Local persisting canonical systems memory
- NeuronForge Local orchestrating cloud providers
- NeuronForge Local defining shared contracts or rendering public AuthorForge UX
- NeuronForge Local performing operator governance or authority-changing actions
- silent (non-visible) cloud escalation as a default
- faked degraded equivalence or silently dropped offline work

---

## 12. Anti-drift checklist (apply before accepting any NeuronForge Local change)

1. Does this keep NeuronForge Local on the **local execution + candidate
   generation** side of §2, or does it reach into persistence, cloud
   orchestration, contracts, UX, or operator authority?
2. Does any new memory/cache claim stay **operational**, leaving durable local
   truth to DataForge Local?
3. Does any new cloud path keep escalation **visible** and leave cloud
   orchestration to NeuroForge?
4. Do new outputs stay **candidate-only** with truthful route-class and degraded
   state?
5. Do escalation and execution events produce receipts **persisted via DataForge
   Local**, not stored as NeuronForge-owned durable truth?
6. Does offline behavior remain **safe** — queued or truthfully denied, never
   dropped or silently auto-executed?
