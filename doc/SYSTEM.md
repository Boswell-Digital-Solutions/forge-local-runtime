# Forge Local Runtime — Complete System Reference

> Baseline documentation-protocol adoption for Forge Local Runtime.
> "Current repo truth before deeper authored expansion."

**Document version:** 0.1 (2026-04-03) — Baseline protocol adoption

---

## Table of Contents

1. [Overview & Philosophy](#1-overview--philosophy)
2. [Architecture](#2-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Configuration & Environment](#5-configuration--environment)
6. [Design System](#6-design-system)
7. [Frontend](#7-frontend)
8. [API Layer](#8-api-layer)
9. [Backend](#9-backend)
10. [Ecosystem Integration](#10-ecosystem-integration)
11. [Database Schema](#11-database-schema)
12. [AI Integration](#12-ai-integration)
13. [Error Handling Contract](#13-error-handling-contract)
14. [Testing Infrastructure](#14-testing-infrastructure)
15. [Handover / Migration Notes](#15-handover--migration-notes)

---

## 1. Overview & Philosophy

Forge Local Runtime is currently documented through a baseline protocol-adoption pass.
This section records only repository surfaces directly observable from the working tree.

### 1.1 Current Posture

| Topic | Current truth |
| --- | --- |
| Repo | `forge-local-runtime` |
| Protocol status | Baseline adoption in progress |
| Canonical technical reference | `doc/system/` plus generated root `SYSTEM.md` |
| Current scope | Expand this section as product and service boundaries are cataloged |

---

## 2. Architecture

This baseline architecture section records the major repo surfaces present today.

### 2.1 Observed Top-Level Areas

```text
forge-local-runtime/
├── .mypy_cache/
├── .vscode/
├── DECISIONS/
├── db/
├── doc/
├── docs/
├── runtime_promotion/
├── schemas/
├── scripts/
├── tests/
```

---

## 3. Tech Stack

This baseline stack inventory is inferred from repository markers and directory layout.

### 3.1 Detected Surfaces

| Layer | Marker | Current interpretation |
| --- | --- | --- |
| Persistence / Schemas | `alembic/`, `migrations/`, `db/`, `sql/`, `models/`, or `schemas/` present | Database, migration, or schema layer detected |

---

## 4. Project Structure

### 4.1 Directory Layout

```text
forge-local-runtime/
├── .mypy_cache/
├── .vscode/
├── DECISIONS/
├── db/
├── doc/
├── docs/
├── runtime_promotion/
├── schemas/
├── scripts/
├── tests/
```

### 4.2 Documentation Rule

- `doc/system/` is the canonical modular source for the root `SYSTEM.md`
- `scripts/context-bundle.sh` is the selective context assembly surface
- `CLAUDE.md` is the repo-local AI instruction file

---

## 5. Configuration & Environment

This baseline section has not yet enumerated every environment variable or configuration file.

### 5.1 Current Status

| Surface | Status |
| --- | --- |
| Environment variable inventory | Not yet expanded in this baseline |
| Config ownership mapping | Not yet expanded in this baseline |
| Protocol requirement | Every env var must be documented here as this repo matures |

---

## 6. Design System

This section is a placeholder unless a UI surface is present in the current repo.

### 6.1 Current Status

| Surface | Status |
| --- | --- |
| Design tokens | Expand when UI tokens are inventoried |
| Component patterns | Expand when UI components are cataloged |
| Brand posture | Keep this section grounded in implemented UI reality only |

---

## 7. Frontend

No obvious frontend surface was detected from the current top-level directory layout.

### 7.1 Current Status

| Surface | Status |
| --- | --- |
| UI routing and component inventory | Expand from current source files as the repo is cataloged |
| Desktop shell / browser surface | Record here only if implemented in the repo |

---

## 8. API Layer

No obvious dedicated API directory was detected from the current top-level directory layout.

### 8.1 Current Status

| Surface | Status |
| --- | --- |
| Endpoint inventory | Expand with real routes and shapes if this repo exposes APIs |
| Middleware and auth | Expand when the transport contract is cataloged |

---

## 9. Backend

This baseline section records the backend or core runtime surfaces detectable from the repo layout.

### 9.1 Observed Runtime Areas

| Surface | Current interpretation |
| --- | --- |
| Core runtime | Expand from `app/`, `service/`, `cortex_runtime/`, `crates/`, or `src-tauri/` as applicable |
| Delivery posture | Keep this section aligned with implemented code, not roadmap intent |

---

## 10. Ecosystem Integration

This baseline section should be expanded with concrete downstream and upstream dependencies as they are documented.

### 10.1 Current Status

| Surface | Status |
| --- | --- |
| Shared service integrations | Expand as concrete integrations are cataloged |
| Cross-repo boundaries | Keep explicit as this repo's authority boundary is clarified |

---

## 11. Database Schema

Database, schema, or migration surfaces are present in the repository tree.

### 11.1 Current Status

| Surface | Status |
| --- | --- |
| Table inventory | Expand with real table, column, and constraint definitions |
| Migration contract | Expand if this repo owns migrations or persistent schemas |

---

## 12. AI Integration

No obvious AI-specific directory was detected from the current top-level layout.

### 12.1 Current Status

| Surface | Status |
| --- | --- |
| Prompt or model routing docs | Expand as concrete AI surfaces are cataloged |
| Transparency and fallback posture | Record here when the current runtime contract is documented |

---

## 13. Error Handling Contract

Current error-handling documentation is a baseline only.

### 13.1 Baseline Law

- fail closed on missing documentation truth, malformed inputs, and unsupported runtime states
- document real error envelopes here as soon as they are cataloged from code or tests

---

## 14. Testing Infrastructure

This baseline section records only that testing surfaces exist in the repository tree.

### 14.1 Current Status

| Surface | Status |
| --- | --- |
| `tests/` directory | Present |
| QA expansion | Expand with concrete commands, suites, and pre-flight checks as they are cataloged |

---

## 15. Handover / Migration Notes

This repository entered a baseline documentation-protocol migration on 2026-04-03.

### 15.1 Current Migration Note

- modular `doc/system/` was established or normalized to support root `SYSTEM.md`
- further authored expansion is still required for exact APIs, schemas, and runtime contracts
