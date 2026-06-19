CREATE TABLE IF NOT EXISTS runtime_promotion.policy_events (
    policy_event_id TEXT PRIMARY KEY,
    artifact_id TEXT NULL,
    envelope_type TEXT NOT NULL,
    service TEXT NOT NULL,
    fleet_member_id TEXT NOT NULL,

    event_type TEXT NOT NULL,
    outcome TEXT NOT NULL,
    reason_class TEXT NOT NULL,
    summary TEXT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT policy_events_event_type_check
        CHECK (
            event_type IN (
                'normalization',
                'policy_gate',
                'queue_write',
                'transport',
                'delivery_ack',
                'expiry'
            )
        ),

    CONSTRAINT policy_events_outcome_check
        CHECK (
            outcome IN (
                'accepted',
                'queued',
                'retry_scheduled',
                'suppressed',
                'rejected',
                'expired',
                'delivered',
                'delivery_failed',
                'quarantined'
            )
        ),

    CONSTRAINT policy_events_envelope_type_nonempty
        CHECK (length(trim(envelope_type)) > 0),

    CONSTRAINT policy_events_service_nonempty
        CHECK (length(trim(service)) > 0),

    CONSTRAINT policy_events_fleet_member_id_nonempty
        CHECK (length(trim(fleet_member_id)) > 0),

    CONSTRAINT policy_events_reason_class_nonempty
        CHECK (length(trim(reason_class)) > 0)
);

CREATE INDEX IF NOT EXISTS idx_policy_events_artifact_id
    ON runtime_promotion.policy_events (artifact_id);

CREATE INDEX IF NOT EXISTS idx_policy_events_event_type
    ON runtime_promotion.policy_events (event_type);

CREATE INDEX IF NOT EXISTS idx_policy_events_outcome
    ON runtime_promotion.policy_events (outcome);

CREATE INDEX IF NOT EXISTS idx_policy_events_service_created_at
    ON runtime_promotion.policy_events (service, created_at);

CREATE INDEX IF NOT EXISTS idx_policy_events_fleet_member_created_at
    ON runtime_promotion.policy_events (fleet_member_id, created_at);

CREATE INDEX IF NOT EXISTS idx_policy_events_created_at
    ON runtime_promotion.policy_events (created_at);

ALTER TABLE runtime_promotion.policy_events
    ADD CONSTRAINT policy_events_artifact_id_fk
    FOREIGN KEY (artifact_id)
    REFERENCES runtime_promotion.outbound_artifacts (artifact_id)
    ON DELETE SET NULL;