# Forge Local Runtime — Data Ownership Matrix v1

**Version:** 1.0  
**Date:** 2026-03-31  
**Status:** Active Draft

## Purpose

This document is the first required control artifact for the Forge Local Runtime fleet-promotion doctrine.

Its job is to classify runtime data before any promotion schemas, outbound queue mechanics, transport behavior, or cloud aggregation logic are implemented.

This matrix defines, for each candidate data class:

- who produces it
- who owns it locally
- whether promotion is allowed
- what triggers promotion
- what redaction posture applies
- what deduplication posture applies
- what retention class applies
- whether it may support proposals
- whether offline-local behavior must remain intact
- whether a versioned contract is required

This document exists to prevent guesswork and prevent promotion drift.

---

## Core rule

No local-runtime signal may be promoted until it is classified here.

If a signal class does not appear in this matrix, it is not promotion-eligible.

---

## Column definitions

| Column | Meaning |
| --- | --- |
| `data_class` | The bounded signal or artifact class being classified |
| `producer` | The service or runtime component that first emits or observes the signal |
| `local_owner` | The system that owns this truth locally |
| `cloud_owner` | The cloud-side owner if promoted |
| `promotion_allowed` | `yes`, `no`, or `conditional` |
| `promotion_trigger` | What condition must occur before promotion is allowed |
| `redaction_class` | Required redaction/privacy handling |
| `dedupe_strategy` | How duplicate or repeated signals are compacted |
| `retention_class` | Retention posture for local/cloud handling |
| `used_for_proposals` | Whether the signal may support proposals in ForgeCommand |
| `offline_required` | Whether the local system must remain fully meaningful without cloud |
| `versioned_contract_required` | Whether promotion requires a reviewed versioned envelope |

---

## Retention classes used in this matrix

| Retention class | Meaning |
| --- | --- |
| `A` | local transient |
| `B` | local durable operational |
| `C` | cloud aggregated short horizon |
| `D` | cloud historical durable |
| `E` | verification archive |

---

## Redaction classes used in this matrix

| Redaction class | Meaning |
| --- | --- |
| `none` | no sensitive content expected |
| `runtime_metadata_only` | runtime/system metadata only |
| `structured_summary_only` | bounded normalized summary only |
| `strict_no_content` | must contain no app/customer/content payloads |
| `forbidden` | must not be promoted |

---

## Matrix

