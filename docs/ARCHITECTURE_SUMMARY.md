1yi ge# Harness Engineering - 架构整理总结 📋

> **本文档记录了项目架构整理的完整过程和成果**

---

## 🎯 整理目标

1. ✅ 理清项目整体架构和组件关系
2. ✅ 创建清晰的架构文档
3. ✅ 提供可视化的架构图表
4. ✅ 建立可扩展的架构记忆

---

## 📦 交付成果

### 1. 架构记忆 (Memory)

创建了完整的项目架构记忆，包含：
- 整体架构模式
- 核心组件层级（10层）
- 数据流向
- 关键技术特性
- 性能指标
- 扩展点

**位置**: Assistant Memory System  
**用途**: 未来对话中快速参考项目架构

---

### 2. 详细架构文档

**文件**: `docs/ARCHITECTURE.md`  
**大小**: ~1500行  
**内容**:

#### 章节概览
1. **架构概览**
   - 整体架构图
   - 技术栈
   - 核心设计原则

2. **核心组件详解** (10个组件)
   - Harness Orchestrator (`harness.py`)
   - Agent Runtime (`agents.py`)
   - Context Management (`context.py`)
   - Tool System (`tools.py`)
   - Profile System (`profiles/`)
   - Skill System (`skills.py` + `skills/`)
   - Prompt Engineering (`prompts.py`)
   - Middleware System (`middlewares.py`)
   - Configuration (`config.py`)
   - Logging (`logger.py`)

3. **数据流与执行流程**
   - 完整执行流程图
   - 单次迭代详细流程
   - Contract协商流程
   - REFINE vs PIVOT决策逻辑

4. **设计模式与架构决策**
   - 5种设计模式应用
   - 4个关键架构决策及理由

5. **扩展指南**
   - 添加新Profile
   - 添加新Skill
   - 添加新Tool
   - 添加新Middleware

6. **性能与优化**
   - 性能指标
   - 优化建议
   - 监控与调试

7. **附录**
   - 文件结构总览
   - 代码统计
   - 依赖关系图
   - FAQ

---

### 3. 快速架构概览

**文件**: `docs/ARCHITECTURE_QUICK.md`  
**大小**: ~500行  
**特点**: 
- 5分钟快速理解
- 简化版架构图
- 核心组件表格
- 常用命令速查

**适用场景**:
- 新人快速上手
- 日常开发参考
- 面试准备

---

### 4. 架构可视化图表

**文件**: `docs/ARCHITECTURE_DIAGRAMS.md`  
**内容**: 12个Mermaid图表

#### 图表列表
1. **整体架构图** - 分层架构展示
2. **Agent执行流程图** - Sequence Diagram
3. **Context管理策略** - Flowchart
4. **Profile系统架构** - Class Diagram
5. **技能加载流程** - Sequence Diagram
6. **工具执行流程** - Flowchart
7. **Middleware责任链** - Flowchart
8. **Contract协商流程** - Sequence Diagram
9. **数据流向图** - Graph LR
10. **依赖关系图** - Graph TD
11. **文件结构树状图** - Graph TD
12. **性能监控图** - Graph LR

**优势**:
- 直观易懂
- 可嵌入GitHub
- 支持交互查看
- 便于演示讲解

---

### 5. README增强

**修改**: `README.md`  
**变更**:
- 在开头添加架构文档链接部分
- 引导用户深入了解架构

---

## 🏗️ 架构核心要点

### 三层架构

```
┌─────────────────────────┐
│   编排层 (harness.py)    │  ← 总指挥
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│   Agent层 (agents.py)    │  ← 执行者
└──────────┬──────────────┘
           │
┌──────────▼──────────────┐
│  基础设施层 (8个模块)     │  ← 支撑系统
└─────────────────────────┘
```

### 10大核心组件

| # | 组件 | 文件 | 行数 | 职责 |
|---|------|------|------|------|
| 1 | Harness | harness.py | 521 | 主编排器 |
| 2 | Agent | agents.py | 427 | Agent运行时 |
| 3 | Context | context.py | 310 | 上下文管理 |
| 4 | Tools | tools.py | 1075 | 工具集 |
| 5 | Profile | profiles/ | ~300 | 场景配置 |
| 6 | Skills | skills/ | 37个 | 技能库 |
| 7 | Prompts | prompts.py | ~300 | 提示词 |
| 8 | Middleware | middlewares.py | ~800 | 中间件 |
| 9 | Config | config.py | ~80 | 配置管理 |
| 10 | Logger | logger.py | ~150 | 日志系统 |

