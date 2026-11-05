import importlib.util
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("repo_context_tools", ROOT / "scripts/repo_context_tools.py")
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


def test_feature_checkout_keeps_origin_default_identity(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    def git(*args):
        return subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True, text=True).stdout.strip()
    git("init", "-b", "master")
    git("-c", "user.name=synthetic", "-c", "user.email=synthetic@example.invalid", "commit", "--allow-empty", "-m", "synthetic")
    git("update-ref", "refs/remotes/origin/master", "HEAD")
    git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/master")
    git("checkout", "-b", "fix/synthetic")
    assert context.observed_default_branch(tmp_path) == "master"
    assert git("branch", "--show-current") == "fix/synthetic"


def test_pr_base_is_checked_in_ci(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")
    monkeypatch.setenv("GITHUB_BASE_REF", "unexpected")
    assert context.observed_default_branch(tmp_path) == "unexpected"


def test_preserved_claude_notes_are_part_of_generated_drift_check():
    expected = context.expected_instructions(ROOT)["CLAUDE.md"]
    assert expected.endswith((ROOT / "docs/claude-context-notes.txt").read_text())
