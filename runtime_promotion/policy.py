from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Mapping, Sequence

from runtime_promotion.types import (
    PromotionEnvelope,
    PromotionPolicyDecision,
    PromotionPolicyGate,
    PromotionPolicyOutcome,
)


BANNED_TOP_LEVEL_FIELDS = {
    "customer_id",
    "customer_name",
    "customer_email",
    "user_id",
    "user_email",
    "project_id",
    "project_name",
    "manuscript_id",
    "manuscript_title",
    "document_content",
    "raw_content",
    "prompt_text",
    "semantic_summary",
    "table_contents",
}

BANNED_NESTED_FIELD_FRAGMENTS = {
    "customer",
    "manuscript",
    "document_content",
    "raw_content",
    "prompt",
    "semantic_summary",
    "table_contents",
}


@dataclass(frozen=True, slots=True)
class DefaultPromotionPolicyGate(PromotionPolicyGate):
    """
    First-pass governed policy gate.

    Current behavior is intentionally narrow and conservative:
    - reject malformed envelopes
    - reject banned top-level or nested content-bearing fields
    - suppress very low-value single-occurrence signals
    - accept bounded runtime-oriented artifacts
    """

    retry_delay_minutes: int = 15

    def decide(self, envelope: PromotionEnvelope) -> PromotionPolicyDecision:
        required_check = self._check_required_fields(envelope)
        if required_check is not None:
            return required_check

        banned_check = self._check_banned_fields(envelope.payload)
        if banned_check is not None:
            return banned_check

        occurrence_count = self._extract_occurrence_count(envelope.payload)
        if occurrence_count == 1 and envelope.envelope_type.value in {
            "local_failure_pattern",
            "promotion_ready_evidence_bundle",
        }:
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.SUPPRESSED,
                reason_class="insufficient_repetition_signal",
                summary="Single-occurrence artifact suppressed pending stronger repeated evidence.",
            )

        return PromotionPolicyDecision(
            outcome=PromotionPolicyOutcome.ACCEPTED,
            reason_class="promotion_policy_gate_pass",
            summary="Envelope passed first-pass policy checks.",
        )

    def build_retry_decision(
        self,
        reason_class: str,
        summary: str | None = None,
    ) -> PromotionPolicyDecision:
        return PromotionPolicyDecision(
            outcome=PromotionPolicyOutcome.RETRY_SCHEDULED,
            reason_class=reason_class,
            summary=summary,
            next_attempt_at=datetime.now(UTC) + timedelta(minutes=self.retry_delay_minutes),
        )

    def _check_required_fields(
        self,
        envelope: PromotionEnvelope,
    ) -> PromotionPolicyDecision | None:
        if not envelope.envelope_version.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_envelope_version",
                summary="Envelope version is required.",
            )

        if not envelope.producer_version.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_producer_version",
                summary="Producer version is required.",
            )

        if not envelope.runtime_bundle_id.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_runtime_bundle_id",
                summary="Runtime bundle id is required.",
            )

        if not envelope.runtime_bundle_version.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_runtime_bundle_version",
                summary="Runtime bundle version is required.",
            )

        if not envelope.fleet_member_id.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_fleet_member_id",
                summary="Fleet member id is required.",
            )

        if not envelope.service.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_service",
                summary="Service is required.",
            )

        if not envelope.dedupe_key.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_dedupe_key",
                summary="Dedupe key is required.",
            )

        if not envelope.retention_class.strip():
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="missing_retention_class",
                summary="Retention class is required.",
            )

        return None

    def _check_banned_fields(
        self,
        payload: dict[str, Any],
    ) -> PromotionPolicyDecision | None:
        top_level_hit = BANNED_TOP_LEVEL_FIELDS.intersection(payload.keys())
        if top_level_hit:
            field_name = sorted(top_level_hit)[0]
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="banned_top_level_field_present",
                summary=f"Banned field present in payload: {field_name}",
            )

        nested_hit = self._find_banned_nested_field(payload)
        if nested_hit is not None:
            return PromotionPolicyDecision(
                outcome=PromotionPolicyOutcome.REJECTED,
                reason_class="banned_nested_field_present",
                summary=f"Banned nested field present in payload: {nested_hit}",
            )

        return None

    def _find_banned_nested_field(
        self,
        value: object,
        prefix: str = "",
    ) -> str | None:
        if isinstance(value, Mapping):
            for key, nested_value in value.items():
                if not isinstance(key, str):
                    continue

                path = f"{prefix}.{key}" if prefix else key
                lowered_key = key.lower()

                if lowered_key in BANNED_TOP_LEVEL_FIELDS:
                    return path

                if any(fragment in lowered_key for fragment in BANNED_NESTED_FIELD_FRAGMENTS):
                    return path

                found = self._find_banned_nested_field(nested_value, path)
                if found is not None:
                    return found

            return None

        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            for index, item in enumerate(value):
                path = f"{prefix}[{index}]"
                found = self._find_banned_nested_field(item, path)
                if found is not None:
                    return found

            return None

        return None

    def _extract_occurrence_count(self, payload: dict[str, Any]) -> int:
        raw_value = payload.get("occurrence_count", 0)
        if isinstance(raw_value, int):
            return raw_value
        return 0