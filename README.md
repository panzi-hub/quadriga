# Harness — 多 Agent 自主开发架构

[English](README_EN.md) | 中文

> 基于 Anthropic 文章 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 的完整实现。
> 
> 纯 Python 构建，支持任何 OpenAI 兼容的 API 端点，不依赖任何 Agent SDK。

## 🚀 项目简介

Harness 是一个强大的多 Agent 自主开发框架，能够根据一句话需求，全流程自动化完成：

1. **产品规划**：将简短需求扩展为详细产品规格
2. **验收标准协商**：Builder 和 Evaluator 协商明确的完成标准
3. **代码实现**：自动生成、测试和调试代码
4. **质量评估**：基于多维度标准进行打分
5. **迭代优化**：根据反馈自动调整和改进

## 🎯 核心特性

### 1. 多 Profile 支持
- **app-builder**：从提示构建 Web 应用（Anthropic 文章原始场景）
- **terminal**：解决终端/CLI 任务（Terminal-Bench-2 风格）
- **swe-bench**：修复真实仓库中的 GitHub 问题
- **reasoning**：知识密集型 QA（MMMU-Pro 风格）

### 2. 三 Agent 协作系统
- **Planner**：将 1-4 句话的需求扩展为详细产品规格
- **Builder**：根据规格实现代码，处理反馈进行迭代
- **Evaluator**：测试应用并基于多维度标准打分

### 3. 智能上下文管理
- **上下文焦虑检测**：识别模型"提前收工"的信号
- **自动压缩**：当上下文过大时智能摘要旧消息
- **硬重置**：当模型性能下降时创建新的上下文白板
- **角色差异化策略**：为不同 Agent 定制上下文管理方案

### 4. 策略决策机制
- **REFINE vs PIVOT**：根据分数趋势自动决定是优化现有方案还是推倒重来
- **Sprint Contract**：每轮迭代前协商明确的验收标准
- **Sub-Agent 隔离**：父 Agent 可委派子 Agent 执行特定任务，保持上下文干净

### 5. 技能系统
- **渐进式披露**：Agent 根据需要自主加载相关技能
- **丰富的技能库**：包含前端设计、密码恢复、视频处理等多种专业技能
- **可扩展架构**：轻松添加自定义技能

### 6. 多模型支持
- **OpenAI**：支持 GPT-4o 等模型
- **OpenRouter**：支持 Claude 等第三方模型
- **Ollama**：支持本地部署的模型

## 📦 项目结构

```
├── harness.py        # 主入口，编排 Plan → Contract → Build → Evaluate 流程
├── agents.py         # 核心 Agent 实现，包含 while 循环和工具执行
├── context.py        # 上下文管理，包含压缩、焦虑检测和重置
├── tools.py          # 工具实现，如文件操作、浏览器测试等
├── prompts.py        # 所有 Agent 的系统提示和评估标准
├── skills.py         # 技能注册表和管理
├── skills/           # 技能库，包含各种专业技能
├── profiles/         # 不同场景的配置文件
│   ├── app_builder.py    # Web 应用构建配置
│   ├── terminal.py       # 终端任务配置
│   ├── swe_bench.py       # GitHub 问题修复配置
│   └── reasoning.py       # 知识密集型 QA 配置
├── config.py         # 配置管理，自动加载环境变量
├── .env.template     # 环境变量模板
├── requirements.txt  # Python 依赖
└── workspace/        # 生成的项目输出目录
```

## 🔧 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt

# 可选：安装 Playwright 用于浏览器测试
python -m playwright install chromium
```

### 2. 配置环境

```bash
cp .env.template .env
# 编辑 .env 文件，填入你的 API key
```

### 3. 运行示例

```bash
# 构建一个简单的 Pomodoro 计时器
python harness.py "Build a Pomodoro timer with start, pause, reset buttons. Single HTML file."

# 构建一个交互式元素周期表
python harness.py "Build an interactive periodic table of elements with search, category filters, and element detail popups"

