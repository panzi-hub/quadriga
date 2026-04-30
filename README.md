# Harness Engineering

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A multi-agent autonomous development framework based on Anthropic's [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

Harness automates the full development lifecycle — planning, contract negotiation, implementation, evaluation, and iterative refinement — using multiple specialized LLM agents without human intervention.

[中文](README_CN.md)

---

## Overview

Harness implements a three-agent collaborative system that transforms a natural language task description into a working application:

1. **Planner** — Analyzes requirements and generates a detailed product specification (`spec.md`).
2. **Builder** — Implements the specification, writes code, runs tests, and iterates based on feedback.
3. **Evaluator** — Assesses the output across multiple dimensions and decides whether to refine, pivot, or accept.

Before each build round, Builder and Evaluator negotiate a **sprint contract** with explicit acceptance criteria, preventing unfocused iterations.

### Workflow

```
User: "Build a Pomodoro timer"
    → Planner generates spec.md
    → Contract negotiation (Builder + Evaluator)
    → Builder writes, tests, debugs code
    → Evaluator scores (Design / Originality / Craft / Functionality)
    → If score < threshold: refine or pivot
    → If score >= threshold: done
```

---

## Features

- **Zero third-party agent SDK dependencies** — Pure Python, no LangChain, AutoGen, or CrewAI.
- **OpenAI-compatible API support** — Works with OpenAI, Anthropic (via OpenRouter), Ollama, Azure, and any compatible endpoint.
- **Context lifecycle management** — Automatic compression, anxiety detection, and hard resets with checkpointing to handle long-running tasks without context window exhaustion.
- **Profile system** — Task-specific configurations for web apps, terminal tasks, GitHub issue fixing, and reasoning.
- **Skill library** — 37+ domain-specific skills with progressive disclosure to minimize context usage.
- **Middleware system** — Loop detection, time budget enforcement, pre-exit verification, and error recovery.

---

## Quick Start

### Prerequisites

- Python 3.10+
- An OpenAI-compatible API key

### Installation

```bash
git clone https://github.com/panzi-hub/-Harness_Engineering.git
cd Harness_Engineering
pip install -r requirements.txt

# Optional: browser automation for app-builder evaluator
python -m playwright install chromium
```

### Configuration

```bash
cp .env.template .env
```

Edit `.env`:

```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

### Usage

**Web application (default profile):**

```bash
python harness.py "Build a Pomodoro timer with start, pause, and reset buttons"
```

**Terminal tasks:**

```bash
python harness.py --profile terminal "Find and fix broken symlinks in /tmp"
```

**List all profiles:**

```bash
python harness.py --list-profiles
```

Output is written to `workspace/{timestamp}_{task}/`, including the specification, contract, generated code, and evaluation feedback.

---

## Architecture

| Component | Responsibility |
|-----------|----------------|
| `harness.py` | Main orchestrator: runs the Plan → Contract → Build → Evaluate loop |
| `agents.py` | Agent runtime loop, tool execution, trace recording |
| `context.py` | Context lifecycle: compression, anxiety detection, checkpoint reset |
| `tools.py` | Tool implementations: file I/O, shell, browser, git, skills |
| `middlewares.py` | Middleware stack: loop detection, time budgets, task tracking |
| `prompts.py` | System prompts for all agent roles |
| `skills.py` | Skill registry with progressive disclosure |
| `profiles/` | Scenario-specific configurations (app-builder, terminal, swe-bench, reasoning) |
| `skills/` | Domain skill library (37+ skills) |

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | API key for the LLM provider |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API endpoint URL |
| `HARNESS_MODEL` | `gpt-4o` | Model identifier |
| `HARNESS_WORKSPACE` | `./workspace` | Output directory |
| `MAX_HARNESS_ROUNDS` | `5` | Max build-evaluate iterations |
| `PASS_THRESHOLD` | `7.0` | Minimum score to pass (0–10) |
| `COMPRESS_THRESHOLD` | `50000` | Token count to trigger context compression |
| `RESET_THRESHOLD` | `100000` | Token count to trigger context reset |
| `MAX_AGENT_ITERATIONS` | `5` | Max tool calls per agent (high ceiling; time budget middleware handles real stopping) |

---

## Provider Examples

**OpenRouter (Claude, Gemini, etc.):**

```bash
OPENAI_BASE_URL=https://openrouter.ai/api/v1
HARNESS_MODEL=anthropic/claude-sonnet-4
OPENAI_API_KEY=sk-or-your-key
```

**Ollama (local):**

```bash
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
# No API key required
```

---

## Project Structure

```
Harness_Engineering/
├── harness.py          # Entry point
├── agents.py           # Agent runtime
├── context.py          # Context management
├── tools.py            # Tool implementations
├── middlewares.py      # Middleware stack
├── prompts.py          # System prompts
├── skills.py           # Skill registry
├── config.py           # Configuration loader
├── profiles/           # Scenario profiles
│   ├── app_builder.py
│   ├── terminal.py
│   ├── swe_bench.py
│   └── reasoning.py
├── skills/             # Domain skill library
├── docs/               # Architecture and usage docs
├── tests/              # Test scripts
├── benchmarks/         # Benchmark data
└── workspace/          # Runtime output (gitignored)
```

---

## Documentation

- [Architecture Overview](docs/ARCHITECTURE_QUICK.md) — 5-minute introduction
- [Detailed Architecture](docs/ARCHITECTURE.md) — Full system design
- [Architecture Diagrams](docs/ARCHITECTURE_DIAGRAMS.md) — Visual diagrams
- [Project Structure](docs/PROJECT_STRUCTURE.md) — Directory layout
- [Profiles Guide](docs/PROFILES.md) — Using and creating profiles
- [Quick Reference](docs/QUICK_REFERENCE.md) — Command reference

---

## Contributing

Contributions are welcome. Please open an issue or pull request for bug fixes, new features, skills, or documentation improvements.

When contributing:
- Follow PEP 8 style guidelines.
- Add tests for new functionality.
- Update relevant documentation.

---

## License

MIT License — see [LICENSE](LICENSE).

---

## Acknowledgments

- [Anthropic](https://www.anthropic.com/) — Original Harness design concept
- [OpenAI](https://openai.com/) — LLM API
