# Harness — Multi-Agent Autonomous Development Architecture

[中文](README.md) | English

> Full implementation based on Anthropic's article [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps).
> 
> Built with pure Python, supports any OpenAI-compatible API endpoint, and doesn't depend on any Agent SDK.

## 🚀 Project Introduction

Harness is a powerful multi-agent autonomous development framework that can automatically complete the entire process from a single sentence request:

1. **Product Planning**: Expand short requirements into detailed product specifications
2. **Acceptance Criteria Negotiation**: Builder and Evaluator negotiate clear completion standards
3. **Code Implementation**: Automatically generate, test, and debug code
4. **Quality Evaluation**: Score based on multi-dimensional criteria
5. **Iterative Optimization**: Automatically adjust and improve based on feedback

## 🎯 Core Features

### 1. Multiple Profile Support
- **app-builder**: Build web applications from prompts (original Anthropic article scenario)
- **terminal**: Solve terminal/CLI tasks (Terminal-Bench-2 style)
- **swe-bench**: Fix GitHub issues in real repositories
- **reasoning**: Knowledge-intensive QA (MMMU-Pro style)

### 2. Three-Agent Collaboration System
- **Planner**: Expand 1-4 sentence requirements into detailed product specifications
- **Builder**: Implement code according to specifications, handle feedback for iteration
- **Evaluator**: Test applications and score based on multi-dimensional criteria

### 3. Intelligent Context Management
- **Context Anxiety Detection**: Identify signals of the model "wrapping up early"
- **Automatic Compression**: Intelligently summarize old messages when context is too large
- **Hard Reset**: Create a new context白板 when model performance declines
- **Role-Differentiated Strategies**: Customize context management schemes for different agents

### 4. Strategy Decision Mechanism
- **REFINE vs PIVOT**: Automatically decide whether to optimize the existing solution or start over based on score trends
- **Sprint Contract**: Negotiate clear acceptance criteria before each iteration
- **Sub-Agent Isolation**: Parent agents can delegate specific tasks to sub-agents to keep context clean

### 5. Skill System
- **Progressive Disclosure**: Agents autonomously load relevant skills as needed
- **Rich Skill Library**: Includes frontend design, password recovery, video processing, and many other professional skills
- **Extensible Architecture**: Easily add custom skills

### 6. Multi-Model Support
- **OpenAI**: Support for models like GPT-4o
- **OpenRouter**: Support for third-party models like Claude
- **Ollama**: Support for locally deployed models

## 📦 Project Structure

```
├── harness.py        # Main entry point, orchestrates Plan → Contract → Build → Evaluate flow
├── agents.py         # Core Agent implementation, including while loop and tool execution
├── context.py        # Context management, including compression, anxiety detection, and reset
├── tools.py          # Tool implementations, such as file operations, browser testing, etc.
├── prompts.py        # System prompts and evaluation criteria for all agents
├── skills.py         # Skill registry and management
├── skills/           # Skill library, containing various professional skills
├── profiles/         # Configuration files for different scenarios
│   ├── app_builder.py    # Web application building configuration
│   ├── terminal.py       # Terminal task configuration
│   ├── swe_bench.py       # GitHub issue fixing configuration
│   └── reasoning.py       # Knowledge-intensive QA configuration
├── config.py         # Configuration management, automatically loads environment variables
├── .env.template     # Environment variable template
├── requirements.txt  # Python dependencies
└── workspace/        # Generated project output directory
```

## 🔧 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt

# Optional: Install Playwright for browser testing
python -m playwright install chromium
```

### 2. Configure Environment

```bash
cp .env.template .env
# Edit .env file and fill in your API key
```

### 3. Run Examples

```bash
# Build a simple Pomodoro timer
python harness.py "Build a Pomodoro timer with start, pause, reset buttons. Single HTML file."

# Build an interactive periodic table
python harness.py "Build an interactive periodic table of elements with search, category filters, and element detail popups"

# Build a complete browser DAW
python harness.py "Build a fully featured DAW in the browser using the Web Audio API"

# Use terminal profile to solve terminal tasks
python harness.py --profile terminal "Fix the broken symlinks in /tmp"

