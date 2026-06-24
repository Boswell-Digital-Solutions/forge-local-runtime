# Bellows + Voice Ladder — Plan Review

Review of the external "Bellows + Voice Ladder" plan set (v0.2) against the live Forge
repos, produced 2026-06-23. This bundle is review/advisory material, not accepted doctrine.

## Contents

| File | What it is |
|------|------------|
| `00-plan-review.md` | Consolidated review: per-repo alignment, three critical conflicts (C1–C3), naming gaps, strengths, prioritized edits. |
| `08-readback-tts-ladder.revised.md` | Rewritten plan doc 08, rebased onto the existing NeuroForge+AuthorForge audiobook pipeline (resolves C1). |
| `04-contract-classification.md` | local-vs-shared classification of the doc-04 contracts; shows none need a forge_contract_core RFC if kept local (resolves C3). |
| `05-roster-and-slices-reconciliation.md` | Targeted deltas applying the doc-08 and ADR-0010 rulings to the remaining plan docs (01 doctrine, 02 architecture, 05 slices, 09 capabilities). |

The companion split-trigger evaluation (C2) lives as a Proposed ADR:
`DECISIONS/0010-bellows-audio-io-split-trigger.md`.

## Headline findings

1. **C1 — read-back/TTS is not greenfield.** A baseline TTS pipeline already ships
   (NeuroForge audiobook router → kokoro/orpheus/qwen3 sidecars; AuthorForge consumer schema
   + UI). Read-back must reuse it, not re-propose it. A live owner-naming contradiction
   (audiobook router says "NeuronForge"; AuthorForge migration says "NeuroForge") needs
   resolving.
2. **C2 — Bellows is a 5th service behind a doctrine gate.** Evaluated against ADR 0007 it
   passes, scoped to capture + device-level transport (not generation, not playback UX).
3. **C3 — new contract families skip the RFC, but mostly don't need one.** Keep the `bellows_*`
   and voice payloads `local`/service-internal; route durable sync through DataForge Local.

Deferred: "Leopold" (undefined across all repos) — out of scope for this pass per request.
