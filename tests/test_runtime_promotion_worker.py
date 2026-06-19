from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime

from runtime_promotion.worker import ClaimedArtifact, PromotionDeliveryWorker


ArtifactRow = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    dict[str, object],
    str,
    int,
    datetime,
    datetime | None,
    datetime | None,
    datetime | None,
    datetime | None,
    str | None,
    datetime,
    datetime,
]


class FakeWorkerCursor:
    def __init__(self, *, rows: Sequence[ArtifactRow] | None = None) -> None:
        self.rows: list[ArtifactRow] = list(rows) if rows is not None else []
        self.calls: list[tuple[str, dict[str, object]]] = []

    def execute(self, sql: str, params: dict[str, object] | None = None) -> None:
        self.calls.append((sql, params or {}))

    def fetchall(self) -> list[ArtifactRow]:
        return self.rows


class FakeWorkerConnection:
    def __init__(self, *, rows: Sequence[ArtifactRow] | None = None) -> None:
        self._cursor = FakeWorkerCursor(rows=rows)
        self.commit_called = False
        self.rollback_called = False

    def cursor(self) -> FakeWorkerCursor:
        return self._cursor

    def commit(self) -> None:
        self.commit_called = True

    def rollback(self) -> None:
        self.rollback_called = True


class StubSuccessWorker(PromotionDeliveryWorker):
    def _post_to_dataforge(self, artifact: ClaimedArtifact) -> None:
        return None


class StubFailureWorker(PromotionDeliveryWorker):
    def _post_to_dataforge(self, artifact: ClaimedArtifact) -> None:
        raise RuntimeError("DataForge unavailable")


def build_claimed_artifact(
    *,
    artifact_id: str = "artifact-001",
    envelope_type: str = "local_failure_pattern",
    envelope_version: str = "v1",
    service: str = "df_local_foundation",
    fleet_member_id: str = "fleet-dev-001",
    dedupe_key: str = "df-local:migration-failure:v1",
    payload_json: dict[str, object] | None = None,
    status: str = "delivery_in_progress",
    delivery_attempt_count: int = 1,
    first_observed_at: datetime | None = None,
    last_attempted_at: datetime | None = None,
    next_attempt_at: datetime | None = None,
    expires_at: datetime | None = None,
    acknowledged_at: datetime | None = None,
    rejection_reason_class: str | None = None,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> ClaimedArtifact:
    now = datetime.now(UTC)

    return ClaimedArtifact(
        artifact_id=artifact_id,
        envelope_type=envelope_type,
        envelope_version=envelope_version,
        service=service,
        fleet_member_id=fleet_member_id,
        dedupe_key=dedupe_key,
        payload_json=payload_json
        if payload_json is not None
        else {
            "failure_pattern_type": "migration_failure",
            "severity": "high",
        },
        status=status,
        delivery_attempt_count=delivery_attempt_count,
        first_observed_at=first_observed_at or now,
        last_attempted_at=last_attempted_at or now,
        next_attempt_at=next_attempt_at,
        expires_at=expires_at,
        acknowledged_at=acknowledged_at,
        rejection_reason_class=rejection_reason_class,
        created_at=created_at or now,
        updated_at=updated_at or now,
    )


def test_claim_ready_artifacts_maps_rows_into_claimed_artifacts() -> None:
    observed_at = datetime.now(UTC)
    attempted_at = datetime.now(UTC)
    created_at = datetime.now(UTC)
    updated_at = datetime.now(UTC)

    rows: list[ArtifactRow] = [
        (
            "artifact-claim-001",
            "local_failure_pattern",
            "v1",
            "df_local_foundation",
            "fleet-dev-001",
            "df-local:migration-failure:v1",
            {"failure_pattern_type": "migration_failure"},
            "delivery_in_progress",
            1,
            observed_at,
            attempted_at,
            None,
            None,
            None,
            None,
            created_at,
            updated_at,
        )
    ]

    connection = FakeWorkerConnection(rows=rows)
    worker = PromotionDeliveryWorker()

    claimed = worker.claim_ready_artifacts(connection, limit=5)

    assert len(claimed) == 1
    assert claimed[0].artifact_id == "artifact-claim-001"
    assert claimed[0].envelope_type == "local_failure_pattern"
    assert claimed[0].service == "df_local_foundation"
    assert claimed[0].status == "delivery_in_progress"
    assert claimed[0].delivery_attempt_count == 1

    cursor = connection.cursor()
    assert len(cursor.calls) == 1
    assert "claim_ready_artifacts" in cursor.calls[0][0]
    assert cursor.calls[0][1] == {"limit": 5}


def test_deliver_claimed_artifact_marks_delivered_by_default() -> None:
    connection = FakeWorkerConnection()
    worker = StubSuccessWorker()
    artifact = build_claimed_artifact(
        payload_json={
            "failure_pattern_type": "migration_failure",
            "severity": "high",
        }
    )

    result = worker.deliver_claimed_artifact(connection, artifact)

    assert result.artifact_id == artifact.artifact_id
    assert result.action == "delivered"
    assert result.reason_class is None

    cursor = connection.cursor()
    assert len(cursor.calls) == 1
    assert "mark_delivered" in cursor.calls[0][0]
    assert cursor.calls[0][1]["artifact_id"] == artifact.artifact_id
    assert cursor.calls[0][1]["acknowledged_at"] is not None


def test_deliver_claimed_artifact_schedules_retry_on_simulated_failure() -> None:
    connection = FakeWorkerConnection()
    worker = PromotionDeliveryWorker()
    artifact = build_claimed_artifact(
        payload_json={
            "failure_pattern_type": "migration_failure",
            "severity": "high",
            "simulate_delivery_failure": True,
        }
    )

    result = worker.deliver_claimed_artifact(connection, artifact)

    assert result.artifact_id == artifact.artifact_id
    assert result.action == "retry_scheduled"
    assert result.reason_class == "simulated_delivery_failure"

    cursor = connection.cursor()
    assert len(cursor.calls) == 1
    assert "release_claim_for_retry" in cursor.calls[0][0]
    assert cursor.calls[0][1]["artifact_id"] == artifact.artifact_id
    assert cursor.calls[0][1]["reason_class"] == "simulated_delivery_failure"
    assert cursor.calls[0][1]["next_attempt_at"] is not None


def test_deliver_claimed_artifact_schedules_retry_when_dataforge_delivery_fails() -> None:
    connection = FakeWorkerConnection()
    worker = StubFailureWorker()
    artifact = build_claimed_artifact(
        payload_json={
            "failure_pattern_type": "migration_failure",
            "severity": "high",
        }
    )

    result = worker.deliver_claimed_artifact(connection, artifact)

    assert result.artifact_id == artifact.artifact_id
    assert result.action == "retry_scheduled"
    assert result.reason_class == "dataforge_delivery_failed"

    cursor = connection.cursor()
    assert len(cursor.calls) == 1
    assert "release_claim_for_retry" in cursor.calls[0][0]
    assert cursor.calls[0][1]["artifact_id"] == artifact.artifact_id
    assert cursor.calls[0][1]["reason_class"] == "dataforge_delivery_failed"
    assert cursor.calls[0][1]["next_attempt_at"] is not None