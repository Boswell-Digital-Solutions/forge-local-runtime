# Forensic Retention — Forge Local Runtime

## Purpose

This document defines retention posture for minimized forensic event envelopes in Forge Local Runtime.

## Rule

Forensic retention must support accountability without turning the runtime into a content archive.

Retention is governed by class, not by operator convenience.

## Core retention classes

The runtime uses these retention classes:

- `ephemeral`
- `short`
- `standard`
- `extended_by_exception`

## Retention guidance

### ephemeral
Use for low-risk transient operational artifacts that do not need durable forensic value.

### short
Use for most minimized runtime events where short accountability windows are sufficient.

### standard
Use for events with meaningful governance, denial, integrity, or execution significance.

### extended_by_exception
Use only where a justified governance, incident, or operator exception path explicitly requires longer retention.

## Minimization rule

Forensic envelopes should prefer:

- event class
- service id
- correlation ids
- requester class
- capability id
- plan hash
- severity
- retention class
- redaction status

Raw content inclusion is excluded by default.

## Content rule

If content is ever included:

- it must be exceptional, not default
- it must use explicit reference posture
- it must be redacted
- retention should be narrowly justified

## Schema alignment

Retention posture aligns with:

- `schemas/forensic-event-envelope.schema.json`

## Governing question

Is the retained artifact the minimum necessary for accountability, and is its retention class justified?