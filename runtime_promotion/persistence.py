from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from runtime_promotion.db import PromotionQueueDbWriter, QueueWriteResult
from runtime_promotion.queue import QueueWritePlan


@runtime_checkable
class DbCursor(Protocol):
    def execute(self, sql: str, params: dict[str, Any]) -> None: ...


@runtime_checkable
class DbConnection(Protocol):
    def cursor(self) -> DbCursor: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class ConnectionFactory(Protocol):
    def __call__(self) -> DbConnection: ...


@dataclass(frozen=True, slots=True)
class PersistResult:
    artifact_written: bool
    policy_event_written: bool
    artifact_id: str | None
    policy_event_id: str
    queue_status: str | None


class RuntimePromotionRepository:
    """
    First-pass persistence adapter for runtime promotion.

    Current responsibility:
    - accept a QueueWritePlan
    - translate it through PromotionQueueDbWriter
    - execute the actual SQL against a DB-API-like connection
    - commit on success
    - rollback on failure

    Important boundary:
    - this class does not decide policy
    - this class does not normalize signals
    - this class does not build queue plans
    - it only persists an already-decided plan
    """

    def __init__(
        self,
        connection_factory: ConnectionFactory,
        db_writer: PromotionQueueDbWriter | None = None,
    ) -> None:
        self._connection_factory = connection_factory
        self._db_writer = db_writer or PromotionQueueDbWriter()

    def persist_plan(self, plan: QueueWritePlan) -> PersistResult:
        connection = self._connection_factory()

        try:
            write_result = self._write_plan(connection, plan)
            connection.commit()
            return self._build_persist_result(plan, write_result)
        except Exception:
            connection.rollback()
            raise

    def _write_plan(
        self,
        connection: DbConnection,
        plan: QueueWritePlan,
    ) -> QueueWriteResult:
        cursor = connection.cursor()
        return self._db_writer.write_plan(cursor, plan)

    def _build_persist_result(
        self,
        plan: QueueWritePlan,
        write_result: QueueWriteResult,
    ) -> PersistResult:
        artifact_id = None
        queue_status = None

        if plan.queue_record is not None:
            artifact_id = plan.queue_record.artifact_id
            queue_status = plan.queue_record.status.value

        policy_event_id = str(write_result.policy_event_params["policy_event_id"])

        return PersistResult(
            artifact_written=write_result.artifact_written,
            policy_event_written=write_result.policy_event_written,
            artifact_id=artifact_id,
            policy_event_id=policy_event_id,
            queue_status=queue_status,
        )