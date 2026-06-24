# 08 — Read-Back and TTS Ladder (revised)

> **Revision note (v0.3-draft):** v0.2 of this document described read-back/TTS as
> greenfield (a fresh R0→R5 climb that ends in "experimental local TTS"). That is
> incorrect against the live repos. A **baseline-quality TTS narration pipeline already
> ships** across NeuroForge and AuthorForge. This revision rebases read-back onto that
> existing pipeline, resolves a live owner-naming contradiction, and removes the
> duplicate `voice_tts_generate` audio engine. Capture/ASR remains genuinely new and is
> unchanged.

## Current reality (what already exists)

Read-back is **not** building TTS from zero. The following ships today:

- **NeuroForge** — `neuroforge_backend/routers/audiobook.py` exposes `/api/v1/audiobook/{providers,preflight,generate,jobs,preview,prep-assist,review-assist}`. It owns a provider registry and routes to **three baseline local TTS sidecars** on loopback: `kokoro-82m` (:8810), `orpheus` (:8811), `qwen3-tts` (:8812). All are `tier: "baseline"`. A Pro/cloud entitlement gate already exists (fail-closed; Stripe wiring is a TODO). Claude is intelligence-only here, never a narration engine.
- **AuthorForge** — migration `015_audiobook_system.sql` defines the consumer half: `narration_provider_profiles`, `audiobook_voice_profiles`, `audiobook_chapter_assets` (with `generation_status`, `accepted`, `drift_level ∈ {current, minor_drift, critical_drift}`, `provenance`, `model_signature`, `intent_signature`, `high_risk_flags`), and `audiobook_export_packages`. The Svelte store + `ChapterAudioPanel`/`VoiceAndPronunciationPanel`/`PreflightExportPanel` already do generate / preview / accept / regenerate with drift-aware review.

Read-back (paragraph- or selection-level "hear this aloud") is the **same TTS capability** as chapter narration, at finer granularity, pointed at the **same sidecars** and the **same `narration_provider_profiles` registry**. It must reuse that pipeline, not re-propose it.

## Owner-naming contradiction — must be resolved first

The codebase names two different owners for the one TTS routing layer:

- `NeuroForge/.../audiobook.py` docstring: *"NeuronForge is the contract and routing layer."*
- `Author-Forge/.../015_audiobook_system.sql`: *"All narration generation routes through **NeuroForge**."*

v0.2 inherited this by assigning **local** TTS to NeuronForge (the local-candidate repo) and **cloud** TTS to NeuroForge (the cloud repo) — but the shipped audio-generation router (local baseline sidecars *and* the Pro/cloud gate) physically lives in **NeuroForge** and already does local-first-with-entitled-escalation in one place.

**Ruling for this plan (recommended):** the **NeuroForge audiobook router is the single TTS audio-generation + provider-routing layer** for both chapter narration and read-back. Local baseline sidecars and entitled Pro/cloud providers are selected there, by tier, exactly as today. Action: fix the `audiobook.py` docstring to say **NeuroForge** (the cheap correctness fix), rather than migrating a shipped router into NeuronForge (expensive, and it would split local/cloud TTS across two services for no functional gain).

This keeps the plan's doctrine intact — local-first, candidate-only, visible/entitled cloud escalation — without fighting shipped code.

## Revised ownership split

### Public app (AuthorForge) owns
- Which text/selection is read back, and whether read-back is requested.
- Playback UI controls and accessibility preferences.
- The read-back candidate review surface (reuse the continuity/audiobook accept-reject pattern; do not invent a new one).

### NeuronForge owns (its candidate-lane ladder)
- `voice_transcribe` — ASR. **Genuinely new**; no STT exists anywhere yet.
- `voice_cleanup` — transcript text cleanup (text-in/text-out; fits the existing lane model).
- `voice_readback_prepare` — normalizes selected text **for speech only** (abbreviation expansion, pronunciation markup), emitting a reviewable candidate. **Never writes back to the manuscript.**
- NeuronForge does **not** own a separate `voice_tts_generate` audio engine — that would duplicate the audiobook router (see below).

