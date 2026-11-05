# Known Issues

This file records confirmed defects and open problems. Each entry states its status, its cause and what is not done.

## The Repo Context Gate fails because CLAUDE.md differs from the generator output

- **Status**: Closed on 2026-10-30. Recorded 2026-10-02. The gate has failed on every push run to `master` that had a result: 2026-07-01, 2026-09-09, 2026-09-25 and 2026-09-30.
- **Closure evidence (2026-10-30)**: commit `59f043a` (#11, 2026-10-15) committed a `CLAUDE.md` that matches the generator output: it adds 141 lines to the file. The `Repo Context Gate` passed on the push run to `master` at `59f043a` (run 38693094309). The last failing push run was `2da39c9` (run 37053332350). `59f043a` is still the head of `master`. This closes the drift failure only. It says nothing about other gates, and the repository still has no code CI.
- **What is wrong**: the step "Confirm generated files are committed" in the `Repo Context Gate` workflow regenerates the four agent instruction files (`AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `GEMINI.md`) and fails if `git diff --exit-code` shows a difference. Running `python3 scripts/generate_agent_instructions.py` on a clean `master` changes `CLAUDE.md`: 125 lines are added and 29 are removed. The other three files do not change.
- **Cause**: the committed `CLAUDE.md` was not regenerated after the manifest or the generator changed.
- **Impact**: low. The gate fails on every run, so it proves nothing. A failing gate that nobody reads also hides a real drift later. The new Documentation CI is separate and passes.
- **Fix, as recorded on 2026-10-02 (now done by `59f043a`)**: run the generator, read the new `CLAUDE.md`, and commit it. Check that the generated text carries no local path of a developer machine. The operator decides whether the new text is correct.
- **Related**: the repository has a `Makefile` target and a script `ci_gate.sh` that no workflow runs. The repository has no code CI.

## The branch consolidation is not finished: origin still serves `master` as the default

- **Status**: Open. Recorded 2026-11-05. Two of the four steps are done in this change. The two that remain are GitHub repository settings, not code.
- **What is wrong**: the repository had two branches. `master` held 18 commits of work that `main` did not have. `main` held two commits that `master` did not have. Neither branch was a superset, so no single branch held the repository. `repo.manifest.yaml` declared `default_branch: master`, and the four generated agent instruction files repeated it, so an agent that read them operated on the branch that was about to be retired.
- **Done in this change**: a merge commit on `master` takes both of `main`'s commits, so `master` is now a superset of both branches and PR #13 (`master` into `main`) carries the whole repository. `repo.manifest.yaml` declares `default_branch: main`, the four generated files were regenerated from it, and the three workflows trigger on `[main, master]` so neither branch loses CI during the transition.
- **Not done, and only the operator can do it**: switch the GitHub default branch to `main` (Settings, Branches), then delete `master`. Deleting a branch is not reversible from here, and no tool in this session can change a repository setting.
- **Consequence until then**: the `default_branch` check in `scripts/verify_repo_context.py` fails, and the `Repo Context Gate` is red on every push run. The failure is correct and states the remedy: `origin default / CI base is master; expected main`. It is the outstanding settings change reported as a failing check, not a regression. It passes on PR #13 itself, because that check reads the pull request base ref, which is already `main`.
- **Related, fixed in this change**: `observed_default_branch` in `scripts/repo_context_tools.py` read `refs/remotes/origin/HEAD`, which `actions/checkout` never creates, so the gate aborted with a `CalledProcessError` traceback instead of reporting a result. It also returned `"master"` whenever `GITHUB_REF` was `refs/heads/master`, which is the branch that was pushed and not the repository default, so the check would have passed for any declared value. It now asks the remote with `git ls-remote --symref origin HEAD` and returns `""` on failure, which the check reports as `<undetermined>`.
