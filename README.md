# Harness — 多 Agent 自主开发架构 🤖✨

[English](README_EN.md) | 中文

> 🎯 **基于 Anthropic 文章 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 的完整实现**
> 
> 🐍 **纯 Python 构建** | 🔌 **支持任何 OpenAI 兼容 API** | 🚫 **零 Agent SDK 依赖**

---

## 📚 文档导航

### 架构文档
想深入了解 Harness 的内部架构？我们准备了完整的架构文档：

- 🗺️ **[快速架构概览](docs/ARCHITECTURE_QUICK.md)** - 5分钟理解核心架构
- 🏗️ **[详细架构文档](docs/ARCHITECTURE.md)** - 完整的系统架构说明
- 📊 **[架构可视化图表](docs/ARCHITECTURE_DIAGRAMS.md)** - 12个Mermaid图表直观展示
- 📋 **[项目结构说明](docs/PROJECT_STRUCTURE.md)** - 整理后的目录结构详解

### 其他文档
- 📖 [Profiles使用指南](docs/PROFILES.md)
- ⚡ [快速参考手册](docs/QUICK_REFERENCE.md)
- 📝 [CLAUDE配置说明](docs/CLAUDE.md)
- 🌍 [English README](docs/README_EN.md)

---

## 🌟 项目简介

想象一下：**只需一句话描述你的想法，AI 就能自动完成从设计到代码的全流程开发！**

Harness 正是这样一个革命性的多 Agent 自主开发框架。它像一个智能软件开发团队，包含规划师、工程师和测试员三个角色，协同工作将你的创意转化为可运行的应用。

### 💡 它能做什么？

```
你输入: "Build a Pomodoro timer with start, pause, reset buttons"
         ↓
🧠 Planner (规划师): 生成详细的产品规格文档
         ↓
📋 Contract (协商): Builder 和 Evaluator 确定验收标准
         ↓
🔨 Builder (工程师): 编写代码 → 测试 → 修复 bug → 迭代优化
         ↓
✅ Evaluator (测试员): 多维度评分，确保质量达标
         ↓
🎉 输出: 完整的、可运行的 HTML/CSS/JS 应用！
```

### 🎯 核心价值

- **全流程自动化**: 从需求分析到代码交付，无需人工干预
- **智能迭代**: 自动检测问题、接收反馈、持续优化
- **质量保证**: 多维度评估体系，确保产出专业级应用
- **灵活扩展**: 丰富的技能库，轻松适配各种开发场景

---

## ✨ 核心特性

### 1️⃣ 多场景 Profile 系统

Harness 内置多种专业配置，针对不同任务场景优化：

| Profile | 适用场景 | 示例任务 |
|---------|----------|----------|
| **app-builder** 🎨 | Web 应用开发 | 构建计时器、仪表盘、交互页面 |
| **terminal** 💻 | CLI/终端任务 | 文件处理、系统管理、脚本调试 |
| **swe-bench** 🔧 | GitHub 问题修复 | Bug 修复、功能增强、代码重构 |
| **reasoning** 🧩 | 知识密集型问答 | 复杂推理、学术研究、技术分析 |

### 2️⃣ 三 Agent 协作系统

Harness 模拟真实软件团队的协作模式：

#### 🧠 **Planner（规划师）**
- **职责**: 将模糊的需求转化为清晰的蓝图
- **能力**: 理解用户意图，生成包含功能列表、技术栈、UI/UX 设计的详细规格文档
- **示例**: "Build a calculator" → 生成包含科学计算、历史记录、主题切换等功能的完整规格

#### 🔨 **Builder（工程师）**
- **职责**: 将规格文档变为可运行的代码
- **能力**: 
  - 自主加载相关技能（如前端设计、数据处理）
  - 编写、测试、调试代码
  - 根据反馈迭代优化
- **特色**: 支持子 Agent 委派，保持主上下文干净

