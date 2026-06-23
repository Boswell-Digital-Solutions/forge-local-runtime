# Doc-04 Contract Classification — local vs. shared

**Purpose:** resolve conflict **C3** of the plan review. v0.2 doc 04 defines seven
`bellows_*` schemas plus four NeuronForge voice payloads and implies they need
forge_contract_core admission. They mostly do not. forge_contract_core governs only
**cross-repo shared / promotable** artifacts; local scratch evidence stays out of it, and
**FP004 (`local_only_truth_promoted_by_convenience`, blocking)** forbids promoting local
truth into the shared corpus for convenience.

The fix is a classification, not seven RFCs.

## Rule

- `source_scope: local` → service-owned schema; **no forge_contract_core family, no RFC.**
  Durable sync (if any) goes through **DataForge Local** (owner of local operational memory,
  receipts, and syncable edge evidence), not through a contract-core family.
- `source_scope: shared|restricted` → crosses a governed promotion seam into canonical truth
  → **requires RFC + repo-role-matrix entry**, and should reuse an existing family where one
  fits rather than minting a bespoke one.

## Classification

| Contract (v0.2 doc 04) | Scope | Governed by | Contract-core RFC? |
|------------------------|-------|-------------|--------------------|
| `bellows_audio_session.v1` | local | Bellows (schema) | No |
| `bellows_audio_segment.v1` | local | Bellows (schema); handoff to NeuronForge is **ref+hash**, not a family | No |
| `bellows_capture_receipt.v1` | local | Bellows; optional sync via DataForge Local | No |
| `bellows_playback_session.v1` | local | Bellows | No |
| `bellows_playback_receipt.v1` | local | Bellows; optional sync via DataForge Local | No |
| `bellows_duplex_state.v1` | local | Bellows | No |
| `bellows_degraded_state.v1` | local | **forge-local-runtime degraded taxonomy (ADR 0009)** — must map to the shared `degraded_subtype` enum, not invent labels | No (but reconcile vocabulary) |
| `voice_transcribe` payload | service-internal | **NeuronForge** task contract (`AuthorForgeTaskEnvelopeV1`) | No |
| `voice_cleanup` payload | service-internal | NeuronForge task contract | No |
| `voice_tts_generate` payload | *retired* | replaced by existing NeuroForge audiobook `generate` (see revised doc 08) | No |
| `voice_readback_prepare` payload | service-internal | NeuronForge task contract | No |

**Result: none of the v0.2 contracts require a forge_contract_core RFC**, provided they are
explicitly marked `local`/service-internal and durable sync is routed through DataForge Local.

## The one place an RFC would be needed

If voice evidence is later promoted to **canonical cross-system truth** — e.g. a capture/
playback receipt surfaced for durable operator review in Forge_Command, or a voice "finding"
entering the promotion corpus — that single seam needs:

1. An RFC per `doc/system/40_governance/12-change-workflow-and-rfc-rules.md` (3 reviewers,
   migration notes, compatibility).
2. A `registry/repo_role_matrix.json` producer entry (none of Bellows / NeuronForge /
   AuthorForge is listed today; without it **FP006** blocks emission).
3. Reuse of an existing receipt/evidence family if one fits, rather than a new `bellows_*`
   family, to avoid family proliferation.

The plan does not currently require this seam. Keep everything local until it genuinely does.

## Secondary fixes for doc 04

- **Reference grammar.** If any artifact does become a contract-core family, its reference is
  `<artifact_family>:<artifact_id>:v<version>` (e.g. `bellows_capture_receipt:<uuid>:v1`),
  not `bellows_capture_receipt.v1`. The `.v1` filename suffix is fine for schema *files*;
  it is not a valid artifact *reference*.
- **No nested envelopes.** Local schemas that later promote must not nest the shared envelope
  in their payload (**FP001**).
- **Degraded reconciliation.** Align `bellows_degraded_state.v1` codes with ADR 0009 / the
  `degraded_subtype` enum before treating them as a stable contract.