### NeuroForge owns (existing audiobook router)
- TTS audio generation and provider routing for narration **and** read-back.
- Baseline local sidecar selection; entitled Pro/cloud provider selection; provider/cost receipts.

### Bellows owns (new)
- Playback device readiness, audio-hash validation before playback, playback session lifecycle (play/pause/resume/stop), playback receipts, and duplex conflict state when read-back overlaps capture.

## Read-back flow (revised — reuse, don't rebuild)

```text
AuthorForge selected text/paragraph
→ FA Local admission: voice.readback           (capability is new; FA Local enforcement is still Phase-1 advisory — see doc 09)
→ NeuronForge voice_readback_prepare lane       (candidate: speech-normalized text + pronunciation markup)
→ NeuroForge /api/v1/audiobook/generate         (EXISTING router; selects baseline-local or entitled-cloud provider; returns audio asset + hash)
→ Bellows playback session                      (validates hash, plays, emits playback receipt)
→ user listens; optional review notes only
```

`voice_tts_generate` from v0.2 is **retired as a standalone lane** and replaced by the existing audiobook `generate` path. The new surface area for read-back is: (a) the `voice_readback_prepare` candidate lane, (b) a paragraph/selection granularity request shape into the existing generate path, and (c) Bellows playback.

## Revised promotion ladder

The TTS audio engine is **already at baseline**, so the ladder no longer climbs from "experimental local TTS." It tracks the genuinely-new pieces: Bellows playback, the `voice_readback_prepare` candidate lane, and the read-back entry point.

### Level R0 — Bellows playback proof *(new component)*
- Plays a known WAV asset produced by the audiobook `generate` path.
- Validates audio hash; blocks on mismatch.
- Handles pause/resume/stop; emits `bellows_playback_receipt`.

### Level R1 — Read-back entry contracts *(thin, not a new TTS contract)*
- Propose `voice_readback_prepare` lane in NeuronForge (state: `proposed` in `docs/registries/task-lanes.md`).
- Define the selection/paragraph request shape into the **existing** `/api/v1/audiobook/generate` (no new provider contract).
- Unsupported read-back profiles fail closed. No new TTS engine is introduced.

### Level R2 — Experimental read-back prepare lane *(NeuronForge)*
- `voice_readback_prepare` runner emits speech-normalized text + pronunciation markup as a **candidate**.
- Empty/invalid selection degrades safely. Lane moves `proposed → experimental` once tests exist (existing `register_lane` + `analytics/lanes/*.json` mechanics).
- Audio generation continues to use the already-baseline sidecars — nothing experimental there.

### Level R3 — Evidence pack *(extends existing audiobook evidence)*
- Reuse `audiobook_chapter_assets` drift/accept semantics at read-back granularity.
- Samples: narrative prose, dialogue, proper names, long text, punctuation-heavy, playback interruption, **and** duplex (read-back during capture).

### Level R4 — Baseline read-back *(entry-point promotion, not engine promotion)*
- Freeze the `voice_readback_prepare` profile and the read-back voice-profile defaults (reuse `audiobook_voice_profiles`).
- The TTS engine/providers are already frozen at baseline; record that read-back rides them.
- Known limitations documented; release gate passes.

### Level R5 — Entitled cloud read-back *(already-built gate)*
- No new architecture: register Pro cloud providers in `narration_provider_profiles` and rely on the audiobook router's existing fail-closed entitlement gate (wire Stripe per the existing TODO). Quota tracking is the one real gap to add.

## Invariants (unchanged)
- Read-back output is a playback artifact, never user intent or manuscript truth.
- `voice_readback_prepare` never writes back to the document.
- No audio plays without a visible playback indicator (doc 09).
- Cloud read-back is visible, entitled, and receipt-backed; withheld escalation surfaces a denial reason, never a silent fallback.