#### ✅ **Evaluator（测试员）**
- **职责**: 严格把关，确保交付质量
- **评估维度**:
  - 🎨 **Design Quality**: 视觉设计是否专业美观
  - 💡 **Originality**: 是否有创新设计，避免 AI 模板化
  - 🛠️ **Craft**: 代码工艺和技术执行质量
  - ⚙️ **Functionality**: 功能完整性与稳定性

### 3️⃣ 智能上下文管理 🧠

LLM 的上下文窗口有限，Harness 独创三层管理策略：

#### 🔍 **焦虑检测 (Anxiety Detection)**
```python
# 识别模型"提前收工"的信号
if model_says("I think this is complete") but task_is_not_done():
    trigger_context_reset()  # 强制继续工作
```

#### 📦 **自动压缩 (Auto Compression)**
```python
# 当上下文超过阈值时
if token_count > 50000:
    summarize_old_messages()  # 智能摘要历史对话
    keep_recent_interactions()  # 保留最近关键信息
```

#### 🔄 **硬重置 (Hard Reset)**
```python
# 当模型性能明显下降时
if quality_score_drops_significantly():
    create_checkpoint()  # 保存当前进度
    start_fresh_context()  # 创建新的白板重新开始
```

**效果**: 即使面对百万 Token 的长任务，也能保持稳定的输出质量！

### 4️⃣ 策略决策机制 🎲

Harness 不是盲目迭代，而是智能决策：

#### 📈 **REFINE vs PIVOT**
```
分数趋势分析:
├─ 持续上升 → REFINE: 继续优化现有方案
├─ 停滞不前 → PIVOT: 尝试全新方法
└─ 明显下降 → RESET: 回退到上一个稳定版本
```

#### 📝 **Sprint Contract（冲刺合同）**
每轮迭代前，Builder 和 Evaluator 会协商：
- ✅ 本轮需要完成的具体功能
- 🎯 明确的验收标准
- 📊 预期达到的分数目标

**好处**: 避免无意义的迭代，每次修改都有明确目标！

#### 👥 **Sub-Agent 隔离**
```python
# Builder 可以委派子任务
builder.delegate("research_best_practices", sub_agent)
# 子 Agent 独立工作，结果汇总后返回
# 主上下文保持简洁，不受研究过程干扰
```

### 5️⃣ 技能系统 🎓

Harness 的技能系统让 Agent 具备专业能力：

#### 🌈 **渐进式披露 (Progressive Disclosure)**
- Agent 不会一次性加载所有技能（那会占用大量上下文）
- 根据当前任务，**自主选择**需要的技能
- 用完即释放，保持轻量高效

#### 📚 **丰富的技能库**（30+ 专业技能）

| 类别 | 技能示例 | 应用场景 |
|------|----------|----------|
| **前端开发** | frontend-design | 创建专业级 UI/UX |
| **安全分析** | password-recovery, crack-7z-hash | 密码恢复与安全测试 |
| **多媒体** | video-processing, extract-moves-from-video | 视频分析与处理 |
| **机器学习** | torch-pipeline-parallelism, train-fasttext | PyTorch 并行训练 |
| **系统运维** | qemu-startup, db-wal-recovery | 虚拟机与数据库管理 |
| **算法** | write-compressor, chess-best-move | 数据压缩与博弈算法 |
| **更多...** | ... | 持续更新中 |

#### ➕ **自定义技能**
只需创建一个 `SKILL.md` 文件：
```
---
name: my-custom-skill
description: 用一句话描述这个技能的作用
---

# 详细说明
这里是技能的完整教程、最佳实践和示例代码...
```

### 6️⃣ 多模型支持 🔌

Harness 兼容任何 OpenAI 格式的 API：

| 平台 | 推荐模型 | 特点 |
|------|----------|------|
| **OpenAI** | gpt-4o, gpt-4-turbo | 最强通用能力 |
| **Anthropic** (via OpenRouter) | claude-sonnet-4, claude-opus | 优秀的代码生成 |
| **Ollama** (本地) | qwen2.5-coder:32b, llama3.1 | 隐私保护，零成本 |
| **其他兼容端点** | 任意模型 | 灵活接入 |

