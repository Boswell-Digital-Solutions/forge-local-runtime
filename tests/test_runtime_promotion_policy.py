from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime_promotion.db import PromotionQueueDbWriter
from runtime_promotion.normalizer import DefaultPromotionNormalizer
from runtime_promotion.policy import DefaultPromotionPolicyGate
from runtime_promotion.queue import QueueWritePlanner
from runtime_promotion.types import PromotionPolicyDecision, PromotionPolicyOutcome, PromotionQueueStatus


def build_candidate_signal(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "envelope_type": "local_failure_pattern",
        "envelope_version": "v1",
        "producer_version": "1.0.0",
        "runtime_bundle_id": "forge-local-runtime",
        "runtime_bundle_version": "1.0.0",
        "fleet_member_id": "fleet-dev-001",
        "service": "df_local_foundation",
        "observed_at": datetime.now(UTC).isoformat(),
        "dedupe_key": "df-local:migration-failure:v1",
        "retention_class": "C",
        "failure_pattern_type": "migration_failure",
        "frequency_window": "15m",
        "occurrence_count": 3,
        "severity": "high",
        "affected_contract_or_capability": "runtime_promotion_queue",
        "supporting_examples": [
            {
                "example_id": "ex-001",
                "reason_class": "migration_failed",
                "observed_at": datetime.now(UTC).isoformat(),
                "summary": "Migration failed during startup",
            }
        ],
    }
    base.update(overrides)
    return base


class FakeExecutor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        self.calls.append((sql, params))


def test_policy_rejects_banned_top_level_field() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()

    candidate_signal = build_candidate_signal(customer_id="cust-123")

    envelope = normalizer.normalize(candidate_signal)
    decision = policy_gate.decide(envelope)

    assert decision.outcome == PromotionPolicyOutcome.REJECTED
    assert decision.reason_class == "banned_top_level_field_present"


def test_policy_suppresses_single_occurrence_failure_pattern() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()

    candidate_signal = build_candidate_signal(occurrence_count=1)

    envelope = normalizer.normalize(candidate_signal)
    decision = policy_gate.decide(envelope)

    assert decision.outcome == PromotionPolicyOutcome.SUPPRESSED
    assert decision.reason_class == "insufficient_repetition_signal"


def test_policy_accepts_valid_repeated_failure_pattern() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()

    candidate_signal = build_candidate_signal(occurrence_count=4)

    envelope = normalizer.normalize(candidate_signal)
    decision = policy_gate.decide(envelope)

    assert decision.outcome == PromotionPolicyOutcome.ACCEPTED
    assert decision.reason_class == "promotion_policy_gate_pass"


def test_normalizer_moves_non_reserved_fields_into_payload() -> None:
    normalizer = DefaultPromotionNormalizer()

    candidate_signal = build_candidate_signal(
        issue_class="migration_failure",
        promotion_basis="repeated_failure_pattern",
    )

    envelope = normalizer.normalize(candidate_signal)

    assert envelope.payload["issue_class"] == "migration_failure"
    assert envelope.payload["promotion_basis"] == "repeated_failure_pattern"
    assert "service" not in envelope.payload
    assert "dedupe_key" not in envelope.payload


def test_queue_planner_builds_queue_record_for_accepted_decision() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()

    candidate_signal = build_candidate_signal(occurrence_count=4)

    envelope = normalizer.normalize(candidate_signal)
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)

    assert plan.queue_record is not None
    assert plan.queue_record.status == PromotionQueueStatus.QUEUED
    assert plan.queue_record.payload_json["failure_pattern_type"] == "migration_failure"
    assert plan.policy_event["outcome"] == "accepted"


def test_queue_planner_builds_nonqueue_result_for_quarantined_outcome() -> None:
    normalizer = DefaultPromotionNormalizer()
    queue_planner = QueueWritePlanner()

    candidate_signal = build_candidate_signal(occurrence_count=4)
    envelope = normalizer.normalize(candidate_signal)

    decision = PromotionPolicyDecision(
        outcome=PromotionPolicyOutcome.QUARANTINED,
        reason_class="manual_review_required",
        summary="Manual review required before queue write.",
    )

    plan = queue_planner.build_plan(envelope, decision)

    assert plan.queue_record is None
    assert plan.policy_event["outcome"] == "quarantined"


def test_db_writer_writes_artifact_and_policy_event_for_queueable_plan() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()
    db_writer = PromotionQueueDbWriter(queue_planner=queue_planner)
    executor = FakeExecutor()

    envelope = normalizer.normalize(build_candidate_signal(occurrence_count=4))
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)

    result = db_writer.write_plan(executor, plan)

    assert result.artifact_written is True
    assert result.policy_event_written is True
    assert result.artifact_params is not None
    assert len(executor.calls) == 2
    assert "INSERT INTO runtime_promotion.outbound_artifacts" in executor.calls[0][0]
    assert "INSERT INTO runtime_promotion.policy_events" in executor.calls[1][0]


def test_db_writer_writes_only_policy_event_for_nonqueue_plan() -> None:
    normalizer = DefaultPromotionNormalizer()
    queue_planner = QueueWritePlanner()
    db_writer = PromotionQueueDbWriter(queue_planner=queue_planner)
    executor = FakeExecutor()

    envelope = normalizer.normalize(build_candidate_signal(occurrence_count=4))
    decision = PromotionPolicyDecision(
        outcome=PromotionPolicyOutcome.QUARANTINED,
        reason_class="manual_review_required",
        summary="Manual review required before queue write.",
    )
    plan = queue_planner.build_plan(envelope, decision)

    result = db_writer.write_plan(executor, plan)

    assert result.artifact_written is False
    assert result.policy_event_written is True
    assert result.artifact_params is None
    assert len(executor.calls) == 1
    assert "INSERT INTO runtime_promotion.policy_events" in executor.calls[0][0]