| data_class | producer | local_owner | cloud_owner | promotion_allowed | promotion_trigger | redaction_class | dedupe_strategy | retention_class | used_for_proposals | offline_required | versioned_contract_required |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| df_local.migration_failure | DF Local Foundation | DF Local Foundation | DataForge Cloud | yes | repeated failure, severity threshold, or version-regression suspicion | runtime_metadata_only | dedupe by migration signature + version + correlation window | B/C/D | yes | yes | yes |
| df_local.compatibility_failure | DF Local Foundation | DF Local Foundation | DataForge Cloud | yes | repeated compatibility mismatch or startup-blocking incompatibility | runtime_metadata_only | dedupe by compatibility signature + platform + version window | B/C/D | yes | yes | yes |
| df_local.readiness_transition | DF Local Foundation | DF Local Foundation | DataForge Cloud | conditional | promote only meaningful transitions relevant to fleet diagnosis, false-positive/false-negative analysis, or rollout verification | structured_summary_only | compact repeated transitions by state pair + reason_class + time window | A/B/C | yes | yes | yes |
| df_local.degraded_transition | DF Local Foundation | DF Local Foundation | DataForge Cloud | yes | repeated degraded pattern, severity threshold, or contract-truth concern | structured_summary_only | compact by degraded reason_class + service_version + correlation window | B/C/D | yes | yes | yes |
| df_local.restore_blocked_event | DF Local Foundation | DF Local Foundation | DataForge Cloud | conditional | promote only when repeated, severe, or rollout/compatibility relevant | structured_summary_only | dedupe by restore blocker class + version + environment_class | B/C | yes | yes | yes |
| df_local.backup_export_readiness_posture | DF Local Foundation | DF Local Foundation | DataForge Cloud | conditional | promote only posture changes or repeated fleet-relevant failures | structured_summary_only | compact by posture class + version + time window | A/B/C | yes | yes | yes |
| neuronforge_local.contract_structure_failure_pattern | NeuronForge Local | NeuronForge Local | DataForge Cloud | yes | repeated contract-shape failure or candidate instability cluster | strict_no_content | dedupe by contract id + failure pattern type + model/profile version | B/C/D | yes | yes | yes |
| neuronforge_local.degraded_ai_mode_frequency | NeuronForge Local | NeuronForge Local | DataForge Cloud | conditional | promote only when degradation frequency exceeds threshold or worsens after rollout | strict_no_content | aggregate by lane/profile + environment_class + time window | B/C/D | yes | yes | yes |
| neuronforge_local.lane_local_eval_result | NeuronForge Local | NeuronForge Local | DataForge Cloud | yes | approved eval output marked promotable by doctrine | strict_no_content | dedupe by candidate_id + baseline_id + evaluation_scope | B/D/E | yes | yes | yes |
| neuronforge_local.route_profile_regression_signal | NeuronForge Local | NeuronForge Local | DataForge Cloud | conditional | promote on repeated regression or rollout verification relevance | strict_no_content | dedupe by route/profile id + regression class + version | B/C/D | yes | yes | yes |
| cortex.extraction_completeness_failure | Cortex | Cortex | DataForge Cloud | yes | repeated structural extraction incompleteness pattern | strict_no_content | dedupe by source lane + failure class + extractor version | B/C/D | yes | yes | yes |
| cortex.partial_success_cluster | Cortex | Cortex | DataForge Cloud | yes | repeated partial-success cluster affecting truthfulness or usability | strict_no_content | aggregate by lane + reason_class + version window | B/C/D | yes | yes | yes |
| cortex.freshness_invalidation_failure | Cortex | Cortex | DataForge Cloud | yes | repeated stale/freshness invalidation failure pattern | strict_no_content | dedupe by invalidation class + package type + version | B/C/D | yes | yes | yes |
| cortex.retrieval_package_validity_failure | Cortex | Cortex | DataForge Cloud | conditional | promote when repeated or rollout-regression relevant | strict_no_content | dedupe by package contract + validity failure class + version | B/C/D | yes | yes | yes |
| fa_local.denial_class_anomaly | FA Local | FA Local | DataForge Cloud | yes | repeated denial-class anomaly or false-denial suspicion | strict_no_content | aggregate by denial class + capability + policy version | B/C/D | yes | yes | yes |
| fa_local.false_admission_signal | FA Local | FA Local | DataForge Cloud | conditional | promote only when bounded evidence supports admission-quality defect | strict_no_content | dedupe by capability + false-admission class + version | B/C/D | yes | yes | yes |
| fa_local.false_denial_signal | FA Local | FA Local | DataForge Cloud | conditional | promote only when bounded evidence supports denial-quality defect | strict_no_content | dedupe by capability + false-denial class + version | B/C/D | yes | yes | yes |
| fa_local.execution_governed_fallback_failure | FA Local | FA Local | DataForge Cloud | yes | repeated governed fallback failure or review-handoff breakdown | strict_no_content | dedupe by fallback class + capability + version window | B/C/D | yes | yes | yes |
| app_domain.table_contents | Application | Application | none | no | never | forbidden | n/a | local only | no | yes | n/a |
| app_domain.project_or_manuscript_content | Application | Application | none | no | never | forbidden | n/a | local only | no | yes | n/a |
| app_domain.customer_identity_fields | Application | Application | none | no | never | forbidden | n/a | local only | no | yes | n/a |
| app_domain.semantic_content_summary | Application or service-derived | Application | none | no | never | forbidden | n/a | local only | no | yes | n/a |
| app_domain.raw_log_payload_with_content_risk | Application or service | Application or producing service | none | no | never | forbidden | n/a | local only | no | yes | n/a |
| runtime.cross_fleet_failure_cluster | Derived from promoted artifacts | DataForge Cloud | DataForge Cloud | cloud-canonical only | derived after aggregation, not directly promoted from app truth | structured_summary_only | cluster merge rules in cloud | D | yes | yes | yes |
| runtime.proposal_history | ForgeCommand / DataForge Cloud path | DataForge Cloud | DataForge Cloud | cloud-canonical only | created by review/decision lifecycle | structured_summary_only | proposal id + state transition identity | D/E | yes | yes | yes |
| runtime.rollout_verification_history | rollout verification path | DataForge Cloud | DataForge Cloud | cloud-canonical only | created after approved rollout and revalidation | structured_summary_only | proposal id + cohort + verification window | E | yes | yes | yes |
| runtime.verified_regression_evidence | evaluation / verification path | DataForge Cloud | DataForge Cloud | cloud-canonical only | created after verification confirms regression or improvement | structured_summary_only | regression signature + version window + cohort | D/E | yes | yes | yes |

---

## Initial implementation boundary

The first proving slice is intentionally limited to DF Local Foundation-originated signals only:

- `df_local.migration_failure`
- `df_local.compatibility_failure`
- `df_local.readiness_transition`
- `df_local.degraded_transition`

No other signal classes should be wired for real promotion until this first slice is proven.

---

## Hard reject rules

Promotion must be rejected immediately if a candidate artifact contains or implies:

- app table contents
- manuscript, project, or customer content
- customer identity fields
- app-owned domain truth
- raw extracted content
- free-form payloads that may carry content fragments
- raw prompts or semantic summaries of customer-owned material
- any field outside the reviewed versioned envelope

---

## First follow-on artifacts after this matrix

After this document is accepted, implementation may proceed in this order:

1. promotion envelope schemas
2. runtime-owned outbound promotion queue
3. DF Local proving slice
4. DataForge Cloud intake for bounded promoted artifacts
5. ForgeCommand read surface for promoted fleet-learning evidence

---

## Definition of done for this document

This matrix is considered good enough for Phase 1 when:

- every first-slice DF Local signal is classified
- forbidden classes are explicit
- promotable classes are bounded
- cloud-canonical classes are distinguished from local operational truth
- later schema work can proceed without guessing