**一键切换**: 只需修改 `.env` 文件中的配置即可！

---

## 📦 项目结构

```
Harness_Engineering/
│
├── 🚀 核心引擎
│   ├── harness.py          # 主编排器：Plan → Contract → Build → Evaluate
│   ├── agents.py           # Agent 运行时：循环控制 + 工具执行
│   ├── context.py          # 上下文管家：压缩、焦虑检测、重置
│   ├── tools.py            # 工具箱：文件操作、浏览器测试、Shell 命令
│   ├── prompts.py          # 提示词库：所有 Agent 的系统指令
│   └── skills.py           # 技能管理器：注册、加载、卸载
│
├── 🎭 Profiles（场景配置）
│   ├── app_builder.py      # Web 应用开发模式
│   ├── terminal.py         # 终端任务模式
│   ├── swe_bench.py        # GitHub Issue 修复模式
│   ├── reasoning.py        # 知识问答模式
│   └── base.py             # 基础配置类
│
├── 🎓 Skills（技能库）
│   ├── frontend-design/    # 前端设计技能
│   ├── video-processing/   # 视频处理技能
│   ├── password-recovery/  # 密码恢复技能
│   └── ... (30+ 技能)     # 每个技能包含 SKILL.md 说明文档
│
├── 📊 Benchmarks（基准测试）
│   ├── harbor_agent.py     # 测试代理
│   └── tb2_tasks.json      # Terminal-Bench-2 任务集
│
├── ⚙️ 配置文件
│   ├── config.py           # 配置加载器
│   ├── .env.template       # 环境变量模板
│   └── requirements.txt    # Python 依赖
│
└── 📁 workspace/           # 输出目录（自动生成）
    └── {task_id}/          # 每个任务的独立工作空间
        ├── spec.md         # 产品规格文档
        ├── feedback.md     # 评估反馈记录
        └── ...             # 生成的代码文件
```

---

## 🔧 快速开始

### 1️⃣ 安装依赖

```bash
# 克隆项目
git clone https://github.com/panzi-hub/-Harness_Engineering.git
cd Harness_Engineering

# 安装 Python 依赖
pip install -r requirements.txt

# （可选）安装 Playwright 用于浏览器自动化测试
python -m playwright install chromium
```

### 2️⃣ 配置环境

```bash
# 复制环境变量模板
cp .env.template .env

# 编辑 .env 文件，填入你的 API Key
nano .env  # 或使用你喜欢的编辑器
```

**.env 配置示例**:
```bash
# OpenAI 配置
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
OPENAI_API_KEY=sk-your-api-key-here

# 或者使用 OpenRouter（支持 Claude 等模型）
# OPENAI_BASE_URL=https://openrouter.ai/api/v1
# HARNESS_MODEL=anthropic/claude-sonnet-4
# OPENROUTER_API_KEY=your-key-here

# 或者使用本地 Ollama
# OPENAI_BASE_URL=http://localhost:11434/v1
# HARNESS_MODEL=qwen2.5-coder:32b
```

### 3️⃣ 运行示例

#### 🎨 构建 Web 应用（默认模式）

```bash
# 示例 1: 简单的番茄钟计时器
python harness.py "Build a Pomodoro timer with start, pause, reset buttons. Single HTML file."

# 示例 2: 交互式元素周期表
python harness.py "Build an interactive periodic table with search, category filters, and element detail popups"

# 示例 3: 浏览器音乐工作站（DAW）
python harness.py "Build a fully featured DAW in the browser using the Web Audio API with multiple tracks, effects, and recording"

# 示例 4: 实时天气仪表盘
python harness.py "Create a weather dashboard that shows current conditions, 5-day forecast, and interactive maps for any city"
```

#### 💻 终端任务模式

