"""
Regression tests for the workspace / skills path sandbox in tools.py.

The containment check used to be a raw string prefix comparison,
`str(p).startswith(str(root))`, which has two holes:

  * a sibling directory that merely shares the prefix is accepted, because
    "/base/workspace2/x" does start with "/base/workspace" -- so
    "../workspace2/secret.txt" walked straight out of the sandbox;
  * the comparison is case-sensitive while the filesystem is not, so a
    differently-cased path was rejected on Windows.

These tests pin down both directions: escapes must be refused, and legal
in-workspace paths (including ".." that stays inside) must keep working.

Only the path helpers are exercised directly -- no shell execution.
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

import config  # noqa: E402
import tools  # noqa: E402

REJECTED = "[error]"


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def workspace(tmp_path):
    """A real workspace plus a sibling that shares its name prefix."""
    ws = tmp_path / "workspace"
    (ws / "sub").mkdir(parents=True)
    (ws / "inner.txt").write_text("inside", encoding="utf-8")
    (ws / "sub" / "deep.txt").write_text("deep", encoding="utf-8")

    sibling = tmp_path / "workspace2"
    sibling.mkdir()
    (sibling / "secret.txt").write_text("SECRET", encoding="utf-8")

    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.txt").write_text("SECRET", encoding="utf-8")

    return ws


@pytest.fixture
def fake_project(tmp_path, monkeypatch):
    """A fake project root, wired into read_skill_file via its __file__."""
    root = tmp_path / "proj"
    (root / "skills" / "demo").mkdir(parents=True)
    (root / "skills" / "demo" / "SKILL.md").write_text("demo skill", encoding="utf-8")

    sibling = root / "skills2"
    sibling.mkdir()
    (sibling / "secret.txt").write_text("SECRET", encoding="utf-8")

    monkeypatch.setattr(tools, "__file__", str(root / "tools.py"))
    return root


# ---------------------------------------------------------------------------
# _resolve -- workspace sandbox
# ---------------------------------------------------------------------------

def test_sibling_dir_escape_denied(workspace, monkeypatch):
    """../workspace2/x must not pass just because '/workspace' is a prefix."""
    monkeypatch.setattr(config, "WORKSPACE", str(workspace))
    with pytest.raises(ValueError):
        tools._resolve("../workspace2/secret.txt")


def test_absolute_outside_denied(workspace, monkeypatch):
    monkeypatch.setattr(config, "WORKSPACE", str(workspace))
    outside = workspace.parent / "outside" / "secret.txt"
    with pytest.raises(ValueError):
        tools._resolve(str(outside))
    with pytest.raises(ValueError):
        tools._resolve(str(workspace.parent / "workspace2" / "secret.txt"))


def test_dotdot_inside_allowed(workspace, monkeypatch):
    """A '..' that still lands inside the workspace must not be over-blocked."""
    monkeypatch.setattr(config, "WORKSPACE", str(workspace))
    assert tools._resolve("sub/../inner.txt") == (workspace / "inner.txt")
    assert tools._resolve("sub/../sub/deep.txt") == (workspace / "sub" / "deep.txt")
    # ...while one that really leaves the tree is still refused.
    with pytest.raises(ValueError):
        tools._resolve("sub/../../inner.txt")


def test_trailing_separator_ok(workspace, monkeypatch):
    """Configured root with / without a trailing separator behaves the same."""
    for root in (str(workspace), str(workspace) + os.sep):
        monkeypatch.setattr(config, "WORKSPACE", root)
        assert tools._resolve("inner.txt") == (workspace / "inner.txt")
        assert tools._resolve("sub/deep.txt") == (workspace / "sub" / "deep.txt")


@pytest.mark.skipif(os.name != "nt", reason="case-insensitive filesystem only")
def test_windows_case(workspace, monkeypatch, tmp_path):
    """Different case for the same location is not an escape."""
    monkeypatch.setattr(config, "WORKSPACE", str(workspace).upper())
    try:
        resolved = tools._resolve("inner.txt")
    except ValueError:
        pytest.fail("case-only difference was treated as an escape")
    assert resolved == (workspace / "inner.txt")

    # Same, for a workspace that does not exist yet: resolve() cannot
    # canonicalise it, so case folding has to happen in the comparison.
    pending = tmp_path / "not_created_yet"
    monkeypatch.setattr(config, "WORKSPACE", str(pending).upper())
    pending_file = str(pending).lower() + os.sep + "inner.txt"
    try:
        tools._resolve(pending_file)
    except ValueError:
        pytest.fail("case-only difference was treated as an escape")


# ---------------------------------------------------------------------------
# read_skill_file -- skills sandbox
# ---------------------------------------------------------------------------

def test_skill_sibling_dir_escape_denied(fake_project):
    """skills2/x shares the '/skills' prefix and must be refused."""
    result = tools.read_skill_file("skills2/secret.txt")
    assert result.startswith(REJECTED), result


def test_skill_absolute_outside_denied(fake_project, tmp_path):
    assert tools.read_skill_file(str(tmp_path / "outside.txt")).startswith(REJECTED)


def test_skill_dotdot_inside_allowed(fake_project):
    result = tools.read_skill_file("skills/demo/../demo/SKILL.md")
    assert not result.startswith(REJECTED), result
    assert result == "demo skill"


def test_skill_trailing_separator_ok(fake_project):
    result = tools.read_skill_file(os.path.join("skills", "demo", "SKILL.md"))
    assert not result.startswith(REJECTED), result
    assert result == "demo skill"


@pytest.mark.skipif(os.name != "nt", reason="case-insensitive filesystem only")
def test_skill_windows_case(fake_project, tmp_path, monkeypatch):
    """A case-only difference must not be mistaken for a sandbox escape.

    The root does not exist, so resolve() cannot canonicalise its case and
    the comparison itself has to fold it. The read that follows fails with
    "not found", which proves the path cleared the sandbox check.
    """
    root = tmp_path / "caseproj"
    monkeypatch.setattr(tools, "__file__", str(root).upper() + os.sep + "tools.py")
    pending = str(root).lower() + os.sep + "skills" + os.sep + "demo" + os.sep + "SKILL.md"
    result = tools.read_skill_file(pending)
    assert "must be inside skills/" not in result, result


# ---------------------------------------------------------------------------
# keep the real repository layout working
# ---------------------------------------------------------------------------

def test_real_skill_file_still_readable():
    """The shipped skills/ tree must remain reachable through the sandbox."""
    result = tools.read_skill_file("skills/frontend-design/SKILL.md")
    assert not result.startswith(REJECTED), result
    assert "frontend-design" in result


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