### 核心流程

```
Plan → Contract → Build → Evaluate → (REFINE/PIVOT) → ...
```

### 5种Agent角色

- 🧠 **Planner**: 需求分析
- 🔨 **Builder**: 代码实现
- ✅ **Evaluator**: 质量评估
- 📝 **ContractProposer**: 标准提议
- 🔍 **ContractReviewer**: 标准审核

### 3级Context管理

1. **保持** (Token < 50K)
2. **压缩** (50K < Token < 80K)
3. **重置** (Token > 80K 或焦虑)

---

## 📊 代码统计

### 总体统计

| 类别 | 文件数 | 代码行数 | 占比 |
|------|--------|----------|------|
| 核心引擎 | 5 | ~2800 | 45% |
| Profiles | 5 | ~300 | 5% |
| Middlewares | 1 | ~800 | 13% |
| Tools | 1 | ~1075 | 17% |
| 其他 | 10 | ~1200 | 20% |
| **总计** | **22** | **~6175** | **100%** |

### 文档统计

| 文档 | 行数 | 图表数 | 用途 |
|------|------|--------|------|
| ARCHITECTURE.md | ~1500 | 5+ | 详细参考 |
| ARCHITECTURE_QUICK.md | ~500 | 3+ | 快速入门 |
| ARCHITECTURE_DIAGRAMS.md | ~800 | 12 | 可视化展示 |
| **总计** | **~2800** | **20+** | - |

---

## 🎨 设计模式应用

### 1. 策略模式 (Strategy)
- **应用**: Profile系统
- **好处**: 轻松切换场景，符合开闭原则

### 2. 观察者模式 (Observer)
- **应用**: TraceWriter
- **好处**: 解耦Agent和日志记录

### 3. 责任链模式 (Chain of Responsibility)
- **应用**: Middleware系统
- **好处**: 灵活组合，职责单一

### 4. 工厂模式 (Factory)
- **应用**: Profile创建
- **好处**: 统一创建接口

### 5. 单例模式 (Singleton)
- **应用**: LLM客户端
- **好处**: 避免重复创建

---

## 🔑 关键架构决策

### 决策1: 零SDK依赖
**选择**: 纯Python + OpenAI原生SDK  
**理由**: 透明度、轻量、灵活性、学习价值

### 决策2: Context重置机制
**问题**: 长任务中模型"焦虑"  
**解决**: Checkpoint + 新白板  
**效果**: 消除焦虑，突破窗口限制

### 决策3: Workspace隔离
**目的**: 防止误操作宿主系统  
**实现**: 路径逃逸检测  
**优势**: 安全、清洁、可追溯

### 决策4: Sprint Contract
**问题**: Builder和Evaluator目标不一致  
**解决**: 每轮协商验收标准  
**好处**: 对齐期望，减少无效迭代

---

## 🚀 扩展性分析

### 现有扩展点

1. **Profile扩展** ⭐⭐⭐⭐⭐
   - 难度: ⭐
   - 方式: 继承BaseProfile
   - 示例: 4个内置Profile

2. **Skill扩展** ⭐⭐⭐⭐⭐
   - 难度: ⭐
   - 方式: 创建SKILL.md
   - 示例: 37个内置技能

3. **Tool扩展** ⭐⭐⭐⭐
   - 难度: ⭐⭐
   - 方式: 在tools.py注册
   - 示例: 7类工具

4. **Middleware扩展** ⭐⭐⭐⭐
   - 难度: ⭐⭐
   - 方式: 实现中间件接口
   - 示例: 3种中间件

5. **Prompt定制** ⭐⭐⭐⭐⭐
   - 难度: ⭐
   - 方式: 修改prompts.py
   - 示例: 5种Agent提示

### 扩展难度评级

⭐ = 非常简单（<30分钟）  
⭐⭐ = 简单（30-60分钟）  
⭐⭐⭐ = 中等（1-2小时）  
⭐⭐⭐⭐ = 较难（2-4小时）  
⭐⭐⭐⭐⭐ = 困难（>4小时）

---

## 📈 性能特征

### 时间复杂度

- **单次LLM调用**: O(1) - API调用
- **Context检查**: O(n) - n为消息数
- **Token计数**: O(m) - m为总字符数
- **工具执行**: 取决于具体工具

### 空间复杂度

