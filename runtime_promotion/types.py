from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Protocol


class PromotionEnvelopeType(StrEnum):
    LOCAL_STATE_EVENT = "local_state_event"
    LOCAL_FAILURE_PATTERN = "local_failure_pattern"
    LOCAL_IMPROVEMENT_EVAL_RESULT = "local_improvement_eval_result"
    PROMOTION_READY_EVIDENCE_BUNDLE = "promotion_ready_evidence_bundle"
    LOCAL_ROLLOUT_VERIFICATION_RESULT = "local_rollout_verification_result"


class PromotionQueueStatus(StrEnum):
    QUEUED = "queued"
    RETRY_SCHEDULED = "retry_scheduled"
    DELIVERY_IN_PROGRESS = "delivery_in_progress"
    SUPPRESSED = "suppressed"
    REJECTED = "rejected"
    EXPIRED = "expired"
    DELIVERED = "delivered"
    DELIVERY_FAILED = "delivery_failed"


class PromotionPolicyOutcome(StrEnum):
    ACCEPTED = "accepted"
    QUEUED = "queued"
    RETRY_SCHEDULED = "retry_scheduled"
    SUPPRESSED = "suppressed"
    REJECTED = "rejected"
    EXPIRED = "expired"
    DELIVERED = "delivered"
    DELIVERY_FAILED = "delivery_failed"
    QUARANTINED = "quarantined"


class PromotionEventType(StrEnum):
    NORMALIZATION = "normalization"
    POLICY_GATE = "policy_gate"
    QUEUE_WRITE = "queue_write"
    TRANSPORT = "transport"
    DELIVERY_ACK = "delivery_ack"
    EXPIRY = "expiry"


@dataclass(frozen=True, slots=True)
class PromotionEnvelope:
    envelope_type: PromotionEnvelopeType
    envelope_version: str
    producer_version: str
    runtime_bundle_id: str
    runtime_bundle_version: str
    fleet_member_id: str
    service: str
    observed_at: datetime
    dedupe_key: str
    retention_class: str
    payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class PromotionPolicyDecision:
    outcome: PromotionPolicyOutcome
    reason_class: str
    summary: str | None = None
    next_attempt_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class PromotionQueueRecord:
    artifact_id: str
    envelope_type: PromotionEnvelopeType
    envelope_version: str
    service: str
    fleet_member_id: str
    dedupe_key: str
    payload_json: dict[str, Any]
    status: PromotionQueueStatus
    delivery_attempt_count: int
    first_observed_at: datetime
    last_attempted_at: datetime | None = None
    next_attempt_at: datetime | None = None
    expires_at: datetime | None = None
    acknowledged_at: datetime | None = None
    rejection_reason_class: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PromotionNormalizer(Protocol):
    def normalize(self, candidate_signal: dict[str, Any]) -> PromotionEnvelope: ...


class PromotionPolicyGate(Protocol):
    def decide(self, envelope: PromotionEnvelope) -> PromotionPolicyDecision: ...