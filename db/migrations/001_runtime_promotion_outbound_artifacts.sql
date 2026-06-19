CREATE SCHEMA IF NOT EXISTS runtime_promotion;

CREATE TABLE IF NOT EXISTS runtime_promotion.outbound_artifacts (
    artifact_id TEXT PRIMARY KEY,
    envelope_type TEXT NOT NULL,
    envelope_version TEXT NOT NULL,
    service TEXT NOT NULL,
    fleet_member_id TEXT NOT NULL,
    dedupe_key TEXT NOT NULL,
    payload_json JSONB NOT NULL,

    status TEXT NOT NULL,
    delivery_attempt_count INTEGER NOT NULL DEFAULT 0,

    first_observed_at TIMESTAMPTZ NOT NULL,
    last_attempted_at TIMESTAMPTZ NULL,
    next_attempt_at TIMESTAMPTZ NULL,
    expires_at TIMESTAMPTZ NULL,
    acknowledged_at TIMESTAMPTZ NULL,

    rejection_reason_class TEXT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT outbound_artifacts_status_check
        CHECK (
            status IN (
                'queued',
                'retry_scheduled',
                'delivery_in_progress',
                'suppressed',
                'rejected',
                'expired',
                'delivered',
                'delivery_failed'
            )
        ),

    CONSTRAINT outbound_artifacts_envelope_type_nonempty
        CHECK (length(trim(envelope_type)) > 0),

    CONSTRAINT outbound_artifacts_envelope_version_nonempty
        CHECK (length(trim(envelope_version)) > 0),

    CONSTRAINT outbound_artifacts_service_nonempty
        CHECK (length(trim(service)) > 0),

    CONSTRAINT outbound_artifacts_fleet_member_id_nonempty
        CHECK (length(trim(fleet_member_id)) > 0),

    CONSTRAINT outbound_artifacts_dedupe_key_nonempty
        CHECK (length(trim(dedupe_key)) > 0),

    CONSTRAINT outbound_artifacts_delivery_attempt_count_nonnegative
        CHECK (delivery_attempt_count >= 0)
);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_status
    ON runtime_promotion.outbound_artifacts (status);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_next_attempt_at
    ON runtime_promotion.outbound_artifacts (next_attempt_at);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_service_status
    ON runtime_promotion.outbound_artifacts (service, status);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_fleet_member_id
    ON runtime_promotion.outbound_artifacts (fleet_member_id);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_dedupe_key
    ON runtime_promotion.outbound_artifacts (dedupe_key);

CREATE INDEX IF NOT EXISTS idx_outbound_artifacts_created_at
    ON runtime_promotion.outbound_artifacts (created_at);

CREATE UNIQUE INDEX IF NOT EXISTS uq_outbound_artifacts_active_dedupe
    ON runtime_promotion.outbound_artifacts (dedupe_key, envelope_type, envelope_version)
    WHERE status IN ('queued', 'retry_scheduled');

CREATE OR REPLACE FUNCTION runtime_promotion.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_outbound_artifacts_set_updated_at
    ON runtime_promotion.outbound_artifacts;

CREATE TRIGGER trg_outbound_artifacts_set_updated_at
BEFORE UPDATE ON runtime_promotion.outbound_artifacts
FOR EACH ROW
EXECUTE FUNCTION runtime_promotion.set_updated_at();