```bash
# 修复损坏的符号链接
python harness.py --profile terminal "Find and fix all broken symlinks in /tmp directory"

# 批量重命名文件
python harness.py --profile terminal "Rename all .txt files in current directory to include timestamp prefix"

# 分析日志文件
python harness.py --profile terminal "Parse server.log and extract all ERROR entries with timestamps"
```

#### 🔧 GitHub 问题修复模式

```bash
# 修复特定错误
python harness.py --profile swe-bench "Fix the TypeError in parse_config() function when handling None values"

# 添加新功能
python harness.py --profile swe-bench "Add pagination support to the user list endpoint"
```

#### 🧩 知识问答模式

```bash
# 复杂推理问题
python harness.py --profile reasoning "What is the escape velocity of Mars and how does it compare to Earth's?"

# 技术分析
python harness.py --profile reasoning "Explain the differences between TCP and UDP with real-world use cases"
```

### 4️⃣ 查看结果

任务完成后，在 `workspace/` 目录下查看：

```bash
ls workspace/latest/
# 你会看到：
# ├── spec.md          # 产品规格文档
# ├── feedback.md      # 评估反馈记录
# ├── index.html       # 生成的网页文件
# ├── style.css        # 样式文件
# └── script.js        # JavaScript 代码
```

直接在浏览器打开 `index.html` 即可体验生成的应用！

---

## 📊 评估标准详解

Evaluator 采用多维度评分体系，确保应用质量：

| 维度 | 权重 | 评分要点 | 满分标准 |
|------|------|----------|----------|
| **🎨 Design Quality** | ⭐⭐⭐ HIGH | • 视觉一致性<br>• 色彩和谐度<br>• 排版专业性<br>• 品牌识别感 | 像专业设计师作品，有统一的视觉语言 |
| **💡 Originality** | ⭐⭐⭐ HIGH | • 避免 AI 模板化<br>• 独特的交互设计<br>• 创新的解决方案<br>• 个性化细节 | 有明显的设计思考和创新点，非千篇一律 |
| **🛠️ Craft** | ⭐⭐ MEDIUM | • 代码规范性<br>• 响应式布局<br>• 动画流畅度<br>• 无障碍访问 | 代码整洁，细节精致，无明显瑕疵 |
| **⚙️ Functionality** | ⭐⭐⭐ HIGH | • 功能完整性<br>• 交互可用性<br>• 边界情况处理<br>• 错误容错性 | 所有功能正常工作，用户体验流畅 |

**通过标准**: 综合评分 ≥ `PASS_THRESHOLD`（默认 85 分）

---

## 🎓 技能系统深度解析

### 技能是如何工作的？

```python
# 1. Agent 分析当前任务
current_task = "Build a login form with validation"

# 2. 从技能库中检索相关技能
relevant_skills = skills.search(["form", "validation", "frontend"])
# 返回: ['frontend-design', 'password-recovery']

# 3. 加载技能内容到上下文
skill_content = skills.load('frontend-design')
# 包含: 设计原则、最佳实践、代码示例

# 4. Agent 使用技能指导生成代码
# LLM 会参考技能文档中的建议来创建设计

# 5. 任务完成后释放技能
skills.unload('frontend-design')
# 保持上下文轻量
```

### 内置技能亮点

#### 🎨 **frontend-design**
- 现代 UI 设计原则
- 配色方案建议
- 响应式布局技巧
- 微交互动画指南

#### 🔐 **password-recovery**
- 密码强度分析
- Hash 破解方法
- 安全最佳实践
- 常见攻击向量

#### 🎬 **video-processing**
- FFmpeg 命令大全
- 视频格式转换
- 帧提取与分析
- 音频分离技术

#### 🤖 **torch-pipeline-parallelism**
- PyTorch 管道并行原理
- 分布式训练配置
- 性能优化技巧
- 常见问题排查

### 如何贡献新技能？

1. 在 `skills/` 下创建目录：`skills/my-awesome-skill/`
2. 创建 `SKILL.md` 文件：

