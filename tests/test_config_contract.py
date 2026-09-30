"""Configuration contract tests.

These tests pin the behaviour that README.md / .env.example / .env.template
promise to the configuration code, so defaults and documentation cannot drift
apart again.

Everything here is a pure unit test: no LLM calls, no network, no provider SDK.
config.py is loaded in a subprocess from a temporary copy, so a developer's
local .env file cannot leak into the assertions.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

_MISSING = "<not defined>"

# Environment variables read by config.py. Scrubbed before loading a pristine
# copy so the caller's environment cannot influence the assertions.
CONFIG_ENV_KEYS = (
    "MAX_AGENT_ITERATIONS",
    "MAX_TOOL_ERRORS",
    "TASK_BUDGET_SECONDS",
    "MAX_HARNESS_ROUNDS",
    "PASS_THRESHOLD",
    "COMPRESS_THRESHOLD",
    "RESET_THRESHOLD",
    "ENABLE_PARALLEL_TOOL_CALLS",
    "HARNESS_WORKSPACE",
)


def load_config_values(tmp_path: Path, names, **env_overrides):
    """Import a pristine copy of config.py in a subprocess and read values from it.

    Returns a dict of {name: value} as seen by the fresh module import.
    """
    shutil.copyfile(REPO_ROOT / "config.py", tmp_path / "config.py")
    script = (
        "import json, config\n"
        f"names = {list(names)!r}\n"
        f"missing = {_MISSING!r}\n"
        "print(json.dumps({n: getattr(config, n, missing) for n in names}))\n"
    )
    env = {k: v for k, v in os.environ.items() if k not in CONFIG_ENV_KEYS}
    env.update({k: str(v) for k, v in env_overrides.items()})

    proc = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(tmp_path), env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"config.py failed to import:\n{proc.stderr}"
    return json.loads(proc.stdout.strip().splitlines()[-1])


def documented_env_value(path: Path, key: str) -> str | None:
    """First `KEY=value` occurrence in a dotenv template.

    Commented examples count — both templates document optional settings
    with a leading `#`.
    """
    pattern = re.compile(rf"^\s*#?\s*{re.escape(key)}\s*=\s*(.*?)\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1)
    return None


def readme_table_default(path: Path, key: str) -> str | None:
    """Default column of a row in the README configuration table."""
    pattern = re.compile(
        rf"^\|\s*`{re.escape(key)}`\s*\|\s*`?([^`|]+?)`?\s*\|", re.MULTILINE
    )
    match = pattern.search(path.read_text(encoding="utf-8"))
    return match.group(1).strip() if match else None


@pytest.fixture(scope="module")
def defaults(tmp_path_factory) -> dict:
    """Default values of the configuration knobs under test (no env overrides)."""
    return load_config_values(
        tmp_path_factory.mktemp("config"),
        ["MAX_AGENT_ITERATIONS", "MAX_TOOL_ERRORS", "TASK_BUDGET_SECONDS"],
    )


class TestMaxAgentIterations:
    """MAX_AGENT_ITERATIONS is documented as a high ceiling, not a 5-step leash."""

    def test_default_is_the_high_ceiling(self, defaults):
        assert defaults["MAX_AGENT_ITERATIONS"] == 500

    def test_env_override_still_wins(self, tmp_path):
        values = load_config_values(
            tmp_path, ["MAX_AGENT_ITERATIONS"], MAX_AGENT_ITERATIONS="12"
        )
        assert values["MAX_AGENT_ITERATIONS"] == 12

    @pytest.mark.parametrize("template", [".env.example", ".env.template"])
    def test_default_matches_env_templates(self, defaults, template):
        documented = documented_env_value(REPO_ROOT / template, "MAX_AGENT_ITERATIONS")
        assert documented is not None, f"{template} no longer documents MAX_AGENT_ITERATIONS"
        assert documented == str(defaults["MAX_AGENT_ITERATIONS"])

    @pytest.mark.parametrize("readme", ["README.md", "README_CN.md"])
    def test_default_matches_readme_table(self, defaults, readme):
        documented = readme_table_default(REPO_ROOT / readme, "MAX_AGENT_ITERATIONS")
        assert documented is not None, f"{readme} no longer documents MAX_AGENT_ITERATIONS"
        assert documented == str(defaults["MAX_AGENT_ITERATIONS"])


class TestMaxToolErrors:
    """MAX_TOOL_ERRORS is documented in .env.example and must be honored."""

    def test_default_matches_env_example(self, defaults):
        documented = documented_env_value(REPO_ROOT / ".env.example", "MAX_TOOL_ERRORS")
        assert documented is not None, ".env.example no longer documents MAX_TOOL_ERRORS"
        assert documented == str(defaults["MAX_TOOL_ERRORS"])

    def test_env_override_is_read(self, tmp_path):
        values = load_config_values(tmp_path, ["MAX_TOOL_ERRORS"], MAX_TOOL_ERRORS="3")
        assert values["MAX_TOOL_ERRORS"] == 3


class TestTaskBudgetSeconds:
    """TASK_BUDGET_SECONDS is an optional global override for profile budgets."""

    def test_unset_means_no_global_override(self, defaults):
        assert defaults["TASK_BUDGET_SECONDS"] is None

    def test_env_value_is_parsed_as_seconds(self, tmp_path):
        values = load_config_values(
            tmp_path, ["TASK_BUDGET_SECONDS"], TASK_BUDGET_SECONDS="900"
        )
        assert values["TASK_BUDGET_SECONDS"] == 900.0

    @pytest.mark.parametrize("template", [".env.example", ".env.template"])
    def test_documented_in_env_templates(self, template):
        documented = documented_env_value(REPO_ROOT / template, "TASK_BUDGET_SECONDS")
        assert documented is not None, f"{template} no longer documents TASK_BUDGET_SECONDS"

    @pytest.mark.parametrize("readme", ["README.md", "README_CN.md"])
    def test_documented_in_readme_table(self, readme):
        documented = readme_table_default(REPO_ROOT / readme, "TASK_BUDGET_SECONDS")
        assert documented is not None, f"{readme} no longer documents TASK_BUDGET_SECONDS"

    def test_overrides_profile_budget(self, monkeypatch):
        from profiles.terminal import TerminalProfile

        monkeypatch.delenv("PROFILE_TERMINAL_TASK_BUDGET", raising=False)
        monkeypatch.setenv("TASK_BUDGET_SECONDS", "600")
        assert TerminalProfile()._get("task_budget") == 600.0

    def test_profile_specific_env_wins_over_global(self, monkeypatch):
        from profiles.terminal import TerminalProfile

        monkeypatch.setenv("TASK_BUDGET_SECONDS", "600")
        monkeypatch.setenv("PROFILE_TERMINAL_TASK_BUDGET", "1200")
        assert TerminalProfile()._get("task_budget") == 1200


# ---------------------------------------------------------------------------
# Loop stop conditions — fake clock, stub LLM client, no network
# ---------------------------------------------------------------------------

class _CountingCompletions:
    """Minimal stand-in for client.chat.completions that only counts calls."""

    def __init__(self, error: Exception | None = None):
        self.error = error
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        if self.error is not None:
            raise self.error
        raise AssertionError("the agent loop called the LLM unexpectedly")


class _FakeClient:
    """Drop-in for the OpenAI client used by agents.get_client()."""

    def __init__(self, completions):
        self.chat = types.SimpleNamespace(completions=completions)


@pytest.fixture
def agents_module(monkeypatch, tmp_path):
    """Import agents.py without the openai package and with an isolated workspace.

    Tests must never reach a provider, so add a stub `openai` module to
    sys.modules before importing the real agents module.
    """
    stub = types.ModuleType("openai")
    stub.OpenAI = object  # only needed as an annotation target
    monkeypatch.setitem(sys.modules, "openai", stub)
    sys.modules.pop("agents", None)
    import agents  # noqa: PLC0415 — deliberately imported after the stub

    monkeypatch.setattr(agents.config, "WORKSPACE", str(tmp_path))
    monkeypatch.setattr(agents.time, "sleep", lambda *_args, **_kwargs: None)
    return agents


def _trace_events(tmp_path: Path, agent_name: str) -> list[dict]:
    trace = tmp_path / f"_trace_{agent_name}.jsonl"
    assert trace.exists(), "agent did not write a trace file"
    return [json.loads(line) for line in trace.read_text(encoding="utf-8").splitlines()]


class TestTimeBudgetStopsTheLoop:
    """A budget that only produces advice never stops anything."""

    def test_no_stop_while_budget_remains(self):
        from middlewares import TimeBudgetMiddleware

        mw = TimeBudgetMiddleware(budget_seconds=1800)
        mw.start_time = time.time() - 60
        assert mw.stop_reason() is None

    def test_stop_reason_once_budget_is_exhausted(self):
        from middlewares import TimeBudgetMiddleware

        mw = TimeBudgetMiddleware(budget_seconds=30)
        mw.start_time = time.time() - 31
        reason = mw.stop_reason()
        assert reason, "an exhausted budget must stop the loop"
        assert "time_budget" in reason

    def test_agent_loop_stops_without_another_llm_call(self, agents_module, tmp_path):
        from middlewares import TimeBudgetMiddleware

        completions = _CountingCompletions()
        agents_module.get_client = lambda: _FakeClient(completions)  # type: ignore[assignment]

        agent = agents_module.Agent(
            "builder", "system prompt", middlewares=[TimeBudgetMiddleware(budget_seconds=1)]
        )
        agent.middlewares[0].start_time = time.time() - 5

        result = agent.run("do something")

        assert completions.calls == 0, "the loop spent an LLM call after the budget expired"
        assert "time_budget_exceeded" in result
        finishes = [e for e in _trace_events(tmp_path, "builder") if e["event"] == "finish"]
        assert finishes and finishes[-1]["reason"] == "time_budget_exceeded"


class TestMaxToolErrorsStopsTheLoop:
    """Hitting the documented API-error limit must end the loop, not retry forever."""

    def test_agent_loop_aborts_at_the_configured_limit(self, agents_module, tmp_path):
        completions = _CountingCompletions(error=RuntimeError("upstream connection reset"))
        agents_module.get_client = lambda: _FakeClient(completions)  # type: ignore[assignment]

        agents_module.config.MAX_TOOL_ERRORS = 2
        agent = agents_module.Agent("builder", "system prompt")

        result = agent.run("do something")

        assert completions.calls == 2, "the loop kept retrying past MAX_TOOL_ERRORS"
        assert "MAX_TOOL_ERRORS" in result
        finishes = [e for e in _trace_events(tmp_path, "builder") if e["event"] == "finish"]
        assert finishes and finishes[-1]["reason"] == "api_errors"
