from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from runtime_promotion.types import (
    PromotionEnvelope,
    PromotionEnvelopeType,
    PromotionNormalizer,
)


ENVELOPE_TYPE_MAP: dict[str, PromotionEnvelopeType] = {
    "local_state_event": PromotionEnvelopeType.LOCAL_STATE_EVENT,
    "local_failure_pattern": PromotionEnvelopeType.LOCAL_FAILURE_PATTERN,
    "local_improvement_eval_result": PromotionEnvelopeType.LOCAL_IMPROVEMENT_EVAL_RESULT,
    "promotion_ready_evidence_bundle": PromotionEnvelopeType.PROMOTION_READY_EVIDENCE_BUNDLE,
    "local_rollout_verification_result": PromotionEnvelopeType.LOCAL_ROLLOUT_VERIFICATION_RESULT,
}


@dataclass(frozen=True, slots=True)
class DefaultPromotionNormalizer(PromotionNormalizer):
    """
    First-pass normalizer for bounded candidate signals.

    Current posture:
    - require the common envelope fields
    - coerce envelope_type into the PromotionEnvelopeType enum
    - keep all non-envelope fields inside payload
    - reject malformed or incomplete candidate signals early
    """

    def normalize(self, candidate_signal: dict[str, Any]) -> PromotionEnvelope:
        self._require_mapping(candidate_signal)

        envelope_type = self._parse_envelope_type(candidate_signal.get("envelope_type"))
        envelope_version = self._require_str(candidate_signal, "envelope_version")
        producer_version = self._require_str(candidate_signal, "producer_version")
        runtime_bundle_id = self._require_str(candidate_signal, "runtime_bundle_id")
        runtime_bundle_version = self._require_str(candidate_signal, "runtime_bundle_version")
        fleet_member_id = self._require_str(candidate_signal, "fleet_member_id")
        service = self._require_str(candidate_signal, "service")
        observed_at = self._require_datetime(candidate_signal, "observed_at")
        dedupe_key = self._require_str(candidate_signal, "dedupe_key")
        retention_class = self._require_str(candidate_signal, "retention_class")

        payload = self._build_payload(candidate_signal)

        return PromotionEnvelope(
            envelope_type=envelope_type,
            envelope_version=envelope_version,
            producer_version=producer_version,
            runtime_bundle_id=runtime_bundle_id,
            runtime_bundle_version=runtime_bundle_version,
            fleet_member_id=fleet_member_id,
            service=service,
            observed_at=observed_at,
            dedupe_key=dedupe_key,
            retention_class=retention_class,
            payload=payload,
        )

    def _require_mapping(self, candidate_signal: object) -> None:
        if not isinstance(candidate_signal, Mapping):
            raise ValueError("candidate_signal must be a mapping")

    def _parse_envelope_type(self, raw_value: object) -> PromotionEnvelopeType:
        if not isinstance(raw_value, str) or not raw_value.strip():
            raise ValueError("envelope_type is required")

        normalized = raw_value.strip()
        if normalized not in ENVELOPE_TYPE_MAP:
            raise ValueError(f"unsupported envelope_type: {normalized}")

        return ENVELOPE_TYPE_MAP[normalized]

    def _require_str(self, candidate_signal: Mapping[str, Any], field_name: str) -> str:
        raw_value = candidate_signal.get(field_name)

        if not isinstance(raw_value, str):
            raise ValueError(f"{field_name} must be a string")

        normalized = raw_value.strip()
        if not normalized:
            raise ValueError(f"{field_name} must not be empty")

        return normalized

    def _require_datetime(self, candidate_signal: Mapping[str, Any], field_name: str) -> datetime:
        raw_value = candidate_signal.get(field_name)

        if isinstance(raw_value, datetime):
            return raw_value

        if isinstance(raw_value, str):
            normalized = raw_value.strip()
            if not normalized:
                raise ValueError(f"{field_name} must not be empty")

            try:
                return datetime.fromisoformat(normalized.replace("Z", "+00:00"))
            except ValueError as exc:
                raise ValueError(f"{field_name} must be ISO-8601 parseable") from exc

        raise ValueError(f"{field_name} must be a datetime or ISO-8601 string")

    def _build_payload(self, candidate_signal: Mapping[str, Any]) -> dict[str, Any]:
        reserved_fields = {
            "envelope_type",
            "envelope_version",
            "producer_version",
            "runtime_bundle_id",
            "runtime_bundle_version",
            "fleet_member_id",
            "service",
            "observed_at",
            "dedupe_key",
            "retention_class",
        }

        payload: dict[str, Any] = {}
        for key, value in candidate_signal.items():
            if key in reserved_fields:
                continue
            payload[key] = value

        return payload