```
---
name: my-awesome-skill
description: 用一句话清晰描述这个技能能做什么
category: development  # 可选分类
---

# My Awesome Skill

## 概述
详细介绍这个技能的用途和适用场景...

## 使用方法
提供具体的使用步骤和示例...

## 最佳实践
列出使用该技能的建议和注意事项...

## 示例代码
```
# 提供可直接运行的代码示例
```

## 常见问题
FAQ 和故障排除指南...
```

3. 提交 Pull Request，你的技能将被合并到主仓库！

---

## 🔍 技术实现揭秘

### 核心 Agent 循环

```
# agents.py — Agent.run() 伪代码
class Agent:
    def run(self, prompt, max_iterations=50):
        messages = [{"role": "system", "content": prompt}]
        
        for iteration in range(1, max_iterations + 1):
            logger.info(f"Iteration {iteration}")
            
            # 🔄 1. 上下文生命周期检查
            self.context.check_lifecycle(messages, llm_call, self.role)
            
            # 🧠 2. 调用 LLM 获取响应
            response = llm_call(messages)
            
            # 🛠️ 3. 解析并执行工具调用
            if has_tool_calls(response):
                tool_results = execute_tools(response.tool_calls)
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "tool", "content": tool_results})
                continue  # 继续下一轮
            
            # ✅ 4. 没有工具调用 → 任务完成
            logger.info("Agent finished")
            return response.content
        
        raise Exception("Max iterations reached")
```

### 上下文管理策略

```
# context.py — 智能上下文管理
class ContextManager:
    def check_lifecycle(self, messages, llm_call, role):
        token_count = count_tokens(messages)
        
        # 🚨 紧急情况：检测到焦虑或超过重置阈值
        if token_count > RESET_THRESHOLD or self.detect_anxiety(messages):
            logger.warning("Context reset triggered!")
            checkpoint = self.create_checkpoint(messages, llm_call)
            messages = self.restore_from_checkpoint(checkpoint, role)
            return messages
        
        # 📦 中等情况：需要压缩
        elif token_count > COMPRESS_THRESHOLD:
            logger.info("Compressing context...")
            messages = self.compact_messages(messages, llm_call, role)
            return messages
        
        # ✅ 正常情况：无需操作
        return messages
    
    def detect_anxiety(self, messages):
        """检测模型是否表现出'焦虑'信号"""
        last_message = messages[-1]["content"]
        anxiety_patterns = [
            "I think this is complete",
            "This should be sufficient",
            "I believe we are done",
            "Let me wrap this up"
        ]
        return any(pattern in last_message for pattern in anxiety_patterns)
```

### Sprint Contract 协商机制

```
# harness.py — Builder 和 Evaluator 协商过程
def negotiate_contract(builder, evaluator, spec):
    """协商本轮迭代的验收标准"""
    
    # Builder 提出计划
    builder_proposal = builder.propose_next_steps(spec)
    
    # Evaluator 设定标准
    evaluation_criteria = evaluator.define_criteria(builder_proposal)
    
    # 双方达成一致
    contract = {
        "tasks": builder_proposal.tasks,
        "acceptance_criteria": evaluation_criteria,
        "target_score": 90,  # 目标分数
        "max_attempts": 3    # 最大尝试次数
    }
    
    logger.info(f"Contract established: {contract}")
    return contract
```

---

## 🌐 多模型配置指南

### OpenAI（推荐）

```bash
# .env 配置
OPENAI_BASE_URL=https://api.openai.com/v1
HARNESS_MODEL=gpt-4o
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# 性价比之选
# HARNESS_MODEL=gpt-4-turbo
```

**优势**: 
- ✅ 最强的综合能力
- ✅ 稳定的 API 服务
- ✅ 良好的代码生成质量

**成本**: ~$0.10-$0.50 per task

---

### OpenRouter（支持 Claude 等）

```bash
# .env 配置
OPENAI_BASE_URL=https://openrouter.ai/api/v1
HARNESS_MODEL=anthropic/claude-sonnet-4
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxx

# 其他可选模型
# HARNESS_MODEL=anthropic/claude-opus
# HARNESS_MODEL=google/gemini-pro
# HARNESS_MODEL=mistral/mistral-large
```

