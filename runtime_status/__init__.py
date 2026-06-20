"""Forge Local Runtime status aggregation.

Producer-side composition of the four local services' status into a single
bounded service matrix, plus a deterministic three-class pressure indicator
derived from that matrix. Pure, fail-closed, no I/O.
"""
from __future__ import annotations

from .aggregator import (
    CANONICAL_SERVICES,
    build_service_matrix,
    derive_pressure,
)

__all__ = [
    "CANONICAL_SERVICES",
    "build_service_matrix",
    "derive_pressure",
]
