# quadriga

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

纯 Python 的多 Agent 长任务框架。一次提示会经过规划、实现、测试和评分，而不是只发给模型一次。模型调用走 OpenAI 兼容接口，不依赖 LangChain、AutoGen 或 CrewAI。

设计来自 Anthropic 的 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)。

[English](README.md)

---

## 简单概览

```
任务
  -> Planner        spec.md
  -> Proposer       contract.md          仅 app-builder
  -> Reviewer       APPROVED / 要求修改   最多 3 轮
  -> Builder        代码 / 补丁 / answer.md
  -> Evaluator      feedback.md
       |  分数达到阈值
       |    完成
       |  分数下降
       |    回滚后重新交给 Builder
       |  其他情况
       +--> 带着 feedback.md 再次交给 Builder
```

Planner、合同协商和 Evaluator 都可能不存在。profile 跳过它们时，任务会直接交给 Builder。

## 调用链

`python harness.py` 会先加载一个 profile，再按该 profile 组装最多五个 Agent，然后跑固定的外层循环。每个 Agent 还有自己的内层工具循环。哪些角色存在、能用哪些工具，都由 profile 决定。

| Profile | 用途 | Planner | 合同协商 | Evaluator | 默认通过线 |
|---|---|---|---|---|---|
| `app-builder` | 从一句话生成 Web 应用 | 开启 | 开启 | 开启，并附带浏览器工具 | 7.0 |
| `terminal` | CLI / Terminal-Bench 风格任务 | 经常跳过 | 关闭 | 开启 | 8.0，最多 2 轮 |
| `swe-bench` | 诊断并修复仓库中的问题 | 开启 | 关闭 | 开启 | 7.0 |
| `reasoning` | 知识问答和计算题 | 开启 | 关闭 | 开启 | 7.0 |

只有 `app-builder` 启用合同协商。其他 profile 继承 `BaseProfile` 中默认关闭的合同 Agent。

---

## 调用链

```
python harness.py [--profile NAME] "任务"
        │
        ▼
main()                                          harness.py
  ├─ 解析 --profile / --list-profiles / --verbose
  ├─ get_profile(name)                          profiles/__init__.py
  ├─ 创建 workspace/{timestamp}_{slug}/
  ├─ git init
  ├─ API 预检（benchmark 模式跳过）
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
  │    planner.run("写入 spec.md")              planner 启用时
  │    否则把原始提示直接写入 spec.md
  │
  └─ 2. for round in 1..max_rounds
       ├─ CONTRACT                              仅 app-builder
       │    proposer.run  -> contract.md
       │    reviewer.run  -> APPROVED 或要求修改
       │    最多重复 3 次
       ├─ git tag round-N-start
       ├─ BUILD
       │    profile.format_build_task(...)
       │    builder.run(task)                   读取 spec/feedback/contract
       ├─ git tag round-N-end
       └─ EVALUATE                              evaluator 启用时
            evaluator.run("写入 feedback.md")
            profile.extract_score(feedback.md)
            score >= 阈值 -> 结束
            score 下降    -> git reset --hard round-(N-1)-end
```

外层轮数先看 profile，profile 没有覆盖时用 `MAX_HARNESS_ROUNDS`（默认 5）。通过分默认是 `PASS_THRESHOLD=7.0`。profile 也可以在 `resolve_time_allocation()` 里直接关掉 planner 或 evaluator。

### 每个 Agent 负责什么

| Agent | 产物 | 结束条件 |
|---|---|---|
| Planner | `spec.md` | 不再调用工具 |
| Contract proposer | `contract.md` | Reviewer 写入 `APPROVED`，或评审达到 3 次 |
| Contract reviewer | 修订后的 `contract.md` | 同上 |
| Builder | 应用文件、补丁，或 `answer.md` | 工具循环结束，或中间件硬停止 |
| Evaluator | 带 `Average: X/10` 的 `feedback.md` | 工具循环结束 |

`format_build_task()` 会把原始任务、上一轮 `feedback.md` 和分数历史送回下一轮 Builder。这是 refine。若新分数低于上一轮，`Harness.run` 会回滚到上一轮的 git tag。这是 pivot。

### 一次 `Agent.run` 的内部调用

所有角色共用这个循环。profile 只更换提示词、工具 schema、中间件和时间预算。

```
Agent.run(task)                                 agents.py
  messages = [系统提示 + skill 目录, 用户任务]
  trace = workspace/_trace_{role}.jsonl

  for iteration in 1..MAX_AGENT_ITERATIONS:     默认 500
    ├─ middleware.stop_reason()                 硬停止，不再请求模型
    ├─ middleware.per_iteration()               可注入一条 user 消息
    ├─ count_tokens(messages)                   context.py
    │    超过 RESET_THRESHOLD 或出现焦虑信号 -> checkpoint 后重置
    │    超过 COMPRESS_THRESHOLD              -> compact_messages()
    ├─ chat.completions.create(                 OpenAI 兼容接口
    │       model, messages, tools, tool_choice=auto)
    ├─ 没有 tool_calls？
    │    middleware.pre_exit() 可以强制再跑一轮
    │    否则返回助手文本
    └─ 每个 tool_call:
         execute_tool(name, args)               tools.py
           校验并修正参数 -> TOOL_DISPATCH -> 结果后处理
         追加 tool result
         middleware.post_tool()                 可注入纠偏提示
```

