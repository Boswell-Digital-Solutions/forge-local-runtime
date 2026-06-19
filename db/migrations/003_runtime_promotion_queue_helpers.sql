CREATE OR REPLACE FUNCTION runtime_promotion.claim_ready_artifacts(
    p_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    artifact_id TEXT,
    envelope_type TEXT,
    envelope_version TEXT,
    service TEXT,
    fleet_member_id TEXT,
    dedupe_key TEXT,
    payload_json JSONB,
    status TEXT,
    delivery_attempt_count INTEGER,
    first_observed_at TIMESTAMPTZ,
    last_attempted_at TIMESTAMPTZ,
    next_attempt_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    acknowledged_at TIMESTAMPTZ,
    rejection_reason_class TEXT,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH candidates AS (
        SELECT oa.artifact_id
        FROM runtime_promotion.outbound_artifacts oa
        WHERE oa.status IN ('queued', 'retry_scheduled')
          AND (oa.next_attempt_at IS NULL OR oa.next_attempt_at <= NOW())
          AND (oa.expires_at IS NULL OR oa.expires_at > NOW())
        ORDER BY
            COALESCE(oa.next_attempt_at, oa.created_at) ASC,
            oa.created_at ASC
        FOR UPDATE SKIP LOCKED
        LIMIT p_limit
    ),
    claimed AS (
        UPDATE runtime_promotion.outbound_artifacts oa
        SET
            status = 'delivery_in_progress',
            delivery_attempt_count = oa.delivery_attempt_count + 1,
            last_attempted_at = NOW(),
            next_attempt_at = NULL
        WHERE oa.artifact_id IN (SELECT c.artifact_id FROM candidates c)
        RETURNING
            oa.artifact_id,
            oa.envelope_type,
            oa.envelope_version,
            oa.service,
            oa.fleet_member_id,
            oa.dedupe_key,
            oa.payload_json,
            oa.status,
            oa.delivery_attempt_count,
            oa.first_observed_at,
            oa.last_attempted_at,
            oa.next_attempt_at,
            oa.expires_at,
            oa.acknowledged_at,
            oa.rejection_reason_class,
            oa.created_at,
            oa.updated_at
    )
    SELECT
        c.artifact_id,
        c.envelope_type,
        c.envelope_version,
        c.service,
        c.fleet_member_id,
        c.dedupe_key,
        c.payload_json,
        c.status,
        c.delivery_attempt_count,
        c.first_observed_at,
        c.last_attempted_at,
        c.next_attempt_at,
        c.expires_at,
        c.acknowledged_at,
        c.rejection_reason_class,
        c.created_at,
        c.updated_at
    FROM claimed c
    ORDER BY
        COALESCE(c.last_attempted_at, c.created_at) ASC,
        c.created_at ASC;
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.release_claim_for_retry(
    p_artifact_id TEXT,
    p_next_attempt_at TIMESTAMPTZ,
    p_reason_class TEXT DEFAULT NULL
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'retry_scheduled',
        next_attempt_at = p_next_attempt_at,
        rejection_reason_class = p_reason_class
    WHERE artifact_id = p_artifact_id
      AND status = 'delivery_in_progress';
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.mark_delivered(
    p_artifact_id TEXT,
    p_acknowledged_at TIMESTAMPTZ DEFAULT NOW()
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'delivered',
        acknowledged_at = p_acknowledged_at,
        next_attempt_at = NULL,
        rejection_reason_class = NULL
    WHERE artifact_id = p_artifact_id
      AND status = 'delivery_in_progress';
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.mark_delivery_failed(
    p_artifact_id TEXT,
    p_reason_class TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'delivery_failed',
        rejection_reason_class = p_reason_class,
        next_attempt_at = NULL
    WHERE artifact_id = p_artifact_id
      AND status = 'delivery_in_progress';
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.mark_rejected(
    p_artifact_id TEXT,
    p_reason_class TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'rejected',
        rejection_reason_class = p_reason_class,
        next_attempt_at = NULL
    WHERE artifact_id = p_artifact_id
      AND status IN ('queued', 'retry_scheduled', 'delivery_in_progress');
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.mark_suppressed(
    p_artifact_id TEXT,
    p_reason_class TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'suppressed',
        rejection_reason_class = p_reason_class,
        next_attempt_at = NULL
    WHERE artifact_id = p_artifact_id
      AND status IN ('queued', 'retry_scheduled', 'delivery_in_progress');
END;
$$;

CREATE OR REPLACE FUNCTION runtime_promotion.expire_artifact(
    p_artifact_id TEXT,
    p_reason_class TEXT DEFAULT 'promotion_artifact_expired'
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE runtime_promotion.outbound_artifacts
    SET
        status = 'expired',
        rejection_reason_class = p_reason_class,
        next_attempt_at = NULL
    WHERE artifact_id = p_artifact_id
      AND status IN ('queued', 'retry_scheduled', 'delivery_in_progress');
END;
$$;