# Reconciliation Deltas — plan docs 01 / 02 / 05 / 09

Targeted edits to bring the rest of the plan set in line with the two rulings already made:

- **Ruling A (doc 08):** TTS audio generation is the **existing NeuroForge audiobook router**
  (baseline local sidecars + entitled cloud). Read-back reuses it; `voice_tts_generate` is retired.
- **Ruling B (ADR 0010):** Bellows is admitted **scoped to capture + device-level audio
  transport** — not generation, not playback UX, not transcription.

These deltas are advisory; apply them to the source plan files when revising past v0.2.

---

## Doc 01 — Service Doctrine

- **"Bellows owns … Playback loop"** → narrow to **playback transport**: device-level
  play/pause/resume/stop of an *already-produced, hash-validated* audio asset, plus playback
  receipts. Bellows does **not** own playback UX, voice selection, or asset acceptance
  (AuthorForge owns those via `audiobook_chapter_assets` / `sound-service.ts`).
- Add to **"Bellows does not own"**: *TTS audio generation* (NeuroForge audiobook router),
  *playback UI / voice selection / accept-reject* (AuthorForge). It already lists ASR/TTS
  model selection — make the generation exclusion explicit, not just model-selection.
- Keep the no-secret-listening doctrine verbatim; ADR 0008 binds it.

## Doc 02 — System Architecture

- **NeuroForge role** — change from "cloud voice/intelligence fallback" to: **owns TTS audio
  generation and provider routing for narration *and* read-back** (baseline local sidecars +
  entitled cloud), via the existing `/api/v1/audiobook` router. Cloud is the entitled tier of
  that same router, not a separate service.
- **NeuronForge role** — owns **ASR + text lanes only**: `voice_transcribe` (new),
  `voice_cleanup`, `voice_readback_prepare`. Remove `voice_tts_generate` from NeuronForge.
- **Bellows role** — capture + device readiness + VAD + duplex + **playback transport/receipts**.
- **Read-back flow** — replace the `NeuronForge voice_tts_generate` step with:
  `NeuronForge voice_readback_prepare (candidate text)` → `NeuroForge /api/v1/audiobook/generate`
  → `Bellows playback session`. (Mirrors revised doc 08.)
- Fix the inherited owner-naming bug: the audiobook router docstring says "NeuronForge"; the
  AuthorForge migration says "NeuroForge." Architecture must name **NeuroForge** as the TTS
  routing owner and the docstring should be corrected in-tree.

## Doc 05 — Implementation Slices

- **Reorder for risk:** capture is the only fully greenfield, conflict-free area — lead with it.
  Suggested order: Slice 00 skeleton → 01 format → 02 capture loop → 03 VAD → 04 scratch+hash →
  05 **playback transport** (reuses an audiobook-generated asset; validates hash; no generation)
  → 06 duplex → 07 app integration.
- **Slice 08 (NeuronForge proposed lanes):** drop `voice_tts_generate`. Propose
  `voice_transcribe`, `voice_cleanup`, `voice_readback_prepare` only.
- **Slice 09 (experimental runners):** remove `voice_tts_generate_lane.py` /
  `voice-tts-generate.json`. The TTS engine already exists in NeuroForge; do not re-implement.
  Add `voice_readback_prepare_lane.py` instead.
- **Slice 13 (cloud assist):** reframe as "register Pro cloud providers in
  `narration_provider_profiles` + wire the existing fail-closed entitlement gate (Stripe TODO)
  + add quota tracking" — not new architecture.
- **Add a contracts note:** all `bellows_*` schemas and voice payloads are `local`/
  service-internal; no forge_contract_core RFC (see `04-contract-classification.md`).

## Doc 09 — Privacy, Permissions, Accessibility

- **Capabilities** — `audio.capture`, `audio.playback`, `audio.duplex`, `audio.scratch.write`,
  `audio.scratch.delete` are admitted through **FA Local** as `capability_id` strings. Note the
  dependency: FA Local admission is **Phase-1 advisory today** ("denials logged but don't yet
  block"); enforcing posture is a prerequisite for the plan's "admit before session" guarantee.
- **Bind to ADR 0008** explicitly: visible recording state, no hidden continuous loop,
  path-hash-not-raw-path, bounded retention. Wake-word / always-listening stays out of scope
  and needs its own ADR (matches the plan's existing anti-secret-listening section — just cite
  0008).
- **Degraded vocabulary** — reconcile `bellows_degraded_state.v1` codes with ADR 0009 /
  the shared `degraded_subtype` enum rather than free-form labels.
- **Accessibility / playback UX** stays AuthorForge-owned; Bellows only exposes stable
  capture/playback **state + device diagnostics**. (Doc 09 already says this — keep it.)
