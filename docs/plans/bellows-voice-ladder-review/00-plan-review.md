# Plan Review — Bellows + Voice Ladder Plan Set v0.2 vs. Active Repos

**Reviewed:** 2026-06-23 · **Plan date:** 2026-06-23 (v0.2)
**Repos checked:** neuronforge, neuroforge, forge-local-runtime, forge_contract_core, Author-Forge, Forge-Agents

## Verdict

The plan's **layering doctrine is sound and the promotion-ladder spine maps almost 1:1 onto NeuronForge's real lane registry.** But the plan is written as if voice/TTS is greenfield. It is not. **A baseline-quality TTS narration pipeline already ships across NeuroForge + AuthorForge**, and several governance gates the plan walks through (new local service, new contract families) are hard-blocked by existing doctrine in forge-local-runtime and forge_contract_core. The plan needs a reconciliation pass before build, not a rewrite.

Three things must change before this is buildable:
1. **Reconcile read-back/TTS with the existing audiobook subsystem** (don't re-propose TTS from R0).
2. **Run Bellows through forge-local-runtime's split-trigger doctrine** (it's a hardcoded 4-service substrate).
3. **Split "local receipt" contracts from "cross-repo shared" contracts** — only the latter need forge_contract_core RFCs.

---

## Per-repo alignment

| Repo | Plan's assumption | Reality | Status |
|------|-------------------|---------|--------|
| **neuronforge** | New voice lanes via proposed→experimental→baseline ladder | Lane registry, states, `register_lane()`, `analytics/lanes/*.json`, promotion seam all exist. Plan's slice 08/09 names match conventions. **No audio I/O today (text-only Ollama).** | ✅ Strong fit; needs audio runtime |
| **neuroforge** | Entitled *cloud* ASR/TTS fallback only | ⚠️ Already ships a **full TTS subsystem** (`/api/v1/audiobook`, kokoro/orpheus/qwen3 sidecars, entitlement gating, prep/review-assist). Cloud ASR/TTS does not exist; quota model does not exist. | ⚠️ Collision |
| **forge-local-runtime** | "Bellows" = new shared local service; FA Local admits `voice.*` | FA Local + capability admission are real (Phase-1 **advisory only**). Service roster is a **hardcoded enum of exactly 4** (`df-local-foundation`, `neuronforge-local`, `cortex`, `fa-local`). No `voice.*` capabilities. | ⚠️ Governance gate |
| **forge_contract_core** | 7 new `bellows_*` families + voice payloads | Adding any family **requires an RFC + 3 reviewers + role-matrix entry**. Neither Bellows, NeuronForge, nor AuthorForge is in the role matrix. Reference grammar is `<family>:<id>:v<n>`, not `bellows_audio_session.v1`. | ⚠️ Process skipped |
| **Author-Forge** | Voice capture + read-back UI, accept/edit/reject review | Capture/dictation/STT: **none (true greenfield)**. Read-back/audiobook playback + voice-profile UI + accept/regenerate + `narration_provider_profiles` schema: **already built**. Candidate review pattern (`ContinuityReviewQueue`) is exactly the accept/reject surface to reuse. | ✅ Reuse heavily; ⚠️ playback overlap |
| **Forge-Agents** | Long-running cancellable/observable voice workflows | Run lifecycle (11 states, two-phase cancel), SSE streaming, 9-adapter tool model all exist. A Bellows adapter slots in cleanly. No audio today. | ✅ Strong fit |

---

## Critical conflicts

### C1 — TTS/read-back is NOT greenfield (highest priority)

The plan's entire doc 08 + Level R0–R5 ladder treats read-back TTS as unbuilt ("R1 Proposed TTS lanes → R2 Experimental local TTS → R4 baseline"). In reality:

- **NeuroForge** (`neuroforge_backend/routers/audiobook.py`, 492 lines) exposes `/api/v1/audiobook/{providers,generate,jobs,preview,preflight,prep-assist,review-assist}` and routes to **three baseline local TTS sidecars**: `kokoro-82m` (:8810), `orpheus` (:8811), `qwen3-tts` (:8812). All tagged `"tier": "baseline"`.
- **AuthorForge** ships the consumer half: DB migration `015_audiobook_system.sql` (`narration_provider_profiles`, `audiobook_chapter_assets`, `audiobook_voice_profiles`), a Svelte store with `generateChapter/acceptChapter/previewVoice/regenerateChapter`, and UI (`ChapterAudioPanel`, `VoiceAndPronunciationPanel`, `PreflightExportPanel`) including drift detection.

**The plan's `voice_tts_generate` lane and the existing audiobook generate path are the same capability at different granularity** (paragraph read-back vs. chapter narration), pointed at the **same sidecars** and the **same `narration_provider_profiles` table**.

Worse, there's a latent **ownership contradiction the plan would inherit**: the audiobook code physically lives in the **NeuroForge (cloud)** repo, yet its header comment says *"NeuronForge is the contract and routing layer."* The plan assigns local TTS to **NeuronForge** and cloud TTS to **NeuroForge** — the opposite of where the code sits today.

**Required:** Doc 08 must start from "audiobook TTS exists in NeuroForge+AuthorForge" and define read-back as a *new entry point into the existing pipeline* (shared providers, shared voice profiles, shared drift/accept semantics), not a fresh R0→R4 climb. Resolve the NeuroForge-vs-NeuronForge ownership of the sidecar router explicitly.

### C2 — Bellows as a 5th local service is doctrine-gated

