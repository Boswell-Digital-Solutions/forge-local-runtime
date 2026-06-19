from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import json
from typing import Any, Protocol, cast, runtime_checkable
from urllib import error, request

from runtime_promotion.persistence import DbConnection


DATAFORGE_RECEIPT_URL = (
    "http://127.0.0.1:8001/api/v1/runtime-promotion/receipts/local-failure-pattern"
)


@runtime_checkable
class WorkerCursor(Protocol):
    def execute(self, sql: str, params: dict[str, Any] | None = None) -> None: ...
    def fetchall(self) -> list[tuple[Any, ...]]: ...


@dataclass(frozen=True, slots=True)
class ClaimedArtifact:
    artifact_id: str
    envelope_type: str
    envelope_version: str
    service: str
    fleet_member_id: str
    dedupe_key: str
    payload_json: dict[str, Any]
    status: str
    delivery_attempt_count: int
    first_observed_at: datetime
    last_attempted_at: datetime | None
    next_attempt_at: datetime | None
    expires_at: datetime | None
    acknowledged_at: datetime | None
    rejection_reason_class: str | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    artifact_id: str
    action: str
    reason_class: str | None = None


class PromotionDeliveryWorker:
    CLAIM_SQL = """
    SELECT *
    FROM runtime_promotion.claim_ready_artifacts(%(limit)s)
    """

    MARK_DELIVERED_SQL = """
    SELECT runtime_promotion.mark_delivered(
        %(artifact_id)s,
        %(acknowledged_at)s
    )
    """

    RELEASE_FOR_RETRY_SQL = """
    SELECT runtime_promotion.release_claim_for_retry(
        %(artifact_id)s,
        %(next_attempt_at)s,
        %(reason_class)s
    )
    """

    def claim_ready_artifacts(
        self,
        connection: DbConnection,
        limit: int = 10,
    ) -> list[ClaimedArtifact]:
        cursor = connection.cursor()
        worker_cursor = cursor
        assert isinstance(worker_cursor, WorkerCursor)

        worker_cursor.execute(self.CLAIM_SQL, {"limit": limit})
        rows = worker_cursor.fetchall()

        claimed: list[ClaimedArtifact] = []
        for row in rows:
            claimed.append(
                ClaimedArtifact(
                    artifact_id=row[0],
                    envelope_type=row[1],
                    envelope_version=row[2],
                    service=row[3],
                    fleet_member_id=row[4],
                    dedupe_key=row[5],
                    payload_json=row[6],
                    status=row[7],
                    delivery_attempt_count=row[8],
                    first_observed_at=row[9],
                    last_attempted_at=row[10],
                    next_attempt_at=row[11],
                    expires_at=row[12],
                    acknowledged_at=row[13],
                    rejection_reason_class=row[14],
                    created_at=row[15],
                    updated_at=row[16],
                )
            )

        return claimed

    def deliver_claimed_artifact(
        self,
        connection: DbConnection,
        artifact: ClaimedArtifact,
    ) -> DeliveryResult:
        simulate_failure = bool(artifact.payload_json.get("simulate_delivery_failure", False))

        cursor = connection.cursor()
        worker_cursor = cursor
        assert isinstance(worker_cursor, WorkerCursor)

        if simulate_failure:
            next_attempt_at = datetime.now(UTC) + timedelta(minutes=15)
            worker_cursor.execute(
                self.RELEASE_FOR_RETRY_SQL,
                {
                    "artifact_id": artifact.artifact_id,
                    "next_attempt_at": next_attempt_at,
                    "reason_class": "simulated_delivery_failure",
                },
            )
            return DeliveryResult(
                artifact_id=artifact.artifact_id,
                action="retry_scheduled",
                reason_class="simulated_delivery_failure",
            )

        try:
            self._post_to_dataforge(artifact)
        except Exception as exc:
            print(f"DATAFORGE DELIVERY ERROR for {artifact.artifact_id}: {exc}")
            next_attempt_at = datetime.now(UTC) + timedelta(minutes=15)
            worker_cursor.execute(
                self.RELEASE_FOR_RETRY_SQL,
                {
                    "artifact_id": artifact.artifact_id,
                    "next_attempt_at": next_attempt_at,
                    "reason_class": "dataforge_delivery_failed",
                },
            )
            return DeliveryResult(
                artifact_id=artifact.artifact_id,
                action="retry_scheduled",
                reason_class="dataforge_delivery_failed",
            )

        worker_cursor.execute(
            self.MARK_DELIVERED_SQL,
            {
                "artifact_id": artifact.artifact_id,
                "acknowledged_at": datetime.now(UTC),
            },
        )
        return DeliveryResult(
            artifact_id=artifact.artifact_id,
            action="delivered",
        )

    def _normalize_supporting_examples(self, payload_json: dict[str, Any]) -> list[str]:
        raw_examples_obj = payload_json.get("supporting_examples", [])
        raw_examples = cast(list[Any], raw_examples_obj if isinstance(raw_examples_obj, list) else [])

        normalized: list[str] = []
        for item in raw_examples:
            if isinstance(item, str):
                value = item.strip()
                if value:
                    normalized.append(value)
                continue

            if isinstance(item, dict):
                item_dict = cast(dict[str, Any], item)
                summary = str(item_dict.get("summary", "")).strip()
                reason_class = str(item_dict.get("reason_class", "")).strip()

                if summary and reason_class:
                    normalized.append(f"{reason_class}: {summary}")
                elif summary:
                    normalized.append(summary)
                elif reason_class:
                    normalized.append(reason_class)

        return normalized

    def _build_dataforge_payload(self, artifact: ClaimedArtifact) -> dict[str, Any]:
        payload_json = artifact.payload_json

        pattern_id_value = payload_json.get("pattern_id")
        pattern_id = str(pattern_id_value).strip() if pattern_id_value is not None else ""
        if not pattern_id:
            pattern_id = f"pattern-{artifact.artifact_id}"

        return {
            "pattern_id": pattern_id,
            "failure_pattern_type": str(payload_json.get("failure_pattern_type", "")),
            "frequency_window": str(payload_json.get("frequency_window", "")),
            "occurrence_count": int(payload_json.get("occurrence_count", 0)),
            "severity": str(payload_json.get("severity", "")),
            "affected_contract_or_capability": str(
                payload_json.get("affected_contract_or_capability", "")
            ),
            "supporting_examples": self._normalize_supporting_examples(payload_json),
        }

    def _post_to_dataforge(self, artifact: ClaimedArtifact) -> None:
        observed_at = artifact.first_observed_at
        if observed_at.tzinfo is None:
            observed_at = observed_at.replace(tzinfo=UTC)

        envelope: dict[str, Any] = {
            "envelope_type": artifact.envelope_type,
            "envelope_version": artifact.envelope_version,
            "fleet_member_id": artifact.fleet_member_id,
            "runtime_bundle_id": "runtime-promotion",
            "runtime_bundle_version": "v1",
            "service": artifact.service,
            "dedupe_key": artifact.dedupe_key,
            "observed_at": observed_at.isoformat().replace("+00:00", "Z"),
            "payload": self._build_dataforge_payload(artifact),
        }

        body = json.dumps(envelope).encode("utf-8")
        http_request = request.Request(
            DATAFORGE_RECEIPT_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(http_request, timeout=10) as response:
                status_code = response.getcode()
                response_body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"DataForge HTTP {exc.code}: {details}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"DataForge unreachable: {exc.reason}") from exc

        if status_code not in (200, 201):
            raise RuntimeError(f"Unexpected DataForge status: {status_code} body={response_body}")