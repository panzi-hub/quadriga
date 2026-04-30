# Harness Engineering - 快速架构概览 🗺️

> **5分钟理解Harness核心架构**

---

## 🎯 一句话总结

Harness是一个**多Agent协作系统**，通过 **Plan → Contract → Build → Evaluate** 循环，将用户需求自动转化为可运行的代码。

---

## 🏗️ 三层架构

```
┌─────────────────────────────────────┐
│     编排层 (harness.py)              │  ← 总指挥
│   Plan → Contract → Build → Eval    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     Agent层 (agents.py)              │  ← 执行者
│  Planner | Builder | Evaluator      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│     基础设施层                        │  ← 支撑系统
│ Context | Tools | Skills | Profile  │
└─────────────────────────────────────┘
```

---

## 🔄 核心流程

```
用户输入 "Build a calculator"
         ↓
    ┌─────────┐
    │ Planner │ → 生成 spec.md（产品规格）
    └────┬────┘
         ↓
    ┌──────────┐
    │ Contract │ → Builder & Evaluator协商验收标准
    └────┬─────┘
         ↓
    ┌─────────┐
    │ Builder │ → 编写代码 → 测试 → 修复
    └────┬────┘     ↑          ↓
         │      Tools执行   Context管理
         ↓
    ┌───────────┐
    │ Evaluator │ → 评分（Design/Originality/Craft/Functionality）
    └─────┬─────┘
          │
    分数 >= 85? 
     ├─ 是 → ✅ 完成！
     └─ 否 → REFINE（优化）或 PIVOT（重来）
             ↓
          回到 Builder
```

---

## 📦 10大核心组件

| # | 组件 | 文件 | 行数 | 职责 |
|---|------|------|------|------|
| 1 | **Harness** | `harness.py` | 521 | 主编排器，控制整体流程 |
| 2 | **Agent** | `agents.py` | 427 | Agent运行时，while循环+工具调用 |
| 3 | **Context** | `context.py` | 310 | 上下文管理（压缩/重置/焦虑检测） |
| 4 | **Tools** | `tools.py` | 1075 | 工具集（文件/Shell/浏览器/Git） |
| 5 | **Profile** | `profiles/` | ~300 | 场景配置（4种内置） |
| 6 | **Skills** | `skills/` | 37个 | 专业技能库（渐进式披露） |
| 7 | **Prompts** | `prompts.py` | ~300 | 系统提示词 |
| 8 | **Middleware** | `middlewares.py` | ~800 | 中间件（超时/重试/监控） |
| 9 | **Config** | `config.py` | ~80 | 配置管理 |
| 10 | **Logger** | `logger.py` | ~150 | 日志系统 |

---

## 🎭 5种Agent角色

```
┌──────────────┐
│   Planner    │ 🧠 规划师：需求 → 规格文档
└──────────────┘

┌──────────────┐
│   Builder    │ 🔨 工程师：规格 → 代码实现
└──────────────┘

┌──────────────┐
│  Evaluator   │ ✅ 测试员：代码 → 评分+反馈
└──────────────┘

┌──────────────────┐
│ContractProposer  │ 📝 合同提议者：制定验收标准
└──────────────────┘

┌──────────────────┐
│ContractReviewer  │ 🔍 合同审核者：审核验收标准
└──────────────────┘
```

---

## 🛠️ 工具集（Tools）

### 文件操作
- `read_file(path)` - 读取文件
- `write_file(path, content)` - 写入文件
- `edit_file(path, old, new)` - 精确替换

### Shell命令
- `run_bash(command, timeout)` - 执行命令

### 浏览器测试
- `browser_test(url, actions)` - Playwright端到端测试

### Git操作
- `git_commit(message)` - 提交更改
- `git_diff()` - 查看差异

### 技能加载
- `read_skill_file(path)` - 读取技能文档

**安全机制**: 所有路径操作都经过`_resolve()`检查，防止逃逸出workspace

---

## 🎓 技能系统（Skills）

### 工作原理
```
1. Agent分析任务
       ↓
2. 从目录检索相关技能
       ↓
3. 加载SKILL.md到上下文
       ↓
4. 参考技能指导生成代码
       ↓
5. 任务完成后释放技能
```

### 37个技能分类
- **前端开发** (3): frontend-design, filter-js-from-html, ...
- **安全分析** (4): password-recovery, crack-7z-hash, ...
- **多媒体** (3): video-processing, extract-moves-from-video, ...
- **机器学习** (5): torch-pipeline-parallelism, train-fasttext, ...
- **系统运维** (6): qemu-startup, db-wal-recovery, ...
- **算法** (5): write-compressor, chess-best-move, ...
- **其他** (11): ...

