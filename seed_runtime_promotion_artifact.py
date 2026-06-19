from __future__ import annotations

from datetime import UTC, datetime

from runtime_promotion.connection import create_connection
from runtime_promotion.normalizer import DefaultPromotionNormalizer
from runtime_promotion.persistence import RuntimePromotionRepository
from runtime_promotion.policy import DefaultPromotionPolicyGate
from runtime_promotion.queue import QueueWritePlanner


def build_candidate_signal() -> dict[str, object]:
    now = datetime.now(UTC).isoformat()
    return {
        "envelope_type": "local_failure_pattern",
        "envelope_version": "v1",
        "producer_version": "1.0.0",
        "runtime_bundle_id": "forge-local-runtime",
        "runtime_bundle_version": "1.0.0",
        "fleet_member_id": "fleet-dev-001",
        "service": "df_local_foundation",
        "observed_at": now,
        "dedupe_key": f"df-local:e2e-proof:{now}",
        "retention_class": "C",
        "failure_pattern_type": "migration_failure",
        "frequency_window": "15m",
        "occurrence_count": 4,
        "severity": "high",
        "affected_contract_or_capability": "runtime_promotion_queue",
        "supporting_examples": [
            {
                "example_id": "ex-e2e-001",
                "reason_class": "migration_failed",
                "observed_at": now,
                "summary": "Migration failed during startup",
            }
        ],
    }


def main() -> None:
    normalizer = DefaultPromotionNormalizer()
    policy_gate = DefaultPromotionPolicyGate()
    queue_planner = QueueWritePlanner()
    repository = RuntimePromotionRepository(connection_factory=create_connection)

    envelope = normalizer.normalize(build_candidate_signal())
    decision = policy_gate.decide(envelope)
    plan = queue_planner.build_plan(envelope, decision)
    result = repository.persist_plan(plan)

    print("artifact_written =", result.artifact_written)
    print("policy_event_written =", result.policy_event_written)
    print("artifact_id =", result.artifact_id)
    print("policy_event_id =", result.policy_event_id)
    print("queue_status =", result.queue_status)
    print("dedupe_key =", envelope.dedupe_key)


if __name__ == "__main__":
    main()