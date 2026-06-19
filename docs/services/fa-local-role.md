# FA Local — Service Role

## Role

FA Local is the bounded, requester-trust-gated, policy-before-execution local execution boundary for the Forge local runtime layer.

It exists to govern local side-effect-capable execution under explicit trust, policy, capability, and bounded-plan constraints without becoming an autonomous or semantic authority surface.

## Owns

FA Local owns:

- execution request intake
- requester identity and requester-class resolution
- requester trust posture evaluation
- policy artifact enforcement before side effects
- capability admission checks
- bounded execution-plan validation
- approval posture ladder enforcement
- plan fingerprinting / plan-hash posture
- controlled execution coordination for approved local routes
- truthful execution-state, denial, degraded, and partial-success reporting
- review-package handoff support where execution cannot proceed directly
- bounded forensic event generation under minimization rules

## Explicitly does not own

FA Local does not own:

- application business semantics
- durable semantic memory
- file-intelligence semantics
- model/inference authority
- hidden workflow policy authority
- open-ended autonomous planning
- broad agentic self-direction
- ungoverned tool access
- silent side-effect execution
- canonical truth promotion

## Why the boundary exists

Execution is the highest-risk local runtime surface because it can cause side effects.

Without constitutional narrowing, an execution controller tends to drift into:

- hidden orchestrator
- de facto agent runtime
- semantic authority
- memory owner
- silent planner
- unreviewable tool governor

FA Local exists to permit governed execution while fail-closing against those drift paths.

## Policy-before-execution rule

No side-effect-capable execution should proceed without policy posture.

Where policy is required, missing policy must deny or route to review rather than silently continue.

## Requester trust model

Execution requests must be resolved against requester posture, not treated as uniformly trusted.

Requester evaluation should support at least bounded distinctions such as:

- trusted operator
- trusted application surface
- constrained internal caller
- untrusted or unknown requester

Unknown requester posture should fail closed by default.

## Capability admission posture

Execution ability must remain capability-scoped.

A valid request is not sufficient by itself.
The requested capability must also be admitted for the requester, route, and policy posture in force.

## Approval posture ladder

FA Local should support a clear approval posture ladder such as:

- deny
- review_required
- explicit_operator_approval
- policy_preapproved
- execute_allowed

Exact labels may evolve, but the ladder concept must remain explicit and governable.

## Bounded execution-plan model

Execution plans must remain bounded, inspectable, and fingerprintable.

Where execution depends on a plan artifact, FA Local should preserve or reference:

- plan identity
- plan hash or fingerprint
- capability scope
- requester posture
- approval posture
- route or tool identity
- resulting state

This prevents silent plan drift between review and execution.

## Review-package handoff posture

When direct execution is not allowed, FA Local may emit a bounded review package or review-required result.

That handoff does not convert FA Local into a hidden planning authority.
It exists to preserve reviewability and fail-closed posture.

## Forensic minimization posture

Forensic event generation must be bounded and minimized.

Preferred forensic content includes:

- event class
- correlation ids
- requester class
- capability id
- plan hash
- retention class
- severity
- redaction posture

Raw content or raw tool payload capture must be excluded by default unless explicitly justified and governed.

## Privacy sensitivity

FA Local may see high-sensitivity execution context.

Therefore:

- logs must remain content-sparing
- diagnostics must be scoped
- retention must be bounded
- review artifacts must minimize sensitive payloads where possible

## Readiness, denial, and degraded behavior

FA Local must report truthful execution states such as:

- denied
- review_required
- waiting_explicit_approval
- admitted_not_started
- degraded_pre_start
- degraded_in_flight
- partial_success
- completed_with_constraints
- unavailable_dependency_block

It must not hide denial or degraded truth behind vague generic failure language.

## Anti-monolith split triggers

A split away from FA Local should be considered only when a concern develops truly distinct:

- trust model
- policy regime
- capability language
- forensic/observability constraints
- execution failure posture
- anti-drift value

No split should occur just to create faux agent hierarchy or naming symmetry.

## Interaction posture with other services

### With DF Local Foundation
FA Local may rely on bounded substrate support for state, records, and recovery-adjacent artifacts.
DF Local Foundation does not become execution authority.

### With NeuronForge Local
FA Local may invoke approved local inference routes where policy allows.
That does not transfer final authority to NeuronForge Local.

### With Cortex
FA Local may invoke Cortex-related preparation paths only within approved policy and capability posture.
That does not make FA Local the syntax authority or Cortex the execution governor.

## Governing rule

FA Local must remain a requester-trust-gated, policy-before-execution, capability-admitted execution boundary.
If a proposal implies autonomy drift, semantic authority drift, durable memory drift, or stealth orchestration accumulation, it should be rejected or split.