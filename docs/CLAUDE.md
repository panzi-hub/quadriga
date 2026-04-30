# Harness Engineering

多智能体自主开发框架。基于 Anthropic 的 "Harness design for long-running application development" 文章的教育性复现。

## 项目是什么

给定一个一句话任务，Harness 能自主完成：规划产品 → 协商验收标准 → 编写代码 → 浏览器测试 → 评分 → 根据反馈迭代——全程无需人工干预。

## 核心架构

```
Harness (编排层)
    ├── Planner     → 生成 spec.md
    ├── Builder     → 执行任务，写代码
    ├── Evaluator   → 浏览器测试，评分
    └── Contract Negotiation → 合同协商
```

**关键设计原则：**
- Profile 驱动：通用编排 + 场景适配
- 上下文焦虑通过重置解决，不是压缩
- 中间件是主要行为塑形工具（6 个可组合）
- Skills 渐进式 Disclosure

## 文件结构

```
├── harness.py          # 入口 + 编排循环
├── agents.py           # Agent 执行循环 + TraceWriter
├── context.py          # 上下文生命周期（压缩/重置）
├── tools.py            # 工具实现 + browser_test
├── prompts.py          # 系统提示词
├── middlewares.py      # 6 个中间件
├── skills.py           # Skill 注册
├── config.py           # 配置加载
├── logger.py           # 日志
├── profiles/           # Profile 适配层
│   ├── base.py
│   ├── app_builder.py  # Web 应用构建
│   └── terminal.py    # CLI 任务 (TB2)
├── benchmarks/
└── skills/             # Skill 指南
```

## 快速开始

```bash
# 1. 复制环境配置
cp .env.example .env
# 编辑 .env，填入你的 API key

# 2. 运行任务
python harness.py "Build a todo app"
python harness.py --profile terminal "Fix the broken symlinks"

# 3. 查看 Profile 列表
python harness.py --list-profiles
```

## 环境变量

```bash
OPENAI_API_KEY=sk-xxxxx           # 必需
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
HARNESS_WORKSPACE=./workspace

# 上下文阈值
COMPRESS_THRESHOLD=50000          # 触发压缩
RESET_THRESHOLD=100000            # 触发重置

# Harness 配置
MAX_HARNESS_ROUNDS=5
PASS_THRESHOLD=7.0
MAX_AGENT_ITERATIONS=500
```

## Profile 说明

| Profile | 用途 |
|---------|------|
| app-builder | Web 应用构建（含浏览器测试） |
| terminal | CLI 任务（Terminal-Bench 2.0） |

## 核心概念

### 中间件（6 个）
- LoopDetection — 检测重复模式，防止死循环
- PreExitVerification — 退出前强制验证
- TimeBudget — 时间预算警告
- TaskTracking — 强制任务分解到 _todo.md
- SkeletonDetection — 防止忽略 TODO 文件
- ErrorGuidance — 错误恢复指导

### 上下文生命周期
- tokens > 50k → 压缩（保留比例：evaluator 50%, builder 15%）
- tokens > 100k 或焦虑检测 → 重置（写 checkpoint 到 progress.md）

### Skills 渐进式 Disclosure
- Level 1：启动时扫描，注入 name + description
- Level 2：Agent 自己决定读取 SKILL.md
- Level 3：按需读取子文件

## 输出文件

| 文件 | 用途 |
|------|------|
| spec.md | 产品规格说明书 |
| contract.md | Sprint 合同 |
| feedback.md | QA 评估反馈 |
| progress.md | 上下文重置时的 checkpoint |
| _todo.md | 任务追踪清单 |
| _trace_*.jsonl | 调试用的决策记录 |

## 扩展项目

添加新 Profile：在 `profiles/` 创建类，继承 `BaseProfile`
添加新中间件：继承 `AgentMiddleware`，实现 `per_iteration/post_tool/pre_exit`
添加新工具：在 `tools.py` 实现函数 + 添加 schema

## 相关文档

- `HARNESS_REWRITE_GUIDE.md` — 从零重写的完整指南
- `HARNESS_ARCHITECTURE.md` — 架构图 + 中文提示词