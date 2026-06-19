# Syntax vs Semantics Firewall — Forge Local Runtime

## Purpose

This document formalizes the syntax-versus-semantics boundary required by the runtime, especially for Cortex and services that consume Cortex artifacts.

## Rule

Syntax and semantics are distinct control domains.

A service that owns syntax-level extraction, structure detection, provenance, packaging, or retrieval preparation must not silently assume semantic interpretation authority.

## Primary implication for Cortex

Cortex may:

- detect structure
- identify sections and headings
- segment content
- extract metadata fields
- preserve extraction provenance
- emit handoff packages
- signal completeness, integrity, and freshness posture

Cortex may not:

- assign meaning
- decide truth
- decide business conclusions
- become retrieval authority
- become workflow authority
- become semantic policy surface

## Downstream implication

A downstream service may consume syntax-level artifacts without retroactively converting Cortex into a semantic authority.

Semantic interpretation, candidate production, or action planning must remain owned where constitutionally assigned.

## Anti-drift implications

The following are disallowed without explicit re-architecture:

- embedding summarization as owned Cortex behavior
- broadening extraction labels into semantic judgment
- using reverse signaling to coordinate downstream workflows
- turning retrieval preparation into ranking or acceptance authority

## Schema and handoff alignment

This firewall should be reflected in:

- `schemas/handoff-envelope.schema.json`
- `schemas/runtime-contract.schema.json`
- `docs/services/cortex-role.md`
- `docs/architecture/boundary-matrix.md`