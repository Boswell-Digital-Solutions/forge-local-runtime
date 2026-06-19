from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from runtime_promotion.db import PromotionQueueDbWriter
from runtime_promotion.normalizer import DefaultPromotionNormalizer
from runtime_promotion.persistence import RuntimePromotionRepository
from runtime_promotion.policy import DefaultPromotionPolicyGate
from runtime_promotion.queue import QueueWritePlan, QueueWritePlanner
from runtime_promotion.types import PromotionPolicyDecision, PromotionPolicyOutcome

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


class FakeCursor:
    def __init__(self, *, fail_on_call_number: int | None = None) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.fail_on_call_number = fail_on_call_number

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        call_number = len(self.calls) + 1
        if self.fail_on_call_number == call_number:
            raise RuntimeError("simulated DB execute failure")
        self.calls.append((sql, params))


class FakeConnection:
    def __init__(self, *, fail_on_call_number: int | None = None) -> None:
        self._cursor = FakeCursor(fail_on_call_number=fail_on_call_number)
        self.commit_called = False
        self.rollback_called = False

    def cursor(self) -> FakeCursor:
        return self._cursor

    def commit(self) -> None:
        self.commit_called = True

    def rollback(self) -> None:
        self.rollback_called = True


def build_queueable_plan() -> tuple[FakeConnection, QueueWritePlan]:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()

    envelope = normalizer.normalize(build_candidate_signal(occurrence_count=4))
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)

    connection = FakeConnection()
    return connection, plan


def test_repository_commits_on_success_for_queueable_plan() -> None:
    connection, plan = build_queueable_plan()
    repository = RuntimePromotionRepository(
        connection_factory=lambda: connection,
        db_writer=PromotionQueueDbWriter(),
    )

    result = repository.persist_plan(plan)

    assert result.artifact_written is True
    assert result.policy_event_written is True
    assert result.artifact_id is not None
    assert result.queue_status == "queued"
    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert len(connection.cursor().calls) == 2


def test_repository_rolls_back_on_execute_failure() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()

    envelope = normalizer.normalize(build_candidate_signal(occurrence_count=4))
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)

    connection = FakeConnection(fail_on_call_number=2)
    repository = RuntimePromotionRepository(
        connection_factory=lambda: connection,
        db_writer=PromotionQueueDbWriter(),
    )

    try:
        repository.persist_plan(plan)
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as exc:
        assert str(exc) == "simulated DB execute failure"

    assert connection.commit_called is False
    assert connection.rollback_called is True


def test_repository_persists_only_policy_event_for_nonqueueable_plan() -> None:
    normalizer = DefaultPromotionNormalizer()
    queue_planner = QueueWritePlanner()

    envelope = normalizer.normalize(build_candidate_signal(occurrence_count=4))
    decision = PromotionPolicyDecision(
        outcome=PromotionPolicyOutcome.QUARANTINED,
        reason_class="manual_review_required",
        summary="Manual review required before queue write.",
    )
    plan = queue_planner.build_plan(envelope, decision)

    connection = FakeConnection()
    repository = RuntimePromotionRepository(
        connection_factory=lambda: connection,
        db_writer=PromotionQueueDbWriter(),
    )

    result = repository.persist_plan(plan)

    assert result.artifact_written is False
    assert result.policy_event_written is True
    assert result.artifact_id is None
    assert result.queue_status is None
    assert connection.commit_called is True
    assert connection.rollback_called is False
    assert len(connection.cursor().calls) == 1
    assert "INSERT INTO runtime_promotion.policy_events" in connection.cursor().calls[0][0]