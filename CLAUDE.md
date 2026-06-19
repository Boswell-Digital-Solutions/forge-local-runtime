# Forge Local Runtime — Claude Instructions

## Module Map

| Module | Surface | Current role |
| --- | --- | --- |
| Documentation Stack | `doc/system/`, `SYSTEM.md`, `scripts/context-bundle.sh` | Canonical repo context and build surfaces |
| Data and Schemas | `schemas/`, `models/`, `db/`, `sql/`, `alembic/`, or `migrations/` | Persistence and validation surfaces |
| Governance and Specs | `docs/`, `governance/`, `DECISIONS/`, `prompts/`, `evals/`, `analytics/`, or `registry/` | Repo doctrine, experiments, and supporting design material |
| Verification | `tests/`, `fixtures/`, `evidence/`, `audit/`, or `reports/` | Test and audit surfaces |

## Coding Standards

- Treat `doc/system/` part files as canonical; rebuild root `SYSTEM.md` with `bash doc/system/BUILD.sh`
- Keep documentation in present tense and aligned to implemented reality
- Prefer bounded patches over broad rewrites unless a file is clearly scaffold-only
- Do not bypass repo-local authority boundaries documented in `SYSTEM.md`

## File Conventions

- Canonical system docs live under `doc/system/`
- Root `SYSTEM.md` is a build artifact
- Supporting design material lives under `docs/`
- Repo automation scripts live under `scripts/`
- Tests live under `tests/` when present

## Context Loading

```bash
# Show available sections and presets
./scripts/context-bundle.sh --list

# Core bundle
./scripts/context-bundle.sh --preset core

# Documentation or testing-focused bundles
./scripts/context-bundle.sh --preset docs
./scripts/context-bundle.sh --preset testing
```

## Ecosystem Rules

- Keep cross-repo integrations explicit and documented
- Do not invent undocumented APIs, tables, routes, or environment variables
- If a runtime contract changes, update `doc/system/`, rebuild `SYSTEM.md`, and keep `CLAUDE.md` current

## Testing Expectations

- Run the repo's existing tests when available before claiming a change is complete
- Keep documentation build and context-bundle scripts working
- Expand test documentation in `SYSTEM.md` as exact suites and commands are cataloged

## Change Protocol

- Edit `doc/system/` part files, not the generated root `SYSTEM.md`
- Rebuild `SYSTEM.md` after documentation changes
- Keep new docs honest about current implementation state