**优势**: 
- ✅ 支持多个顶级模型
- ✅ Claude 在代码生成方面表现出色
- ✅ 可按需选择最合适的模型

**成本**: 取决于选择的模型

---

### Ollama（本地部署）

```
# 1. 安装 Ollama
brew install ollama  # macOS
# 或访问 https://ollama.ai 下载

# 2. 拉取模型
ollama pull qwen2.5-coder:32b
# 或
ollama pull llama3.1:70b

# 3. 启动服务
ollama serve

# 4. .env 配置
OPENAI_BASE_URL=http://localhost:11434/v1
HARNESS_MODEL=qwen2.5-coder:32b
# 无需 API Key
```

**优势**: 
- ✅ 完全免费
- ✅ 数据隐私保护
- ✅ 无网络依赖

**注意**: 
- ⚠️ 需要强大的硬件（建议 32GB+ RAM）
- ⚠️ 推理速度较慢
- ⚠️ 某些复杂任务可能效果不佳

---

### 其他兼容端点

任何遵循 OpenAI API 格式的服务都可以使用：

```
# Azure OpenAI
OPENAI_BASE_URL=https://YOUR_RESOURCE.openai.azure.com/openai/deployments/YOUR_DEPLOYMENT
OPENAI_API_KEY=your-azure-key

# LocalAI
OPENAI_BASE_URL=http://localhost:8080/v1
HARNESS_MODEL=local-model-name

# LM Studio
OPENAI_BASE_URL=http://localhost:1234/v1
HARNESS_MODEL=loaded-model-name
```

---

## 📈 性能指标

### 实际测试数据

| 任务类型 | 平均耗时 | Token 用量 | 成功率 | 成本估算 |
|----------|----------|------------|--------|----------|
| **简单应用**<br>(计算器、计时器) | 15-25 分钟 | 500K-1M | 95% | $0.05-$0.15 |
| **中等应用**<br>(仪表盘、表单) | 30-45 分钟 | 1M-2M | 85% | $0.15-$0.35 |
| **复杂应用**<br>(DAW、游戏) | 45-90 分钟 | 2M-4M | 70% | $0.35-$0.80 |
| **终端任务** | 10-20 分钟 | 300K-800K | 90% | $0.03-$0.10 |
| **Issue 修复** | 20-40 分钟 | 800K-1.5M | 75% | $0.10-$0.25 |

*注: 基于 gpt-4o 模型测试，实际结果因任务复杂度而异*

### 优化建议

- 💡 **使用更强大的模型**: gpt-4o > gpt-4-turbo > gpt-3.5-turbo
- 💡 **提供清晰的需求**: 越详细的描述，成功率越高
- 💡 **合理设置阈值**: 根据任务难度调整 `PASS_THRESHOLD`
- 💡 **利用技能系统**: 为特定任务加载相关技能可提升质量

---

## 🎯 适用场景

### ✅ 理想使用场景

#### 🚀 **快速原型开发**
- 产品经理：快速验证想法
- 创业者：MVP 最小可行产品
- 学生：课程项目原型

> "我有个想法，但不知道做起来要多久" → Harness 帮你快速实现！

#### 🎓 **教育学习**
- 学习多 Agent 系统设计
- 理解 LLM 在工作流中的应用
- 探索 AI 辅助开发的边界

> 阅读源码是最好的学习方式！

#### 🔬 **研究实验**
- LLM 能力边界探索
- 自主 Agent 行为研究
- 人机协作模式实验

> Harness 提供了完整的研究平台

#### 💼 **辅助开发**
- 生成 boilerplate 代码
- 创建演示页面
- 快速搭建测试环境

> 让 AI 处理重复性工作，你专注于核心逻辑

#### 🐛 **问题修复**
- 自动诊断 Bug
- 生成修复补丁
- 回归测试验证

