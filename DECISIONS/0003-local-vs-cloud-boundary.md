# ADR 0003 — Local vs Cloud Boundary

## Status
Accepted

## Context

Forge uses both local-first and cloud-augmented architecture patterns.

Without an explicit boundary, cloud services can silently become baseline dependencies, or local systems can be distorted into weak cloud imitations.

The local runtime needs a constitutional minimum role that remains meaningful without cloud access.

## Decision

The local runtime is a meaningful baseline substrate that must remain useful without cloud connectivity.

Cloud services are additive capability layers.
They may augment local depth, scale, breadth, or synchronization, but they must not redefine the constitutional minimum responsibilities of the local runtime.

## Consequences

- The local runtime must deliver real standalone value.
- Cloud augmentation is permitted, but dependency drift is not.
- Local services should not be designed as thin placeholders for future cloud replacement.
- Boundary docs and schemas must preserve this distinction.