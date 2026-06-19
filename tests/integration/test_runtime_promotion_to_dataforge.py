from __future__ import annotations

import json
import os
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import psycopg
import pytest
from psycopg import Cursor
from psycopg.connection import Connection


@pytest.mark.integration
@pytest.mark.runtime_promotion
class TestRuntimePromotionToDataForge:
    def test_runtime_promotion_delivery_end_to_end(self) -> None:
        cfg = IntegrationConfig.from_env()

        ensure_dataforge_health(cfg.dataforge_base_url)

        artifact = seed_test_artifact(cfg)

        worker_result = run_runtime_promotion_worker(cfg)
        assert worker_result.returncode == 0, (
            "Runtime promotion worker failed.\n\n"
            f"STDOUT:\n{worker_result.stdout}\n\n"
            f"STDERR:\n{worker_result.stderr}"
        )

        local_row = fetch_local_artifact_row(cfg, artifact.artifact_id)
        assert local_row is not None, f"Artifact not found locally: {artifact.artifact_id}"

        assert local_row["status"] == "delivered", (
            "Expected local artifact to be delivered after worker run, "
            f"but got status={local_row['status']!r}"
        )
        assert int(local_row["delivery_attempt_count"]) >= 1
        assert local_row["acknowledged_at"] is not None

        receipt_row = fetch_dataforge_receipt_by_dedupe_key(
            cfg=cfg,
            dedupe_key=artifact.dedupe_key,
        )
        assert receipt_row is not None, (
            "Expected matching DataForge receipt row to exist for "
            f"dedupe_key={artifact.dedupe_key!r}"
        )

        assert receipt_row["dedupe_key"] == artifact.dedupe_key
        assert receipt_row["envelope_type"] == "local_failure_pattern"
        assert receipt_row["ingest_status"] == "accepted"
        assert receipt_row["source"] == "forge_local_runtime"


@dataclass(frozen=True)
class IntegrationConfig:
    runtime_db_url: str
    dataforge_base_url: str
    dataforge_db_url: str | None
    repo_root: str

    @classmethod
    def from_env(cls) -> "IntegrationConfig":
        runtime_db_url = (
            os.getenv("FORGE_LOCAL_RUNTIME_DATABASE_URL")
            or os.getenv("RUNTIME_PROMOTION_DATABASE_URL")
            or os.getenv("DATABASE_URL")
            or ""
        ).strip()

        if not runtime_db_url:
            raise RuntimeError(
                "Missing runtime DB URL. Set FORGE_LOCAL_RUNTIME_DATABASE_URL, "
                "RUNTIME_PROMOTION_DATABASE_URL, or DATABASE_URL before running "
                "this integration test."
            )

        dataforge_base_url = os.getenv("DATAFORGE_BASE_URL", "http://127.0.0.1:8001").strip()
        dataforge_db_url = os.getenv("DATAFORGE_DATABASE_URL")
        repo_root = os.getcwd()

        return cls(
            runtime_db_url=runtime_db_url,
            dataforge_base_url=dataforge_base_url,
            dataforge_db_url=dataforge_db_url.strip() if dataforge_db_url else None,
            repo_root=repo_root,
        )


@dataclass(frozen=True)
class SeededArtifact:
    artifact_id: str
    dedupe_key: str
    created_at: datetime


def ensure_dataforge_health(dataforge_base_url: str) -> None:
    health_url = f"{dataforge_base_url.rstrip('/')}/health"

    try:
        with urlopen(health_url, timeout=10) as response:
            status_code = getattr(response, "status", None) or response.getcode()
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AssertionError(
            f"DataForge health check failed at {health_url}. "
            f"status={exc.code} body={body}"
        ) from exc
    except URLError as exc:
        raise AssertionError(
            f"DataForge health check could not reach {health_url}: {exc}"
        ) from exc

    assert status_code == 200, (
        f"DataForge health check failed at {health_url}. "
        f"status={status_code} body={body}"
    )


