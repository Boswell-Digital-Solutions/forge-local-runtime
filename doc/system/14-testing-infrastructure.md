## 14. Testing Infrastructure

This baseline section records only that testing surfaces exist in the repository tree.

### 14.1 Current Status

| Surface | Status |
| --- | --- |
| `tests/` directory | Present |
| QA expansion | Expand with concrete commands, suites, and pre-flight checks as they are cataloged |

### 14.2 Which CI runs for which change

This repository has no code CI.

The Repo Context Gate runs on every change. It is a documentation gate. It checks the generated agent instruction files, the drift check, and the repo identity.

The Documentation CI runs for documentation changes. It runs `bash doc/system/BUILD.sh`. It then fails if `git diff -- doc` shows a difference. A stale assembled reference therefore fails the check.

Do not add a required check on the Documentation CI. The workflow uses a path filter. A required check on it stays pending when the filter skips it.
