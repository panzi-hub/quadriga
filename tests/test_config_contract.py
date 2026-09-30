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
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

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
        "print(json.dumps({n: getattr(config, n) for n in names}))\n"
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
    return load_config_values(tmp_path_factory.mktemp("config"), ["MAX_AGENT_ITERATIONS"])


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
