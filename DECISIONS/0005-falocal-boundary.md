# ADR 0005 — FA Local Boundary

## Status
Accepted

## Context

FA Local is the governed local execution boundary in the runtime layer.

Its purpose is not open-ended autonomy.
Its purpose is trusted, policy-gated, capability-admitted execution under explicit constraints.

The major risk is drift into hidden orchestration, semantic authority, durable memory ownership, or broad local-agent behavior.

## Decision

FA Local is constrained to requester-trust-gated, policy-before-execution local execution.

FA Local may validate requests, resolve requester trust, evaluate policy artifacts, admit capabilities, validate bounded execution plans, coordinate approved execution routes, and emit truthful execution-state reporting.

FA Local must not become app semantic authority, durable semantic memory, hidden planner, or open-ended autonomous agent substrate.

## Consequences

- Execution remains subordinate to trust and policy.
- Capability access remains explicit and governable.
- Side effects remain bounded and reviewable.
- FA Local is prevented from silently centralizing authority.