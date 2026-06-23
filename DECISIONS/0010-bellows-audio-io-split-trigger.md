# ADR 0010 — Bellows Audio-I/O Split Trigger

## Status
Proposed (draft for review)

## Context

A plan set ("Bellows + Voice Ladder", v0.2) proposes **Bellows**, a shared local-first
sound-I/O service that captures, normalizes, segments, hashes, stores, plays, and receipts
audio for public-facing apps (AuthorForge, and later others). The plan presents Bellows as a
new substrate-level local service alongside the four governed runtime services.

The runtime roster is deliberately bounded. `schemas/service-status.schema.json` hardcodes
exactly four `service_id` values (`df-local-foundation`, `neuronforge-local`, `cortex`,
`fa-local`) and four `service_class` values (`substrate`, `inference`, `file_intelligence`,
`execution`). ADR 0007 requires that any new subsystem demonstrate genuinely distinct
ownership, failure posture, control language, schema needs, observability constraints,
anti-drift value, and repeated cross-service reuse — and forbids splits created "for naming
symmetry, aesthetic completeness, or speculative future convenience alone."

This ADR evaluates Bellows against ADR 0007 before any roster change is made.

## Decision

**Admit Bellows as a fifth governed local service, scoped to audio capture and
device-level audio transport only.** It does not own audio generation, transcription,
playback UX, or audio-asset acceptance.

### ADR 0007 seven-criteria evaluation

| Criterion | Verdict | Basis |
|-----------|---------|-------|
| Distinct **ownership** | ✅ Pass | Microphone/speaker device control, VAD segmentation, capture/playback transport, duplex arbitration. No existing service owns hardware sound I/O. |
| Distinct **failure posture** | ✅ Pass | `device_unavailable`, `permission_denied`, `buffer_overrun`, `silent_input`, `duplex_conflict`, `echo_cancellation_unavailable` — hardware-I/O failure modes absent from the inference/file-intelligence/execution/substrate vocabularies. |
| Distinct **control language** | ✅ Pass | capture / playback / VAD / duplex / device-readiness vocabulary is its own. |
| Distinct **schema needs** | ✅ Pass | audio session / segment / capture-receipt / playback-receipt / duplex-state are not expressible in the four current service schemas. |
| Distinct **observability constraints** | ✅ Pass (and decisive) | Capture literally records the user. ADR 0008 privacy-preserving observability applies with unusual force: anti-secret-listening, visible-recording-state, path-hash-not-raw-path, retention bounds. This is materially different from any current service. |
| **Anti-drift value** | ✅ Pass (and decisive) | Keeping "capture sound" out of NeuronForge prevents the inference service from absorbing device control and secret-listening risk. The capture/interpret separation is the core anti-drift win. |
| Repeated **cross-service reuse** | ✅ Pass | Feeds NeuronForge (ASR input by ref+hash), consumes NeuroForge-produced audio for playback, serves multiple public apps. |

**Capture passes cleanly.** The decisive criteria are observability and anti-drift: a
sound-capture concern must not be folded into an inference repo.

### Required scoping (where the split must NOT over-reach)

The split is admitted **only** under these boundaries, because the adjacent concerns already
have owners and would fail the reuse/anti-drift test if claimed by Bellows:

- **Audio generation (TTS) is NOT Bellows.** It ships today in the NeuroForge audiobook
  router (baseline local sidecars + entitled cloud). Bellows plays the produced asset; it
  never generates it.
- **Playback UX and audio-asset acceptance are NOT Bellows.** AuthorForge owns playback
  controls, voice selection, and accept/reject (`audiobook_chapter_assets`,
  `sound-service.ts`). Bellows owns only the device-level playback **transport + receipt**.
- **Transcription/interpretation is NOT Bellows.** That is NeuronForge (ASR/cleanup lanes).

So Bellows = capture + device readiness + VAD segmentation + duplex arbitration + governed
playback transport/receipts. Nothing above the device/transport seam.

## Consequences

- **Roster change required.** Add `bellows-local` to the `service_id` enum and a new
  `service_class` (proposed: `audio_io`) in `schemas/service-status.schema.json`, plus the
  forensic-event, contract-registry, and service-matrix schemas. This is a governed schema
  change, not an implementation detail.
- **Degraded vocabulary must conform to ADR 0009.** Bellows degraded subtypes must map onto
  the runtime denial/degraded taxonomy; they may not introduce free-form labels. The plan's
  `bellows_degraded_state.v1` codes need reconciling with the shared `degraded_subtype` enum.
- **ADR 0008 binds Bellows hard.** Capture mandates visible recording state, no hidden
  continuous loop, path-hash-not-raw-path, and bounded retention. Any future wake-word /
  always-listening mode is explicitly out of scope and would require its own ADR.
- **FA Local admits Bellows capabilities.** New `audio.capture` / `audio.playback` /
  `audio.duplex` capability IDs are admitted through FA Local (currently Phase-1 advisory;
  enforcement is a dependency, see the plan review).
- **No new contract-core families needed for the local seam.** Bellows audio session/segment/
  receipt artifacts are `source_scope: local` and stay out of forge_contract_core (see the
  companion contract-classification note). Only a genuine cross-repo promotion seam would
  trigger an RFC.
- **Boundary review owns the final call.** This ADR is a Proposed draft; acceptance and the
  roster edits are reserved to the runtime boundary authority.
