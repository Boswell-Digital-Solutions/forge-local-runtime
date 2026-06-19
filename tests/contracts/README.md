# Contract Validation

This folder contains fixture-driven validation for Forge Local Runtime shared schemas.

## Current coverage

- valid service-status fixture
- invalid service-status fixture missing degraded subtype
- valid minimized forensic fixture
- invalid forensic fixture with content included but no content reference

## Validation rule

Shared schema posture is part of the runtime control surface.
Fixtures should prove both:

- valid instances pass
- invalid instances fail