# Use swe-bench profile to fix GitHub issues
python harness.py --profile swe-bench "Fix the TypeError in parse_config()"

# Use reasoning profile to answer knowledge-intensive questions
python harness.py --profile reasoning "What is the escape velocity of Mars?"
```

## 📊 Evaluation Criteria

Evaluator assesses generated applications using the following dimensions:

| Dimension | Weight | Evaluation Content |
|-----------|--------|-------------------|
| **Design Quality** | HIGH | Whether the visual design has a unified identity and whether the interface is aesthetically professional |
| **Originality** | HIGH | Whether there are custom design decisions to avoid AI default aesthetics |
| **Craft** | MEDIUM | Technical execution quality, such as typography, spacing, color harmony |
| **Functionality** | HIGH | Whether the functionality is complete and usable, and whether all interactions work properly |

## 🎨 Skill System

Harness includes a rich skill library that agents can autonomously load based on task requirements:

- **frontend-design**: Create professional frontend interfaces
- **password-recovery**: Password recovery and security analysis
- **video-processing**: Video processing and analysis
- **torch-pipeline-parallelism**: PyTorch pipeline parallelism
- **write-compressor**: Data compression algorithm implementation
- **...**: More skills are continuously being added

## 🔍 Technical Implementation

### Core Agent Loop

```python
# agents.py — Agent.run() method
for iteration in range(1, MAX_AGENT_ITERATIONS + 1):
    # 1. Context lifecycle check (compression or reset)
    # 2. Call LLM to get response
    # 3. Execute tool calls
    # 4. Append results to context
    # 5. If no more tool calls → end
```

### Context Management Strategy

```python
# context.py — Lifecycle check
if token_count > RESET_THRESHOLD or detect_anxiety(messages):
    # Write checkpoint, create new context白板
    checkpoint = create_checkpoint(messages, llm_call)
    messages = restore_from_checkpoint(checkpoint, prompt)
elif token_count > COMPRESS_THRESHOLD:
    # Summarize and compress old messages
    messages = compact_messages(messages, llm_call, role)
```

## 🌐 Multi-Model Configuration

### OpenAI
```bash
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

### OpenRouter
```bash
OPENAI_BASE_URL=https://openrouter.ai/api/v1
HARNESS_MODEL=anthropic/claude-sonnet-4
```

### Ollama (Local)
```bash
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
```

## 📈 Performance Metrics

- **Average Task Completion Time**: 30-60 minutes (depending on complexity)
- **Token Usage**: 1-3M per task
- **Cost**: $0.10-$0.50 per task (using gpt-4o)

## 🎯 Application Scenarios

- **Rapid Prototyping**: Quickly generate usable prototypes from one-sentence requirements
- **Educational Learning**: Understand the design and implementation of multi-agent systems
- **Research Experiments**: Explore the boundaries of LLM capabilities in autonomous development
- **Assistant Development**: Act as a developer's intelligent assistant, automatically completing repetitive tasks
- **Issue Fixing**: Automatically analyze and fix issues in codebases
- **Knowledge Q&A**: Answer complex knowledge-intensive questions

## 🚀 Extension Guide

### Adding Custom Skills

1. Create a new directory under `skills/`
2. Create a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-new-skill
description: One-sentence description of skill functionality
---

Detailed skill description...
```

### Adding Custom Profiles

1. Create a new Python file under `profiles/`
2. Inherit from the `BaseProfile` class and implement necessary methods
3. Register the new profile in `profiles/__init__.py`

### Adjusting System Prompts

Modify system prompts in `prompts.py` to customize agent behavior as needed.

### Configuration Tuning

Adjust the following parameters in the `.env` file:
- `MAX_HARNESS_ROUNDS`: Maximum number of iterations
- `PASS_THRESHOLD`: Passing score threshold
- `COMPRESS_THRESHOLD`: Context compression threshold
- `RESET_THRESHOLD`: Context reset threshold

## 📚 Reference Materials

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)

## 🤝 Contribution

Welcome to submit Issues and Pull Requests to help improve Harness!

## 📄 License

MIT License

---

**Harness** — Making AI autonomous development simple and powerful!