`forge-local-runtime` enforces the substrate roster as a **hardcoded enum** across `service-status.schema.json`, forensic events, and the contract registry: exactly `df-local-foundation`, `neuronforge-local`, `cortex`, `fa-local`. `DECISIONS/0007-split-trigger-policy.md` + `BOUNDARIES.md`: *"No new subsystem may be created for naming symmetry, aesthetic completeness, or speculative future convenience alone."* A split is justified only on distinct ownership / failure posture / schema / observability / reuse / anti-drift value.

- **Capture** (mic, VAD, capture receipts) is genuinely novel — no audio-input code exists anywhere — and plausibly clears the bar.
- **Playback** does *not* — `sound-service.ts` and the audiobook `ChapterAudioPanel` already play audio. Bellows claiming sole playback ownership contradicts shipped code.

**Required:** Add a Bellows split-trigger justification (doc 01 or 02) written against `DECISIONS/0007`, and if admitted, plan the edits to every `service_id` enum + the contract registry. Reconsider whether Bellows owns *playback*, or only *capture* + device/duplex arbitration while playback stays where it is.

### C3 — New contract families skip the RFC process

The 7 `bellows_*` schemas + voice payloads in doc 04 cannot be admitted as drafted:
- `forge_contract_core/CLAUDE.md`: *"Adding a new family Requires RFC … Never add a new family by bypassing the RFC process."* Needs 3 reviewers + migration notes + role-matrix entry.
- Role matrix (`registry/repo_role_matrix.json`) lists no Bellows / NeuronForge / AuthorForge producer. **FP006 (`family_emitted_by_unauthorized_repo`, blocking)** trips immediately.
- Reference grammar is `<artifact_family>:<artifact_id>:v<version>`; `bellows_audio_session.v1` is missing the id segment.

**But most `bellows_*` artifacts are local scratch receipts** (`source_scope: local`). forge_contract_core governs **shared/promotable cross-repo** artifacts; **FP004** explicitly forbids promoting local-only truth "by convenience." So the fix is a *classification split*, not 7 RFCs:
- **Local-only** (capture/playback receipts, duplex state, degraded state, audio segment) → live as Bellows-local schemas, **no forge_contract_core admission needed.**
- **Cross-repo shared** (only what actually crosses a governed seam to DataForge/Forge_Command for durable evidence) → those few need an RFC + role-matrix entry.

**Required:** Doc 04 should label each contract `local` vs `shared` and route only the `shared` ones through the RFC.

---

## Naming / identity gaps

- **"Leopold" is undefined.** It appears in *zero* repos (only spellcheck dictionaries). The plan treats "AuthorForge/Leopold" as a co-primary consumer and names a Leopold conversation/duplex UI. Either it's an unlanded future product or an external codename. **Blocking ambiguity for any flow that targets Leopold** (duplex conversation, voice command). Needs clarification before those slices are scoped.
- **"FA Local" admission is advisory-only today.** `apps/frontend/src/lib/fa-local.ts` is Phase-1: *"denials logged but don't yet block operations."* The plan's "FA Local admits or denies before the public app starts a Bellows session" assumes **enforcement that isn't live**. Fine as a target, but the plan should state it depends on FA Local reaching enforcing posture, and add the new `CapabilityRecord`s (`audio.capture`, `audio.playback`, etc.) — they don't exist.
- **"Cortex" checks out.** It's a real, defined service (file intelligence / retrieval prep) in forge-local-runtime; using it for context packets + pronunciation hints aligns with its charter. (Cortex repo isn't in active scope to verify deeper.)

---

## Where the plan is genuinely strong (reuse, don't rebuild)

- **NeuronForge lane ladder** — proposed→experimental→baseline already exists with the exact mechanics doc 03/05 assume (`docs/registries/task-lanes.md`, `register_lane()`, `analytics/lanes/*.json`, `verify_promotion_seam.py`). Slice 08/09 file names match repo conventions. Adding `voice_*` lanes is incremental, not architectural. The one real gap: an **audio runtime** (`local_runtime.py` is text-only Ollama) — a `local_audio_runtime.py` is net-new.
- **AuthorForge candidate review** — `ContinuityReviewQueue.svelte` + `candidate_unreviewed → retained/rejected/promoted` state machine + decision log is *exactly* the accept/edit/reject surface in slice 10. Mirror it; don't invent a new pattern.
- **ForgeAgents long-run** — lifecycle/SSE/two-phase-cancel + the 9-adapter model directly support the Story Walk / long-session flow; a `BellowsAdapter` follows the existing adapter recipe.
- **NeuroForge entitlement** — fail-closed `X-Entitlement-Token` gating already exists (Stripe wiring is a TODO); the plan's "entitled cloud assist" plugs in. **Quota** genuinely doesn't exist — that's a real gap the plan can own.
- **Capture/ASR is real greenfield everywhere** — no STT/mic/dictation in any repo. This is the cleanest, least-conflicted part of the plan and the best place to start.

---

## Recommended plan edits (priority order)

1. **Rewrite doc 08 + Level R-ladder** to build *on* the existing NeuroForge/AuthorForge audiobook pipeline; resolve NeuroForge-vs-NeuronForge sidecar-router ownership.
2. **Add a Bellows split-trigger justification** against `forge-local-runtime/DECISIONS/0007`; scope Bellows to capture + device/duplex (leave playback where it ships, or explicitly migrate it).
3. **Classify doc-04 contracts `local` vs `shared`**; RFC only the shared ones; fix reference grammar to `<family>:<id>:v<n>`.
4. **Resolve "Leopold"** — define it or remove it from MVP flows.
5. **State the FA-Local-enforcement dependency** and define the new audio `CapabilityRecord`s.
6. **Sequence the build to start with capture** (true greenfield) while the TTS reconciliation and Bellows admission are settled.
