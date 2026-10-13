# quadriga

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A pure-Python multi-agent harness for long-running tasks. It turns one prompt into a planned, built, tested, and scored result through an OpenAI-compatible API. No LangChain, AutoGen, or CrewAI.

The design follows Anthropic's [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).

[中文](README_CN.md)

---

## Simple overview

```
task
  -> Planner        spec.md
  -> Proposer       contract.md          app-builder only
  -> Reviewer       APPROVED / revise    up to 3 passes
  -> Builder        code / patch / answer.md
  -> Evaluator      feedback.md
       |  score >= threshold
       |    done
       |  score dropped
       |    roll back, then Builder again
       |  otherwise
       +--> Builder again, with feedback.md
```

Planner, contract, and Evaluator can be absent. A profile that skips them goes straight to Builder.

## Call chain

`python harness.py` does not send the task to one model and stop. It builds a profile, constructs up to five agents, then drives them through a fixed outer loop. Each agent has its own inner tool loop. Profiles decide which agents exist and which tools they get.

| Profile | What it is for | Planner | Contract | Evaluator | Default pass |
|---|---|---|---|---|---|
| `app-builder` | Web apps from a prompt | on | on | on, plus browser tools | 7.0 |
| `terminal` | CLI / Terminal-Bench-style tasks | often skipped | off | on | 8.0, max 2 rounds |
| `swe-bench` | Diagnose and patch a repository issue | on | off | on | 7.0 |
| `reasoning` | Knowledge and calculation tasks | on | off | on | 7.0 |

Only `app-builder` enables contract negotiation. The other profiles inherit the disabled contract agents from `BaseProfile`.

---

## Call chain

```
python harness.py [--profile NAME] "task"
        │
        ▼
main()                                          harness.py
  ├─ parse --profile / --list-profiles / --verbose
  ├─ get_profile(name)                          profiles/__init__.py
  ├─ create workspace/{timestamp}_{slug}/
  ├─ git init
  ├─ API preflight (skipped in benchmark mode)
  └─ Harness(profile).run(task)
        │
        ▼
Harness.__init__                                harness.py
  ├─ SkillRegistry.build_catalog_prompt()       skills.py
  ├─ profile.planner/builder/evaluator()
  ├─ profile.contract_proposer/reviewer()
  └─ Agent(name, prompt, tools, middlewares)    agents.py
        │
        ▼
Harness.run(task)
  ├─ profile.resolve_time_allocation(task)
  │
  ├─ 1. PLAN
  │    planner.run("write spec.md")             if planner enabled
  │    else write the raw prompt to spec.md
  │
  └─ 2. for round in 1..max_rounds
       ├─ CONTRACT                              app-builder only
       │    proposer.run  -> contract.md
       │    reviewer.run  -> APPROVED or revise
       │    repeat up to 3 times
       ├─ git tag round-N-start
       ├─ BUILD
       │    profile.format_build_task(...)
       │    builder.run(task)                   reads spec/feedback/contract
       ├─ git tag round-N-end
       └─ EVALUATE                              if evaluator enabled
            evaluator.run("write feedback.md")
            profile.extract_score(feedback.md)
            score >= threshold -> stop
            score dropped      -> git reset --hard round-(N-1)-end
```

Outer-loop limits come from the profile, then from `MAX_HARNESS_ROUNDS` (default 5) and `PASS_THRESHOLD` (default 7.0). A profile can also disable the planner or evaluator through `resolve_time_allocation()`.

### What each agent is told to do

| Agent | Writes | Stops when |
|---|---|---|
| Planner | `spec.md` | It stops calling tools |
| Contract proposer | `contract.md` | Reviewer writes `APPROVED`, or 3 review passes end |
| Contract reviewer | revised `contract.md` | Same contract loop |
| Builder | application files, patches, or `answer.md` | Its tool loop ends, or a middleware hard-stops it |
| Evaluator | `feedback.md` with `Average: X/10` | Its tool loop ends |

`format_build_task()` feeds the original prompt, the previous `feedback.md`, and the score history back into the next Builder round. That is the refine path. The pivot path is the git rollback in `Harness.run` when the new score is lower than the previous one.

### Inside one `Agent.run`

This loop is the same for every role. The profile only changes the prompt, tool schema, middleware, and time budget.

```
Agent.run(task)                                 agents.py
  messages = [system prompt + skill catalog, user task]
  trace = workspace/_trace_{role}.jsonl

  for iteration in 1..MAX_AGENT_ITERATIONS:     default 500
    ├─ middleware.stop_reason()                 hard stop, no further model call
    ├─ middleware.per_iteration()               optional injected user message
    ├─ count_tokens(messages)                   context.py
    │    > RESET_THRESHOLD or anxiety -> checkpoint, then restore
    │    > COMPRESS_THRESHOLD         -> compact_messages()
    ├─ chat.completions.create(                 OpenAI-compatible API
    │       model, messages, tools, tool_choice=auto)
    ├─ no tool_calls?
    │    middleware.pre_exit() may force another turn
    │    otherwise return the assistant text
    └─ for each tool_call:
         execute_tool(name, args)               tools.py
           validate/fix args -> TOOL_DISPATCH -> post-process
         append tool result
         middleware.post_tool()                 optional injected nudge
```