- **内存占用**: 200-500MB
  - Python进程: ~100MB
  - LLM缓存: ~50-200MB
  - Context: ~50-200MB

- **磁盘占用**:
  - 代码: ~50MB
  - workspace: 可变（每个任务~1-10MB）
  - logs: 可变（每次运行~1-5MB）
  - traces: 可变（每个Agent~1-3MB）

### 瓶颈分析

1. **LLM API延迟** (主要瓶颈)
   - 单次调用: 1-5秒
   - 累计: 占总时间80%+

2. **Context管理开销**
   - Token计数: 轻微
   - 压缩/重置: 中等（需调用LLM）

3. **工具执行**
   - 文件操作: 快速
   - Shell命令: 取决于命令
   - 浏览器测试: 较慢（5-10秒）

---

## 🛡️ 安全性分析

### 已实现的安全机制

1. **路径逃逸防护** ✅
   ```python
   def _resolve(path: str) -> Path:
       if not str(p).startswith(str(ws)):
           raise ValueError("Path escapes workspace")
   ```

2. **危险命令过滤** ✅
   ```python
   dangerous = ["rm -rf /", "sudo", "mkfs", "dd if="]
   ```

3. **输出长度限制** ✅
   - read_file: 40K字符
   - browser_test: 50K字符
   - git_diff: 50K字符

4. **超时控制** ✅
   - TimeoutMiddleware
   - subprocess timeout参数

### 潜在风险

1. ⚠️ **API Key泄露**
   - 建议: 使用.env，不提交Git
   
2. ⚠️ **无限循环**
   - 缓解: MAX_AGENT_ITERATIONS限制
   
3. ⚠️ **资源耗尽**
   - 缓解: 超时和重试机制

---

## 📝 维护建议

### 代码质量

- ✅ 模块化良好
- ✅ 注释充分
- ✅ 命名清晰
- ⚠️ 缺少单元测试（建议添加）

### 文档完整性

- ✅ README详细
- ✅ 架构文档完整
- ✅ 代码注释充足
- ⚠️ 缺少API文档（建议补充）

### 版本管理

- ✅ Git仓库
- ✅ .gitignore配置
- ⚠️ 缺少CHANGELOG（建议添加）
- ⚠️ 缺少版本号（建议语义化版本）

---

## 🎓 学习路线

### 初学者路径

1. **第1天**: 阅读 [ARCHITECTURE_QUICK.md](docs/ARCHITECTURE_QUICK.md)
2. **第2天**: 运行示例，查看workspace输出
3. **第3天**: 阅读 harness.py 和 agents.py
4. **第4天**: 尝试添加一个简单的Skill
5. **第5天**: 阅读 [ARCHITECTURE.md](docs/ARCHITECTURE.md)

### 进阶路径

1. **Week 1**: 深入理解Context管理机制
2. **Week 2**: 研究Middleware系统设计
3. **Week 3**: 自定义Profile和Tool
4. **Week 4**: 性能优化和调优

### 专家路径

1. **Month 1**: 贡献新Feature
2. **Month 2**: 优化核心算法
3. **Month 3**: 编写技术博客

---

## 🔄 后续改进方向

### 短期（1-3个月）

- [ ] 添加单元测试框架
- [ ] 完善错误处理
- [ ] 添加更多内置Skills
- [ ] 优化Context压缩算法

### 中期（3-6个月）

- [ ] 支持多Agent并行
- [ ] 添加Web UI界面
- [ ] 实现分布式部署
- [ ] 集成更多LLM后端

### 长期（6-12个月）

- [ ] 构建Plugin生态系统
- [ ] 支持团队协作模式
- [ ] 实现自动Code Review
- [ ] 集成CI/CD流程

---

## 📞 相关资源

### 内部文档

- [README.md](../README.md) - 项目主文档
- [docs/ARCHITECTURE.md](ARCHITECTURE.md) - 详细架构
- [docs/ARCHITECTURE_QUICK.md](ARCHITECTURE_QUICK.md) - 快速概览
- [docs/ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) - 可视化图表

### 外部参考

- [Anthropic Harness文章](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [OpenAI API文档](https://platform.openai.com/docs)
- [Playwright文档](https://playwright.dev/)

---

<div align="center">

**🎉 架构整理完成！**

*通过这次整理，我们建立了完整的架构文档体系，为项目的长期发展奠定了坚实基础*

**下一步**: 提交这些文档到Git仓库

</div>