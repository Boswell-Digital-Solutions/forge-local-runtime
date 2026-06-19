from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from runtime_promotion.connection import create_connection
from runtime_promotion.worker import PromotionDeliveryWorker


def main() -> None:
    connection = create_connection()
    worker = PromotionDeliveryWorker()

    try:
        claimed = worker.claim_ready_artifacts(connection, limit=10)

        results: list[dict[str, Any]] = []
        for artifact in claimed:
            result = worker.deliver_claimed_artifact(connection, artifact)
            results.append(
                {
                    "artifact_id": result.artifact_id,
                    "action": result.action,
                    "reason_class": result.reason_class,
                }
            )

        connection.commit()

        output = {
            "claimed_count": len(claimed),
            "claimed_artifacts": [
                {
                    "artifact_id": artifact.artifact_id,
                    "envelope_type": artifact.envelope_type,
                    "service": artifact.service,
                    "status": artifact.status,
                    "delivery_attempt_count": artifact.delivery_attempt_count,
                    "created_at": (
                        artifact.created_at.isoformat()
                        if isinstance(artifact.created_at, datetime)
                        else None
                    ),
                }
                for artifact in claimed
            ],
            "results": results,
        }

        print(json.dumps(output, indent=2, default=str))
    except Exception:
        connection.rollback()
        raise


if __name__ == "__main__":
    main()