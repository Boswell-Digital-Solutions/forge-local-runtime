from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from runtime_promotion.connection import create_connection
from runtime_promotion.db import PromotionQueueDbWriter
from runtime_promotion.normalizer import DefaultPromotionNormalizer
from runtime_promotion.persistence import RuntimePromotionRepository
from runtime_promotion.policy import DefaultPromotionPolicyGate
from runtime_promotion.queue import QueueWritePlanner


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
        "dedupe_key": f"df-local:migration-failure:{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
        "retention_class": "C",
        "failure_pattern_type": "migration_failure",
        "frequency_window": "15m",
        "occurrence_count": 4,
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
        "promotion_basis": "repeated_failure_pattern",
        "issue_class": "migration_failure",
    }
    base.update(overrides)
    return base


def main() -> None:
    candidate_signal = build_candidate_signal(
        simulate_delivery_failure=True,
    )

    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()
    db_writer = PromotionQueueDbWriter()
    repository = RuntimePromotionRepository(
        connection_factory=create_connection,
        db_writer=db_writer,
    )

    envelope = normalizer.normalize(candidate_signal)
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)
    persist_result = repository.persist_plan(plan)

    output: dict[str, Any] = {
        "candidate_signal": candidate_signal,
        "normalized_envelope": {
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
            "payload": envelope.payload,
        },
        "policy_decision": {
            "outcome": decision.outcome.value,
            "reason_class": decision.reason_class,
            "summary": decision.summary,
            "next_attempt_at": (
                decision.next_attempt_at.isoformat()
                if decision.next_attempt_at is not None
                else None
            ),
        },
        "queue_record_present": plan.queue_record is not None,
        "persist_result": {
            "artifact_written": persist_result.artifact_written,
            "policy_event_written": persist_result.policy_event_written,
            "artifact_id": persist_result.artifact_id,
            "policy_event_id": persist_result.policy_event_id,
            "queue_status": persist_result.queue_status,
        },
    }

    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()