技能不是由 harness 预先选中的。系统提示里只有名称和简介。Agent 认为相关时，自己用 `read_skill_file` 读取 `skills/<name>/SKILL.md`。

### 工具和中间件

```
模型 tool_call
  -> tools.execute_tool
       -> _validate_and_fix
       -> read_file | write_file | edit_file | list_files
          run_bash | delegate_task | read_skill_file
          web_search | web_fetch
          browser_test | stop_dev_server          仅 evaluator
       -> 空结果标记 / 大输出落盘
  -> AgentMiddleware.post_tool / pre_exit / stop_reason
       LoopDetection | TimeBudget | PreExitVerification
       TaskTracking | SkeletonDetection | ErrorGuidance
```

文件工具限制在工作区内。`delegate_task` 会发起一次嵌套模型调用，避免长时间探索撑满父上下文。浏览器工具只由 `AppBuilderProfile.evaluator()` 挂上。

### 循环留下的文件

```
workspace/{timestamp}_{slug}/
├── spec.md                  planner 产物，或原始提示
├── contract.md              app-builder 的本轮验收合同
├── feedback.md              evaluator 的分数和意见
├── progress.md              Agent 可选的进度记录
├── _trace_{role}.jsonl      每个角色一份 trace
└── .git                     round-N-start / round-N-end 标签
```

`HARNESS_FLAT_WORKSPACE=1` 时不创建时间戳目录，也不做 API 预检。benchmark 运行器使用这个模式。

---

## 快速开始

```bash
git clone https://github.com/panzi-hub/quadriga.git
cd quadriga
pip install -r requirements.txt
python -m playwright install chromium   # 只有 app-builder 的浏览器评估需要

cp .env.template .env
```

```bash
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

```bash
python harness.py "做一个支持拖拽和本地存储的交互式看板"
python harness.py --profile terminal "找出并修复 /tmp 中的失效符号链接"
python harness.py --profile swe-bench "修复 parse_config() 中的 TypeError"
python harness.py --profile reasoning "火星的逃逸速度是多少？"
python harness.py --list-profiles
```

---

## 配置

| 变量 | 默认值 | 作用位置 |
|---|---|---|
| `OPENAI_API_KEY` | — | `agents.get_client()` |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API 客户端 |
| `HARNESS_MODEL` | `gpt-4o` | 每一次模型调用 |
| `HARNESS_WORKSPACE` | `./workspace` | 项目输出目录 |
| `MAX_HARNESS_ROUNDS` | `5` | profile 未覆盖时的外层轮数 |
| `PASS_THRESHOLD` | `7.0` | 兜底通过分 |
| `COMPRESS_THRESHOLD` | `50000` | 内层循环压缩阈值 |
| `RESET_THRESHOLD` | `100000` | 内层循环 checkpoint 重置阈值 |
| `MAX_AGENT_ITERATIONS` | `500` | 内层循环上限 |
| `MAX_TOOL_ERRORS` | `5` | 连续 API 错误后中止 |
| `TASK_BUDGET_SECONDS` | 未设置 | 全局覆盖所有 profile 的时间预算 |
| `ENABLE_PARALLEL_TOOL_CALLS` | `0` | 默认关闭，除非模型能稳定处理并行工具调用 |

profile 参数也可以不改代码直接覆盖，例如 `PROFILE_TERMINAL_PASS_THRESHOLD=9` 或 `PROFILE_TERMINAL_TASK_BUDGET=1800`。

OpenRouter 和本地 OpenAI 兼容服务只需要改 `OPENAI_BASE_URL` 与 `HARNESS_MODEL`。

---

## 仓库地图

| 路径 | 在调用链中的位置 |
|---|---|
| `harness.py` | CLI、外层循环、合同循环、git tag、分数决策 |
| `agents.py` | 内层模型/工具循环和 JSONL trace |
| `profiles/` | 一个场景使用哪些 Agent、工具、提示词、预算和评分 |
| `prompts.py` | app-builder 路径的角色提示词 |
| `tools.py` | 工具 schema 和 `execute_tool` 分发 |
| `middlewares.py` | 停止条件与纠偏注入 |
| `context.py` | token 计数、压缩、焦虑检测、checkpoint |
| `skills.py`, `skills/` | 技能目录和 36 个按需加载的领域技能 |
| `config.py` | 环境变量和循环阈值 |
| `benchmarks/` | Terminal-Bench 任务元数据和运行胶水 |
| `tests/` | 配置契约、沙箱路径和 API 检查 |

更多细节见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)、[docs/PROFILES.md](docs/PROFILES.md)、[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)。

---

## 许可证

MIT。见 [LICENSE](LICENSE)。
