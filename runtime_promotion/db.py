from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from runtime_promotion.queue import QueueWritePlan, QueueWritePlanner


@dataclass(frozen=True, slots=True)
class QueueWriteResult:
    artifact_written: bool
    policy_event_written: bool
    artifact_params: dict[str, Any] | None
    policy_event_params: dict[str, Any]


class DbExecutor(Protocol):
    def execute(self, sql: str, params: dict[str, Any]) -> None: ...


class PromotionQueueDbWriter:
    """
    First-pass DB write adapter.

    Current responsibility:
    - turn a QueueWritePlan into SQL parameter payloads
    - write outbound artifact rows when present
    - always write a policy event row
    - keep SQL text in one place so later DB integration is cleaner
    """

    INSERT_OUTBOUND_ARTIFACT_SQL = """
    INSERT INTO runtime_promotion.outbound_artifacts (
        artifact_id,
        envelope_type,
        envelope_version,
        service,
        fleet_member_id,
        dedupe_key,
        payload_json,
        status,
        delivery_attempt_count,
        first_observed_at,
        last_attempted_at,
        next_attempt_at,
        expires_at,
        acknowledged_at,
        rejection_reason_class,
        created_at,
        updated_at
    ) VALUES (
        %(artifact_id)s,
        %(envelope_type)s,
        %(envelope_version)s,
        %(service)s,
        %(fleet_member_id)s,
        %(dedupe_key)s,
        %(payload_json)s::jsonb,
        %(status)s,
        %(delivery_attempt_count)s,
        %(first_observed_at)s,
        %(last_attempted_at)s,
        %(next_attempt_at)s,
        %(expires_at)s,
        %(acknowledged_at)s,
        %(rejection_reason_class)s,
        %(created_at)s,
        %(updated_at)s
    )
    """

    INSERT_POLICY_EVENT_SQL = """
    INSERT INTO runtime_promotion.policy_events (
        policy_event_id,
        artifact_id,
        envelope_type,
        service,
        fleet_member_id,
        event_type,
        outcome,
        reason_class,
        summary,
        created_at
    ) VALUES (
        %(policy_event_id)s,
        %(artifact_id)s,
        %(envelope_type)s,
        %(service)s,
        %(fleet_member_id)s,
        %(event_type)s,
        %(outcome)s,
        %(reason_class)s,
        %(summary)s,
        %(created_at)s
    )
    """

    def __init__(self, queue_planner: QueueWritePlanner | None = None) -> None:
        self._queue_planner = queue_planner or QueueWritePlanner()

    def build_write_result(self, plan: QueueWritePlan) -> QueueWriteResult:
        artifact_params = None
        artifact_written = False

        if plan.queue_record is not None:
            artifact_params = self._queue_planner.to_insert_params(plan.queue_record)
            artifact_written = True

        return QueueWriteResult(
            artifact_written=artifact_written,
            policy_event_written=True,
            artifact_params=artifact_params,
            policy_event_params=plan.policy_event,
        )

    def write_plan(self, executor: DbExecutor, plan: QueueWritePlan) -> QueueWriteResult:
        result = self.build_write_result(plan)

        if result.artifact_params is not None:
            executor.execute(self.INSERT_OUTBOUND_ARTIFACT_SQL, result.artifact_params)

        executor.execute(self.INSERT_POLICY_EVENT_SQL, result.policy_event_params)

        return result