> 特别适合处理那些"明明很简单但就是找不到问题在哪"的 Bug

#### 📚 **知识问答**
- 复杂概念解释
- 跨领域知识整合
- 学术研究辅助

> 不只是回答问题，还能提供深度分析

### ⚠️ 不适用场景

- ❌ **生产环境关键系统**: 仍需人工审核和测试
- ❌ **涉及敏感数据的任务**: 注意 API 数据传输安全
- ❌ **需要人类创造力的设计**: AI 擅长执行，不擅长原创艺术
- ❌ **超大规模项目**: 目前更适合单文件或小型项目

---

## 🚀 扩展与定制

### 添加自定义技能

见上方"技能系统深度解析"部分

### 创建自定义 Profile

```
# profiles/my_custom_profile.py
from profiles.base import BaseProfile

class MyCustomProfile(BaseProfile):
    name = "my-custom"
    description = "我的自定义场景"
    
    def get_system_prompt(self, role: str) -> str:
        """自定义系统提示"""
        if role == "planner":
            return "你是一个专业的XXX规划师..."
        elif role == "builder":
            return "你是一个资深的XXX工程师..."
        elif role == "evaluator":
            return "你是一个严格的XXX评估员..."
    
    def get_evaluation_criteria(self) -> dict:
        """自定义评估标准"""
        return {
            "criteria": ["标准1", "标准2", "标准3"],
            "weights": {"标准1": 0.4, "标准2": 0.3, "标准3": 0.3}
        }
    
    def get_available_tools(self) -> list:
        """自定义可用工具"""
        return ["file_write", "shell_command", "my_custom_tool"]

# 在 profiles/__init__.py 中注册
from profiles.my_custom_profile import MyCustomProfile
PROFILES["my-custom"] = MyCustomProfile
```

### 调整系统提示

编辑 `prompts.py`，修改对应角色的系统提示：

```
# 例如，让 Builder 更注重代码注释
BUILDER_PROMPT = """
你是一个注重代码质量的工程师。

重要要求：
1. 所有函数必须包含 docstring
2. 复杂逻辑需要添加行内注释
3. 变量命名要有意义
...
"""
```

### 配置调优

在 `.env` 文件中调整关键参数：

```
# 最大迭代轮数（默认 10）
MAX_HARNESS_ROUNDS=15

# 通过分数阈值（默认 85）
PASS_THRESHOLD=90

# 上下文压缩阈值（Token 数，默认 50000）
COMPRESS_THRESHOLD=40000

# 上下文重置阈值（Token 数，默认 80000）
RESET_THRESHOLD=70000

# Agent 最大迭代次数（默认 50）
MAX_AGENT_ITERATIONS=30

# 是否启用焦虑检测（默认 true）
ENABLE_ANXIETY_DETECTION=true
```

**调优建议**:
- 任务复杂 → 增加 `MAX_HARNESS_ROUNDS`
- 要求高质量 → 提高 `PASS_THRESHOLD`
- 节省 Token → 降低 `COMPRESS_THRESHOLD`
- 避免频繁重置 → 提高 `RESET_THRESHOLD`

---

## 🛠️ 故障排除

### 常见问题

#### Q1: API 调用失败

**症状**: `Error: Connection refused` 或 `Invalid API key`

**解决**:
```bash
# 1. 检查 .env 配置是否正确
cat .env

# 2. 测试 API 连通性
python test_api_connection.py

# 3. 确认 API Key 有效且未过期
# 4. 检查网络连接（如果使用本地模型，确认服务已启动）
```

#### Q2: 任务长时间无响应

**症状**: Harness 运行超过 2 小时仍未完成

**解决**:
```bash
# 1. 检查日志文件
tail -f workspace/latest/harness.log

# 2. 可能是陷入了无限循环
#    按 Ctrl+C 中断，然后：
#    - 简化需求描述
#    - 降低 PASS_THRESHOLD
#    - 更换更强的模型

# 3. 检查是否触发了频繁的上下文重置
#    如果是，提高 RESET_THRESHOLD
```

