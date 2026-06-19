from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4

from runtime_promotion.types import (
    PromotionEnvelope,
    PromotionPolicyDecision,
    PromotionPolicyOutcome,
    PromotionQueueRecord,
    PromotionQueueStatus,
)


@dataclass(frozen=True, slots=True)
class QueueWritePlan:
    queue_record: PromotionQueueRecord | None
    policy_event: dict[str, Any]


class QueueWritePlanner:
    """
    First-pass queue write planner.

    Current responsibility:
    - convert an accepted or queueable policy decision into a queue record
    - convert non-queue outcomes into a policy-event-only result
    - keep DB-writing concerns out of the decision and normalization layer
    """

    def build_plan(
        self,
        envelope: PromotionEnvelope,
        decision: PromotionPolicyDecision,
    ) -> QueueWritePlan:
        artifact_id = self._build_artifact_id()
        now = datetime.now(envelope.observed_at.tzinfo)

        queue_status = self._map_outcome_to_queue_status(decision.outcome)

        if queue_status is None:
            return QueueWritePlan(
                queue_record=None,
                policy_event=self._build_policy_event(
                    artifact_id=artifact_id,
                    envelope=envelope,
                    decision=decision,
                    created_at=now,
                ),
            )

        queue_record = PromotionQueueRecord(
            artifact_id=artifact_id,
            envelope_type=envelope.envelope_type,
            envelope_version=envelope.envelope_version,
            service=envelope.service,
            fleet_member_id=envelope.fleet_member_id,
            dedupe_key=envelope.dedupe_key,
            payload_json=self._build_payload_json(envelope),
            status=queue_status,
            delivery_attempt_count=0,
            first_observed_at=envelope.observed_at,
            last_attempted_at=None,
            next_attempt_at=decision.next_attempt_at,
            expires_at=None,
            acknowledged_at=None,
            rejection_reason_class=(
                None
                if decision.outcome in {PromotionPolicyOutcome.ACCEPTED, PromotionPolicyOutcome.QUEUED}
                else decision.reason_class
            ),
            created_at=now,
            updated_at=now,
        )

        return QueueWritePlan(
            queue_record=queue_record,
            policy_event=self._build_policy_event(
                artifact_id=artifact_id,
                envelope=envelope,
                decision=decision,
                created_at=now,
            ),
        )

    def to_insert_params(self, queue_record: PromotionQueueRecord) -> dict[str, Any]:
        return {
            "artifact_id": queue_record.artifact_id,
            "envelope_type": queue_record.envelope_type.value,
            "envelope_version": queue_record.envelope_version,
            "service": queue_record.service,
            "fleet_member_id": queue_record.fleet_member_id,
            "dedupe_key": queue_record.dedupe_key,
            "payload_json": json.dumps(queue_record.payload_json),
            "status": queue_record.status.value,
            "delivery_attempt_count": queue_record.delivery_attempt_count,
            "first_observed_at": queue_record.first_observed_at,
            "last_attempted_at": queue_record.last_attempted_at,
            "next_attempt_at": queue_record.next_attempt_at,
            "expires_at": queue_record.expires_at,
            "acknowledged_at": queue_record.acknowledged_at,
            "rejection_reason_class": queue_record.rejection_reason_class,
            "created_at": queue_record.created_at,
            "updated_at": queue_record.updated_at,
        }

    def _build_artifact_id(self) -> str:
        return f"artifact-{uuid4()}"

    def _map_outcome_to_queue_status(
        self,
        outcome: PromotionPolicyOutcome,
    ) -> PromotionQueueStatus | None:
        if outcome in {PromotionPolicyOutcome.ACCEPTED, PromotionPolicyOutcome.QUEUED}:
            return PromotionQueueStatus.QUEUED

        if outcome == PromotionPolicyOutcome.RETRY_SCHEDULED:
            return PromotionQueueStatus.RETRY_SCHEDULED

        if outcome == PromotionPolicyOutcome.SUPPRESSED:
            return PromotionQueueStatus.SUPPRESSED

        if outcome == PromotionPolicyOutcome.REJECTED:
            return PromotionQueueStatus.REJECTED

        if outcome == PromotionPolicyOutcome.EXPIRED:
            return PromotionQueueStatus.EXPIRED

        if outcome == PromotionPolicyOutcome.DELIVERED:
            return PromotionQueueStatus.DELIVERED

        if outcome == PromotionPolicyOutcome.DELIVERY_FAILED:
            return PromotionQueueStatus.DELIVERY_FAILED

        return None

    def _build_payload_json(self, envelope: PromotionEnvelope) -> dict[str, Any]:
        return {
            "envelope_type": envelope.envelope_type.value,
            "envelope_version": envelope.envelope_version,
            "producer_version": envelope.producer_version,
            "runtime_bundle_id": envelope.runtime_bundle_id,
            "runtime_bundle_version": envelope.runtime_bundle_version,
            "fleet_member_id": envelope.fleet_member_id,
            "service": envelope.service,
            "observed_at": envelope.observed_at.isoformat(),
            "dedupe_key": envelope.dedupe_key,
            "retention_class": envelope.retention_class,
            **envelope.payload,
        }

    def _build_policy_event(
        self,
        *,
        artifact_id: str,
        envelope: PromotionEnvelope,
        decision: PromotionPolicyDecision,
        created_at: datetime,
    ) -> dict[str, Any]:
        return {
            "policy_event_id": f"policy-{uuid4()}",
            "artifact_id": artifact_id,
            "envelope_type": envelope.envelope_type.value,
            "service": envelope.service,
            "fleet_member_id": envelope.fleet_member_id,
            "event_type": "policy_gate",
            "outcome": decision.outcome.value,
            "reason_class": decision.reason_class,
            "summary": decision.summary,
            "created_at": created_at,
        }