"""ProfileConfig.resolve() type coercion tests.

.env.example tells users to override profile settings from the environment
(`PROFILE_APP_BUILDER_MAX_ROUNDS=5`, ...). Those overrides must come back as the
type the harness code expects — otherwise the harness dies with a TypeError
before the first round instead of running the task.

No LLM calls, no network access.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from profiles.app_builder import AppBuilderProfile  # noqa: E402
from profiles.base import ProfileConfig  # noqa: E402
from profiles.terminal import TerminalProfile  # noqa: E402


def _config_import_error(tmp_path: Path, name: str, raw: str) -> str:
    """Import a pristine config.py with a malformed variable and return the traceback.

    The copy lives in a temp dir so a developer's local .env cannot mask the error.
    """
    shutil.copyfile(REPO_ROOT / "config.py", tmp_path / "config.py")
    env = dict(os.environ)
    env[name] = raw
    proc = subprocess.run(
        [sys.executable, "-c", "import config"],
        cwd=str(tmp_path), env=env, capture_output=True, text=True,
    )
    assert proc.returncode != 0, f"{name}={raw!r} was accepted by config.py"
    return proc.stderr


class TestEnvCoercion:
    """A typed override must come back as the type the caller asked for."""

    def test_int_field_with_none_default(self, monkeypatch):
        monkeypatch.setenv("PROFILE_APP_BUILDER_MAX_ROUNDS", "5")
        value = ProfileConfig().resolve("max_rounds", "app-builder", None)
        assert value == 5
        assert isinstance(value, int)

    def test_int_field_with_int_default(self, monkeypatch):
        monkeypatch.setenv("PROFILE_TERMINAL_MAX_ROUNDS", "4")
        value = ProfileConfig().resolve("max_rounds", "terminal", 2)
        assert value == 4
        assert isinstance(value, int)

    def test_float_field(self, monkeypatch):
        monkeypatch.setenv("PROFILE_TERMINAL_TIME_WARN_THRESHOLD", "0.45")
        value = ProfileConfig().resolve("time_warn_threshold", "terminal", 0.6)
        assert value == 0.45
        assert isinstance(value, float)

    def test_bool_field(self, monkeypatch):
        monkeypatch.setenv("PROFILE_CUSTOM_PLANNER_ENABLED", "1")
        assert ProfileConfig().resolve("planner_enabled", "custom", True) is True
        monkeypatch.setenv("PROFILE_CUSTOM_PLANNER_ENABLED", "no")
        assert ProfileConfig().resolve("planner_enabled", "custom", True) is False

    def test_string_option_keeps_raw_value(self, monkeypatch):
        """Options without a numeric contract stay exactly as written in .env."""
        monkeypatch.setenv("PROFILE_CUSTOM_MODEL", "gpt-4o-mini")
        assert ProfileConfig().resolve("model", "custom", None) == "gpt-4o-mini"

    def test_explicit_config_still_wins_over_default(self, monkeypatch):
        monkeypatch.delenv("PROFILE_TERMINAL_MAX_ROUNDS", raising=False)
        assert ProfileConfig(max_rounds=3).resolve("max_rounds", "terminal", 2) == 3


class TestHarnessIntegration:
    """The documented overrides must be usable where the harness actually reads them."""

    def test_app_builder_max_rounds_override_is_an_int(self, monkeypatch):
        monkeypatch.setenv("PROFILE_APP_BUILDER_MAX_ROUNDS", "5")
        rounds = AppBuilderProfile().max_rounds()
        assert rounds == 5
        # harness.py iterates range(1, max_rounds + 1) — a str raises TypeError here
        assert list(range(1, (rounds or 1) + 1)) == [1, 2, 3, 4, 5]

    def test_terminal_budget_override_is_numeric(self, monkeypatch):
        monkeypatch.setenv("PROFILE_TERMINAL_TASK_BUDGET", "900")
        assert TerminalProfile()._get("task_budget") == 900


class TestInvalidValues:
    """A malformed override must name the variable and the expected type."""

    def test_profile_int_error_names_variable(self, monkeypatch):
        monkeypatch.setenv("PROFILE_APP_BUILDER_MAX_ROUNDS", "abc")
        with pytest.raises(ValueError) as excinfo:
            ProfileConfig().resolve("max_rounds", "app-builder", None)
        assert "PROFILE_APP_BUILDER_MAX_ROUNDS=abc is not a valid int" in str(excinfo.value)

    def test_profile_float_error_names_variable(self, monkeypatch):
        monkeypatch.setenv("PROFILE_TERMINAL_PASS_THRESHOLD", "high")
        with pytest.raises(ValueError) as excinfo:
            ProfileConfig().resolve("pass_threshold", "terminal", 8.0)
        assert "PROFILE_TERMINAL_PASS_THRESHOLD=high is not a valid float" in str(excinfo.value)

    def test_profile_bool_error_names_variable(self, monkeypatch):
        monkeypatch.setenv("PROFILE_CUSTOM_PLANNER_ENABLED", "maybe")
        with pytest.raises(ValueError) as excinfo:
            ProfileConfig().resolve("planner_enabled", "custom", True)
        assert "PROFILE_CUSTOM_PLANNER_ENABLED=maybe is not a valid bool" in str(excinfo.value)

    @pytest.mark.parametrize(
        "name,raw,expected_type",
        [
            ("MAX_AGENT_ITERATIONS", "abc", "int"),
            ("MAX_TOOL_ERRORS", "two", "int"),
            ("COMPRESS_THRESHOLD", "many", "int"),
            ("RESET_THRESHOLD", "lots", "int"),
            ("MAX_HARNESS_ROUNDS", "a-few", "int"),
            ("PASS_THRESHOLD", "high", "float"),
            ("TASK_BUDGET_SECONDS", "soon", "float"),
        ],
    )
    def test_config_bad_value_names_variable(self, tmp_path, name, raw, expected_type):
        stderr = _config_import_error(tmp_path, name, raw)
        assert f"{name}={raw} is not a valid {expected_type}" in stderr
