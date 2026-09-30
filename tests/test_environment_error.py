"""Regression tests for environment-error detection in tools.py.

``_detect_environment_error`` calls ``re.search``, but ``re`` was only imported
inside five unrelated functions. The module never bound the name at import time,
so every ``run_bash`` call raised ``NameError`` while inspecting its output; the
broad ``except Exception`` in ``run_bash`` then replaced the real stdout/stderr
with an ``[error] name 're' is not defined`` string. Commands still executed —
the agent just never saw their output or exit code.

These tests run under pytest and standalone (``python tests/test_environment_error.py``).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile

import config
import tools


def test_detect_environment_error_no_nameerror():
    """The detector must be callable with no command matching any pattern."""
    result = tools._detect_environment_error("ping baidu.com")
    assert isinstance(result, str), f"expected str, got {type(result)!r}"


def test_detect_environment_error_suggests_fix():
    """The regex table must still produce a suggestion when a pattern matches."""
    result = tools._detect_environment_error("bash: npm: command not found")
    assert "[SUGGESTED FIX]" in result, result


def test_run_bash_returns_output():
    """run_bash must return real stdout instead of a swallowed NameError."""
    original_workspace = config.WORKSPACE
    with tempfile.TemporaryDirectory() as tmpdir:
        config.WORKSPACE = tmpdir
        try:
            output = tools.run_bash("echo quadriga_re_ok")
        finally:
            config.WORKSPACE = original_workspace

    assert "quadriga_re_ok" in output, f"command output was lost: {output!r}"
    assert "NameError" not in output, output
    assert "name 're' is not defined" not in output, output
    assert not output.startswith("[error]"), output


if __name__ == "__main__":
    tests = [
        test_detect_environment_error_no_nameerror,
        test_detect_environment_error_suggests_fix,
        test_run_bash_returns_output,
    ]
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"PASS {test.__name__}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