### SKILL.md格式
```markdown
---
name: skill-name
description: 一句话描述
category: development
---

# 详细说明
...
```

---

## 🎯 4种Profile（场景配置）

| Profile | 用途 | 特点 |
|---------|------|------|
| **app-builder** | Web应用开发 | 默认模式，注重视觉设计 |
| **terminal** | 终端任务 | 短超时，无浏览器测试 |
| **swe-bench** | GitHub Issue修复 | 代码阅读和Bug修复 |
| **reasoning** | 知识问答 | 技能驱动，无规划阶段 |

### 自定义Profile示例
```python
class MyProfile(BaseProfile):
    @property
    def name(self): return "my-profile"
    
    def builder(self):
        return AgentConfig(
            system_prompt="你是XXX专家...",
            tool_schemas=["read_file", "write_file"],
        )
```

---

## 🧠 上下文管理（Context）

### 三级策略

```
Token < 50K
  ↓
保持现状 ✅

50K < Token < 80K
  ↓
压缩旧消息 📦

Token > 80K 或 检测到焦虑
  ↓
硬重置（Checkpoint + 新白板）🔄
```

### 焦虑检测
```python
anxiety_patterns = [
    "I think this is complete",
    "This should be sufficient",
    "I believe we are done",
]
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| **任务时间** | 15-90分钟 |
| **Token用量** | 300K-4M |
| **成功率** | 70%-95% |
| **成本** | $0.03-$0.80 (gpt-4o) |

### 优化技巧
```bash
# 降低Token消耗
COMPRESS_THRESHOLD=40000

# 提高成功率
HARNESS_MODEL=gpt-4o
PASS_THRESHOLD=90

# 降低成本
HARNESS_MODEL=gpt-4-turbo  # 便宜50%
# 或使用本地模型（免费）
OPENAI_BASE_URL=http://localhost:11434/v1
```

---

## 🔌 支持的LLM后端

### OpenAI
```bash
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
```

### OpenRouter（Claude等）
```bash
OPENAI_BASE_URL=https://openrouter.ai/api/v1
HARNESS_MODEL=anthropic/claude-sonnet-4
```

### Ollama（本地）
```bash
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
```

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
cp .env.template .env
# 编辑.env填入API Key

# 3. 运行
python harness.py "Build a Pomodoro timer"

# 4. 查看结果
ls workspace/latest/
open workspace/latest/index.html
```

---

## 📁 项目结构（简化版）

```
Harness_Engineering/
│
├── harness.py          # 🎯 主编排器
├── agents.py           # 🤖 Agent运行时
├── context.py          # 🧠 上下文管理
├── tools.py            # 🛠️ 工具集
├── prompts.py          # 💬 提示词
├── skills.py           # 🎓 技能注册表
├── config.py           # ⚙️ 配置管理
├── logger.py           # 📝 日志系统
├── middlewares.py      # 🔧 中间件
│
├── profiles/           # 🎭 场景配置
│   ├── base.py
│   ├── app_builder.py
│   ├── terminal.py
│   ├── swe_bench.py
│   └── reasoning.py
│
├── skills/             # 📚 技能库（37个）
│   ├── frontend-design/
│   ├── password-recovery/
│   └── ...
│
└── workspace/          # 📁 输出目录
    └── latest/
        ├── spec.md
        ├── contract.md
        ├── feedback.md
        └── index.html
```

---

## 🎨 设计模式

- **策略模式**: Profile系统
- **观察者模式**: TraceWriter
- **责任链模式**: Middleware
- **工厂模式**: Profile创建
- **单例模式**: LLM客户端

---

## 🔍 调试技巧

### 查看Trace
```bash
tail -f workspace/latest/_trace_builder.jsonl | jq .
```

### 统计调用
```bash
grep '"event":"llm_response"' workspace/latest/_trace_builder.jsonl | wc -l
```

### 查看日志
```bash
tail -f logs/harness.log
```

---

## ❓ 常见问题

**Q: 如何选择Profile？**
- Web应用 → `app-builder`
- 命令行 → `terminal`
- 修Bug → `swe-bench`
- 问答 → `reasoning`

**Q: Token太高？**
- 降低`COMPRESS_THRESHOLD`
- 使用更强模型
- 加载相关技能

**Q: 如何提高成功率？**
- 详细描述需求
- 使用gpt-4o
- 提高`PASS_THRESHOLD`

**Q: 可以并行运行吗？**
```bash
WORKSPACE=./task1 python harness.py "任务1" &
WORKSPACE=./task2 python harness.py "任务2" &
```

---

<div align="center">

**🎉 现在你已经掌握了Harness的核心架构！**

*详细文档: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)*

</div>