def run_runtime_promotion_worker(cfg: IntegrationConfig) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    return subprocess.run(
        ["python", "scripts/run_runtime_promotion_worker.py"],
        cwd=cfg.repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def seed_test_artifact(cfg: IntegrationConfig) -> SeededArtifact:
    artifact_id = f"artifact-{uuid.uuid4()}"
    dedupe_key = f"it-dedupe-{uuid.uuid4()}"
    created_at = datetime.now().astimezone()

    envelope_payload: dict[str, Any] = {
        "service": "df_local_foundation",
        "severity": "high",
        "dedupe_key": dedupe_key,
        "observed_at": created_at.isoformat(),
        "envelope_type": "local_failure_pattern",
        "fleet_member_id": "fleet-dev-001",
        "retention_class": "C",
        "envelope_version": "v1",
        "frequency_window": "15m",
        "occurrence_count": 4,
        "producer_version": "1.0.0",
        "runtime_bundle_id": "forge-local-runtime",
        "runtime_bundle_version": "1.0.0",
        "pattern_id": f"pattern-{uuid.uuid4()}",
        "failure_pattern_type": "migration_failure",
        "affected_contract_or_capability": "runtime_promotion_queue",
        "supporting_examples": [
            {
                "summary": "Migration failed during startup",
                "example_id": "ex-it-001",
                "observed_at": created_at.isoformat(),
                "reason_class": "migration_failed",
            }
        ],
    }

    with psycopg.connect(cfg.runtime_db_url) as conn:
        typed_conn = cast(Connection[Any], conn)
        with typed_conn.cursor() as cur:
            cur.execute(
                """
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
                    expires_at,
                    created_at,
                    updated_at
                )
                VALUES (
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
                    %(expires_at)s,
                    %(created_at)s,
                    %(updated_at)s
                )
                """,
                {
                    "artifact_id": artifact_id,
                    "envelope_type": "local_failure_pattern",
                    "envelope_version": "v1",
                    "service": "df_local_foundation",
                    "fleet_member_id": "fleet-dev-001",
                    "dedupe_key": dedupe_key,
                    "payload_json": json.dumps(
                        envelope_payload,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    "status": "queued",
                    "delivery_attempt_count": 0,
                    "first_observed_at": created_at,
                    "expires_at": None,
                    "created_at": created_at,
                    "updated_at": created_at,
                },
            )
        typed_conn.commit()

    return SeededArtifact(
        artifact_id=artifact_id,
        dedupe_key=dedupe_key,
        created_at=created_at,
    )

    with psycopg.connect(cfg.runtime_db_url) as conn:
        typed_conn = cast(Connection[Any], conn)
        with typed_conn.cursor() as cur:
            cur.execute(
                """
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
                    expires_at,
                    created_at,
                    updated_at
                )
                VALUES (
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
                    %(expires_at)s,
                    %(created_at)s,
                    %(updated_at)s
                )
                """,
                {
                    "artifact_id": artifact_id,
                    "envelope_type": "local_failure_pattern",
                    "envelope_version": "v1",
                    "service": "df_local_foundation",
                    "fleet_member_id": "integration-test-node",
                    "dedupe_key": dedupe_key,
                    "payload_json": json.dumps(
                        envelope_payload,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    "status": "queued",
                    "delivery_attempt_count": 0,
                    "first_observed_at": created_at,
                    "expires_at": None,
                    "created_at": created_at,
                    "updated_at": created_at,
                },
            )
        typed_conn.commit()

    return SeededArtifact(
        artifact_id=artifact_id,
        dedupe_key=dedupe_key,
        created_at=created_at,
    )


def fetch_local_artifact_row(
    cfg: IntegrationConfig,
    artifact_id: str,
) -> dict[str, Any] | None:
    with psycopg.connect(cfg.runtime_db_url) as conn:
        typed_conn = cast(Connection[Any], conn)
        with typed_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    artifact_id,
                    status,
                    delivery_attempt_count,
                    acknowledged_at,
                    rejection_reason_class
                FROM runtime_promotion.outbound_artifacts
                WHERE artifact_id = %(artifact_id)s
                """
                ,
                {"artifact_id": artifact_id},
            )
            row = cur.fetchone()
            return row_to_dict(cur, row)


def fetch_dataforge_receipt_by_dedupe_key(
    cfg: IntegrationConfig,
    dedupe_key: str,
) -> dict[str, Any] | None:
    if not cfg.dataforge_db_url:
        raise RuntimeError(
            "Missing DATAFORGE_DATABASE_URL. "
            "Set it so this test can verify the receipt directly in DataForge Postgres."
        )

    with psycopg.connect(cfg.dataforge_db_url) as conn:
        typed_conn = cast(Connection[Any], conn)
        with typed_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    receipt_id,
                    dedupe_key,
                    envelope_type,
                    service,
                    ingest_status,
                    source
                FROM runtime_promotion_receipts
                WHERE dedupe_key = %(dedupe_key)s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                {"dedupe_key": dedupe_key},
            )
            row = cur.fetchone()
            return row_to_dict(cur, row)


def row_to_dict(
    cur: Cursor[Any],
    row: Any,
) -> dict[str, Any] | None:
    if row is None:
        return None

    description = cur.description
    if description is None:
        raise RuntimeError("Cursor description is missing after query execution.")

    column_names = [col.name for col in description]
    values = list(row)
    return dict(zip(column_names, values, strict=True))