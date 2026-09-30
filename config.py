"""
Harness configuration.
Uses OpenAI-compatible API so it works with any provider.

Setup:
  cp .env.template .env   # then fill in your real values
"""
import os
from pathlib import Path


def _load_dotenv():
    """Load .env file if it exists. No third-party dependency needed."""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        # .env takes priority over shell env vars
        if key:
            os.environ[key] = value


def parse_int(name: str, raw: str) -> int:
    """Parse an int, naming the offending variable in the error message.

    Shared with profiles/base.py so every typed env var fails the same way.
    """
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"{name}={raw} is not a valid int") from None


def parse_float(name: str, raw: str) -> float:
    """Parse a float, naming the offending variable in the error message."""
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"{name}={raw} is not a valid float") from None


def parse_bool(name: str, raw: str) -> bool:
    """Parse a bool, naming the offending variable in the error message."""
    value = raw.strip().lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    raise ValueError(f"{name}={raw} is not a valid bool")


def _env_int(name: str, default: str) -> int:
    return parse_int(name, os.environ.get(name, default))


def _env_float(name: str, default: str) -> float:
    return parse_float(name, os.environ.get(name, default))


def _env_optional_float(name: str) -> float | None:
    """None when unset or blank, so callers keep their own default."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return None
    return parse_float(name, raw)


_load_dotenv()

# --- API ---
API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("HARNESS_MODEL", "gpt-4o")

# --- Token budgets ---
# Lower thresholds for models with smaller effective context windows.
# Aggressive compaction keeps the model focused and reduces latency.
COMPRESS_THRESHOLD = _env_int("COMPRESS_THRESHOLD", "50000")
RESET_THRESHOLD = _env_int("RESET_THRESHOLD", "100000")

# --- Harness loop ---
MAX_HARNESS_ROUNDS = _env_int("MAX_HARNESS_ROUNDS", "5")
PASS_THRESHOLD = _env_float("PASS_THRESHOLD", "7.0")

# --- Agent limits ---
# NOTE: Do NOT use iteration count as the primary stop condition.
# With ~8-9s per iteration, 80 iterations = ~700s, which silently
# truncates 900s+ tasks. Use a high ceiling here; TimeBudgetMiddleware
# handles the real time-based stop.
#
# Keep this default in sync with MAX_AGENT_ITERATIONS in .env.example,
# .env.template and the README configuration tables.
MAX_AGENT_ITERATIONS = _env_int("MAX_AGENT_ITERATIONS", "500")
# Consecutive API errors / empty responses before the agent loop aborts.
# Documented as MAX_TOOL_ERRORS in .env.example (the name predates the retry logic).
MAX_TOOL_ERRORS = _env_int("MAX_TOOL_ERRORS", "5")

# --- Time budget ---
# Global task time budget in seconds. When set, it overrides the budget a
# profile resolved for itself; None = keep the profile's own default.
TASK_BUDGET_SECONDS = _env_optional_float("TASK_BUDGET_SECONDS")

# --- Parallel tool calls ---
# Only enable for models that reliably produce valid parallel tool calls
# (e.g. Claude, GPT-4o). Disable for models that struggle with it.
ENABLE_PARALLEL_TOOL_CALLS = os.environ.get("ENABLE_PARALLEL_TOOL_CALLS", "0") == "1"

# --- Paths ---
WORKSPACE = os.path.abspath(os.environ.get("HARNESS_WORKSPACE", "./workspace"))
SPEC_FILE = "spec.md"
FEEDBACK_FILE = "feedback.md"
CONTRACT_FILE = "contract.md"
PROGRESS_FILE = "progress.md"