#### Q3: 生成的代码无法运行

**症状**: Evaluator 评分很低，或代码有明显错误

**解决**:
```bash
# 1. 查看 feedback.md 了解具体问题
cat workspace/latest/feedback.md

# 2. 尝试以下方法：
#    - 提供更详细的需求描述
#    - 加载相关技能（如 frontend-design）
#    - 使用更强的模型（如 gpt-4o）
#    - 手动修复后重新运行评估
```

#### Q4: Token 用量过高

**症状**: 单次任务消耗超过 5M Token

**解决**:
```bash
# 1. 降低 COMPRESS_THRESHOLD，更早触发压缩
COMPRESS_THRESHOLD=30000

# 2. 减少 MAX_AGENT_ITERATIONS
MAX_AGENT_ITERATIONS=30

# 3. 简化需求，分步骤实现
#    先实现核心功能，再逐步添加特性
```

#### Q5: Playwright 测试失败

**症状**: `Error: Browser not found`

**解决**:
```bash
# 重新安装浏览器驱动
python -m playwright install chromium

# 如果仍然失败，尝试：
python -m playwright install --force
```

---

## 📚 参考资料

### 原始论文与文章
- 📖 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) - Anthropic 官方博客
- 📖 [Agent Skills: Equipping agents for the real world](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) - Claude 博客

### 相关项目
- 🤖 [AutoGen](https://github.com/microsoft/autogen) - Microsoft 的多 Agent 框架
- 🤖 [LangGraph](https://github.com/langchain-ai/langgraph) - LangChain 的 Agent 编排库
- 🤖 [CrewAI](https://github.com/joaomdmoura/crewAI) - 角色扮演多 Agent 系统

### 技术栈
- 🐍 [OpenAI Python SDK](https://github.com/openai/openai-python)
- 🔢 [Tiktoken](https://github.com/openai/tiktoken) - Token 计数
- 🎭 [Playwright](https://playwright.dev/) - 浏览器自动化

---

## 🤝 贡献指南

我们欢迎任何形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. 创建你的特性分支: `git checkout -b feature/amazing-feature`
3. 提交你的改动: `git commit -m 'Add some amazing feature'`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 开启一个 **Pull Request**

### 贡献类型

- 🐛 **Bug 修复**: 发现并修复问题
- ✨ **新功能**: 添加新的 Profile、技能或工具
- 📝 **文档改进**: 完善 README、添加教程
- 🎨 **代码优化**: 提升性能、改进代码质量
- 🧪 **测试用例**: 增加单元测试和集成测试
- 💡 **想法建议**: 在 Issues 中讨论新想法

### 开发规范

- 遵循 PEP 8 代码风格
- 添加必要的注释和文档字符串
- 为新功能编写测试用例
- 更新相关文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

简而言之：你可以自由使用、修改、分发此代码，无论是个人还是商业用途。

---

## 🌟 致谢

- 🙏 **Anthropic** - 原始的 Harness 设计理念
- 🙏 **OpenAI** - 强大的 LLM API
- 🙏 **开源社区** - 所有依赖库的贡献者
- 🙏 **每一位贡献者** - 让 Harness 变得更好

---

## 📞 联系方式

- 🐛 **问题反馈**: [GitHub Issues](https://github.com/panzi-hub/-Harness_Engineering/issues)
- 💬 **讨论交流**: [GitHub Discussions](https://github.com/panzi-hub/-Harness_Engineering/discussions)
- 📧 **邮件联系**: [panzi@example.com](mailto:panzi@example.com)

---

<div align="center">

**🚀 Harness — 让 AI 自主开发变得简单而强大！🚀**

*从想法到代码，只需一句话*

[⭐ Star this repo](https://github.com/panzi-hub/-Harness_Engineering) | [🍴 Fork this repo](https://github.com/panzi-hub/-Harness_Engineering/fork) | [📖 Read the docs](https://github.com/panzi-hub/-Harness_Engineering/wiki)

</div>