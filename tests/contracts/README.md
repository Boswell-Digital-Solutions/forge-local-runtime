# Contract Validation

This folder contains fixture-driven validation for Forge Local Runtime shared schemas.

## Current coverage

- valid service-status fixture
- invalid service-status fixture missing degraded subtype
- valid minimized forensic fixture
- invalid forensic fixture with content included but no content reference
- valid runtime-service-matrix fixture (mixed states incl. fail-closed missing service)
- invalid runtime-service-matrix fixture missing a required service
- valid runtime-pressure fixture (elevated)
- invalid runtime-pressure fixture with an out-of-enum pressure class

Aggregator logic that produces these envelopes is tested in
`tests/test_runtime_status_aggregator.py` (matrix composition, fail-closed
placeholders, deterministic pressure rollup, and schema conformance of output).

## Validation rule

Shared schema posture is part of the runtime control surface.
Fixtures should prove both:

- valid instances pass
- invalid instances fail