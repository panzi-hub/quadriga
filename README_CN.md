# Harness Engineering

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) | 中文

---

基于 Anthropic 文章 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 实现的多智能体自主开发框架。

Harness 通过多个专用 LLM Agent 协同工作，自动化完成需求规划、合同协商、代码实现、质量评估与迭代优化的完整开发生命周期，无需人工干预。

---

## 概述

Harness 采用三 Agent 协作架构，将自然语言任务描述转换为可运行的应用程序：

1. **Planner（规划师）** — 分析需求，生成详细的产品规格文档（`spec.md`）。
2. **Builder（构建师）** — 根据规格实现代码，执行测试，并基于反馈迭代优化。
3. **Evaluator（评估师）** — 从多维度评估产出，决定是优化（REFINE）、转向（PIVOT）还是通过（ACCEPT）。

每轮构建前，Builder 与 Evaluator 会协商一份**冲刺合同（Sprint Contract）**，明确本轮验收标准，避免无目标的迭代。

### 工作流程

```
用户输入: "做一个支持拖拽排序、可自定义列的交互式看板应用"
    → Planner 生成 spec.md
    → 合同协商（Builder + Evaluator）
    → Builder 编写、测试、调试代码
    → Evaluator 评分（设计 / 原创性 / 工艺 / 功能性）
    → 分数 < 阈值: 优化或转向
    → 分数 >= 阈值: 完成
```

---

## 特性

- **零第三方 Agent SDK 依赖** — 纯 Python 实现，不依赖 LangChain、AutoGen 或 CrewAI。
- **兼容任意 OpenAI 格式 API** — 支持 OpenAI、Anthropic（通过 OpenRouter）、Ollama、Azure 等。
- **上下文生命周期管理** — 自动压缩、焦虑检测与硬重置检查点，避免长任务超出上下文窗口。
- **Profile 场景系统** — 针对网页应用、终端任务、GitHub Issue 修复、推理问答等场景的配置。
- **技能库** — 37+ 领域技能，采用渐进式披露策略以最小化上下文占用。
- **中间件系统** — 死循环检测、时间预算控制、退出前验证与错误恢复。

---

## 快速开始

### 环境要求

- Python 3.10+
- 任意 OpenAI 兼容 API Key

### 安装

```bash
git clone https://github.com/panzi-hub/-Harness_Engineering.git
cd Harness_Engineering
pip install -r requirements.txt

# 可选：安装浏览器自动化依赖（用于 app-builder 评估）
python -m playwright install chromium
```

### 配置

```bash
cp .env.template .env
```

编辑 `.env`：

```bash
OPENAI_API_KEY=sk-your-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

### 使用

**网页应用（默认 Profile）：**

```bash
python harness.py "Build an interactive kanban board with drag-and-drop, column customization, and local storage persistence"
```

**终端任务：**

```bash
python harness.py --profile terminal "Find and fix broken symlinks in /tmp"
```

**查看所有 Profile：**

```bash
python harness.py --list-profiles
```

任务输出保存在 `workspace/{时间戳}_{任务}/` 目录下，包含规格文档、合同、生成的代码和评估反馈。

---

## 架构

| 组件 | 职责 |
|-----------|----------------|
| `harness.py` | 主编排器：执行 Plan → Contract → Build → Evaluate 循环 |
| `agents.py` | Agent 运行时循环、工具执行、轨迹记录 |
| `context.py` | 上下文生命周期：压缩、焦虑检测、检查点重置 |
| `tools.py` | 工具实现：文件 I/O、Shell、浏览器、Git、技能 |
| `middlewares.py` | 中间件栈：死循环检测、时间预算、任务追踪 |
| `prompts.py` | 所有 Agent 角色的系统提示词 |
| `skills.py` | 支持渐进式披露的技能注册表 |
| `profiles/` | 场景配置（app-builder、terminal、swe-bench、reasoning） |
| `skills/` | 领域技能库（37+ 技能） |

详细架构文档见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

---

## 配置参考

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | LLM 提供商的 API Key |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API 端点地址 |
| `HARNESS_MODEL` | `gpt-4o` | 模型标识符 |
| `HARNESS_WORKSPACE` | `./workspace` | 输出目录 |
| `MAX_HARNESS_ROUNDS` | `5` | 最大构建-评估迭代次数 |
| `PASS_THRESHOLD` | `7.0` | 通过最低分（0–10） |
| `COMPRESS_THRESHOLD` | `50000` | 触发上下文压缩的 Token 阈值 |
| `RESET_THRESHOLD` | `100000` | 触发上下文重置的 Token 阈值 |
| `MAX_AGENT_ITERATIONS` | `5` | Agent 最大工具调用次数（高上限；实际停止由 TimeBudgetMiddleware 控制） |

---

## 提供商配置示例

**OpenRouter（Claude、Gemini 等）：**

```bash
OPENAI_BASE_URL=https://openrouter.ai/api/v1
HARNESS_MODEL=anthropic/claude-sonnet-4
OPENAI_API_KEY=sk-or-your-key
```

**Ollama（本地部署）：**

```bash
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
# 无需 API Key
```

---

## 项目结构

```
Harness_Engineering/
├── harness.py          # 入口
├── agents.py           # Agent 运行时
├── context.py          # 上下文管理
├── tools.py            # 工具实现
├── middlewares.py      # 中间件栈
├── prompts.py          # 系统提示词
├── skills.py           # 技能注册表
├── config.py           # 配置加载器
├── profiles/           # 场景配置
│   ├── app_builder.py
│   ├── terminal.py
│   ├── swe_bench.py
│   └── reasoning.py
├── skills/             # 领域技能库
├── docs/               # 架构与使用文档
├── tests/              # 测试脚本
├── benchmarks/         # 基准测试数据
└── workspace/          # 运行时输出（gitignored）
```

---

## 文档

- [快速架构概览](docs/ARCHITECTURE_QUICK.md) — 5 分钟了解核心架构
- [详细架构文档](docs/ARCHITECTURE.md) — 完整系统设计
- [架构可视化图表](docs/ARCHITECTURE_DIAGRAMS.md) — 可视化图表
- [项目结构说明](docs/PROJECT_STRUCTURE.md) — 目录布局
- [Profiles 使用指南](docs/PROFILES.md) — 使用与创建 Profile
- [快速参考手册](docs/QUICK_REFERENCE.md) — 命令速查

---

## 贡献

欢迎提交 Issue 或 Pull Request，包括错误修复、新功能、技能或文档改进。

贡献时请遵循：
- PEP 8 代码风格规范
- 为新功能添加测试
- 更新相关文档

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

## 致谢

- [Anthropic](https://www.anthropic.com/) — 原始 Harness 设计理念
- [OpenAI](https://openai.com/) — LLM API
