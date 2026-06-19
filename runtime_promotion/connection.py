from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import psycopg

from runtime_promotion.persistence import DbConnection, DbCursor


@dataclass(frozen=True, slots=True)
class RuntimePromotionDbConfig:
    database_url: str

    @classmethod
    def from_env(cls) -> "RuntimePromotionDbConfig":
        database_url = os.environ.get("FORGE_LOCAL_RUNTIME_DATABASE_URL", "").strip()
        if not database_url:
            raise ValueError(
                "FORGE_LOCAL_RUNTIME_DATABASE_URL is required for runtime promotion persistence."
            )
        return cls(database_url=database_url)


class PsycopgCursorAdapter(DbCursor):
    def __init__(self, cursor: psycopg.Cursor[Any]) -> None:
        self._cursor = cursor

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        self._cursor.execute(sql, params)

    def fetchall(self) -> list[tuple[Any, ...]]:
        return list(self._cursor.fetchall())


class PsycopgConnectionAdapter(DbConnection):
    def __init__(self, connection: psycopg.Connection[Any]) -> None:
        self._connection = connection

    def cursor(self) -> DbCursor:
        return PsycopgCursorAdapter(self._connection.cursor())

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()


def create_connection() -> DbConnection:
    config = RuntimePromotionDbConfig.from_env()
    raw_connection = psycopg.connect(config.database_url)
    return PsycopgConnectionAdapter(raw_connection)