A skill is not selected by the harness. The catalog is only names and descriptions in the system prompt. The agent loads `skills/<name>/SKILL.md` itself with `read_skill_file` when it decides the skill is relevant.

### Tool and middleware chain

```
model tool_call
  -> tools.execute_tool
       -> _validate_and_fix
       -> read_file | write_file | edit_file | list_files
          run_bash | delegate_task | read_skill_file
          web_search | web_fetch
          browser_test | stop_dev_server          evaluator only
       -> empty-result marker / large-output spill
  -> AgentMiddleware.post_tool / pre_exit / stop_reason
       LoopDetection | TimeBudget | PreExitVerification
       TaskTracking | SkeletonDetection | ErrorGuidance
```

File tools are sandboxed to the workspace. `delegate_task` runs a nested model call so a long exploration does not have to stay in the parent context. Browser tools are attached only by `AppBuilderProfile.evaluator()`.

### Files the loop leaves behind

```
workspace/{timestamp}_{slug}/
├── spec.md                  planner output, or the raw prompt
├── contract.md              app-builder sprint contract
├── feedback.md              evaluator score and critique
├── progress.md              optional agent progress notes
├── _trace_{role}.jsonl      one trace per agent role
└── .git                     round-N-start / round-N-end tags
```

`HARNESS_FLAT_WORKSPACE=1` skips the timestamped directory and the API preflight. Benchmark runners use that mode.

---

## Quick start

```bash
git clone https://github.com/panzi-hub/quadriga.git
cd quadriga
pip install -r requirements.txt
python -m playwright install chromium   # only for app-builder browser evaluation

cp .env.template .env
```

```bash
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

```bash
python harness.py "Build an interactive kanban board with drag-and-drop and local storage"
python harness.py --profile terminal "Find and fix broken symlinks in /tmp"
python harness.py --profile swe-bench "Fix the TypeError in parse_config()"
python harness.py --profile reasoning "What is the escape velocity of Mars?"
python harness.py --list-profiles
```

---

## Configuration

| Variable | Default | Used by |
|---|---|---|
| `OPENAI_API_KEY` | — | `agents.get_client()` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API client |
| `HARNESS_MODEL` | `gpt-4o` | every model call |
| `HARNESS_WORKSPACE` | `./workspace` | project output |
| `MAX_HARNESS_ROUNDS` | `5` | outer loop, if the profile does not override it |
| `PASS_THRESHOLD` | `7.0` | fallback pass score |
| `COMPRESS_THRESHOLD` | `50000` | inner-loop compaction |
| `RESET_THRESHOLD` | `100000` | inner-loop checkpoint reset |
| `MAX_AGENT_ITERATIONS` | `500` | inner loop ceiling |
| `MAX_TOOL_ERRORS` | `5` | consecutive API errors before abort |
| `TASK_BUDGET_SECONDS` | unset | global override of every profile time budget |
| `ENABLE_PARALLEL_TOOL_CALLS` | `0` | off unless the model handles parallel calls reliably |

Profile values can also be overridden without editing code, for example `PROFILE_TERMINAL_PASS_THRESHOLD=9` or `PROFILE_TERMINAL_TASK_BUDGET=1800`.

OpenRouter and local OpenAI-compatible servers work by changing `OPENAI_BASE_URL` and `HARNESS_MODEL`.

---

## Repository map

| Path | Role in the call chain |
|---|---|
| `harness.py` | CLI, outer loop, contract loop, git tags, score decision |
| `agents.py` | Inner model/tool loop and JSONL traces |
| `profiles/` | Which agents, tools, prompts, budgets, and scores a scenario uses |
| `prompts.py` | Role prompts for the app-builder path |
| `tools.py` | Tool schemas and `execute_tool` dispatch |
| `middlewares.py` | Stop conditions and injected course corrections |
| `context.py` | Token counting, compaction, anxiety detection, checkpoints |
| `skills.py`, `skills/` | Catalog plus 36 on-demand domain skills |
| `config.py` | Environment loading and loop thresholds |
| `benchmarks/` | Terminal-Bench task metadata and runner glue |
| `tests/` | Config contract, sandbox path, and API checks |

More detail: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/PROFILES.md](docs/PROFILES.md), [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md).

---

## License

MIT. See [LICENSE](LICENSE).
