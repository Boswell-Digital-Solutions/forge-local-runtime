# Known Issues

This file records confirmed defects and open problems. Each entry states its status, its cause and what is not done.

## The Repo Context Gate fails because CLAUDE.md differs from the generator output

- **Status**: Open. Recorded 2026-10-02. The gate has failed on every push run to `master` that had a result: 2026-07-01, 2026-09-09, 2026-09-25 and 2026-09-30.
- **What is wrong**: the step "Confirm generated files are committed" in the `Repo Context Gate` workflow regenerates the four agent instruction files (`AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`) and fails if `git diff --exit-code` shows a difference. Running `python3 scripts/generate_agent_instructions.py` on a clean `master` changes `CLAUDE.md`: 125 lines are added and 29 are removed. The other three files do not change.
- **Cause**: the committed `CLAUDE.md` was not regenerated after the manifest or the generator changed.
- **Impact**: low. The gate fails on every run, so it proves nothing. A failing gate that nobody reads also hides a real drift later. The new Documentation CI is separate and passes.
- **Fix, not done**: run the generator, read the new `CLAUDE.md`, and commit it. Check that the generated text carries no local path of a developer machine. The operator decides whether the new text is correct.
- **Related**: the repository has a `Makefile` target and a script `ci_gate.sh` that no workflow runs. The repository has no code CI.