# 构建一个完整的浏览器 DAW
python harness.py "Build a fully featured DAW in the browser using the Web Audio API"

# 使用 terminal profile 解决终端任务
python harness.py --profile terminal "Fix the broken symlinks in /tmp"

# 使用 swe-bench profile 修复 GitHub 问题
python harness.py --profile swe-bench "Fix the TypeError in parse_config()"

# 使用 reasoning profile 回答知识密集型问题
python harness.py --profile reasoning "What is the escape velocity of Mars?"
```

## 📊 评估标准

Evaluator 使用以下维度评估生成的应用：

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| **Design Quality** | HIGH | 视觉设计是否有统一身份感，界面是否美观专业 |
| **Originality** | HIGH | 是否有自定义设计决策，避免 AI 默认审美 |
| **Craft** | MEDIUM | 技术执行质量，如排版、间距、色彩和谐度 |
| **Functionality** | HIGH | 功能是否完整可用，所有交互是否正常 |

## 🎨 技能系统

Harness 包含丰富的技能库，Agent 可以根据任务需求自主选择加载：

- **frontend-design**：创建专业级前端界面
- **password-recovery**：密码恢复和安全分析
- **video-processing**：视频处理和分析
- **torch-pipeline-parallelism**：PyTorch 管道并行化
- **write-compressor**：数据压缩算法实现
- **...**：更多技能持续添加中

## 🔍 技术实现

### 核心 Agent 循环

```python
# agents.py — Agent.run() 方法
for iteration in range(1, MAX_AGENT_ITERATIONS + 1):
    # 1. 上下文生命周期检查（压缩或重置）
    # 2. 调用 LLM 获取响应
    # 3. 执行工具调用
    # 4. 将结果追加到上下文
    # 5. 如果没有更多工具调用 → 结束
```

### 上下文管理策略

```python
# context.py — 生命周期检查
if token_count > RESET_THRESHOLD or detect_anxiety(messages):
    # 写 checkpoint，创建新的上下文白板
    checkpoint = create_checkpoint(messages, llm_call)
    messages = restore_from_checkpoint(checkpoint, prompt)
elif token_count > COMPRESS_THRESHOLD:
    # 摘要压缩旧消息
    messages = compact_messages(messages, llm_call, role)
```

## 🌐 多模型配置

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

### Ollama（本地）
```bash
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
```

## 📈 性能指标

- **平均任务完成时间**：30-60 分钟（取决于复杂度）
- **Token 用量**：1-3M per task
- **成本**：$0.10-$0.50 per task（使用 gpt-4o）

## 🎯 适用场景

- **快速原型开发**：根据一句话需求快速生成可用原型
- **教育学习**：了解多 Agent 系统的设计和实现
- **研究实验**：探索 LLM 在自主开发中的能力边界
- **辅助开发**：作为开发者的智能助手，自动完成重复性任务
- **问题修复**：自动分析和修复代码库中的问题
- **知识问答**：回答复杂的知识密集型问题

## 🚀 扩展指南

### 添加自定义技能

1. 在 `skills/` 目录下创建新目录
2. 创建 `SKILL.md` 文件，包含 YAML frontmatter：

```markdown
---
name: my-new-skill
description: 一句话描述技能功能
---

详细技能说明...
```

### 添加自定义 Profile

1. 在 `profiles/` 目录下创建新的 Python 文件
2. 继承 `BaseProfile` 类并实现必要的方法
3. 在 `profiles/__init__.py` 中注册新的 profile

### 调整系统提示

修改 `prompts.py` 中的系统提示，根据需要定制 Agent 行为。

### 配置调优

在 `.env` 文件中调整以下参数：
- `MAX_HARNESS_ROUNDS`：最大迭代轮数
- `PASS_THRESHOLD`：通过分数阈值
- `COMPRESS_THRESHOLD`：上下文压缩阈值
- `RESET_THRESHOLD`：上下文重置阈值

## 📚 参考资料

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request，帮助改进 Harness！

## 📄 许可证

MIT License

---

**Harness** — 让 AI 自主开发变得简单而强大！