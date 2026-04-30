# 项目结构说明 📂

> **整理后的Harness Engineering目录结构**

---

## 🎯 整理原则

根据用户偏好，采用**保守整理方案**：
- ✅ 核心Python代码保留在根目录（可直接运行）
- ✅ 文档文件统一移到`docs/`目录
- ✅ 测试文件移到`tests/`目录
- ✅ 脚本文件移到`scripts/`目录
- ✅ 清理临时文件和运行时产物

---

## 📁 当前目录结构

```
Harness_Engineering/
│
├── 📄 根目录 - 核心代码（9个.py文件 + 配置）
│   ├── harness.py              # 🚀 主入口 - 直接运行: python harness.py "..."
│   ├── agents.py               # 🤖 Agent运行时核心
│   ├── context.py              # 🧠 上下文管理
│   ├── tools.py                # 🛠️ 工具集（1075行）
│   ├── prompts.py              # 💬 提示词工程
│   ├── skills.py               # 🎓 技能管理
│   ├── config.py               # ⚙️ 配置管理
│   ├── logger.py               # 📝 日志系统
│   ├── middlewares.py          # 🔧 中间件系统
│   │
│   ├── .env.template           # 环境配置模板
│   ├── .env.example            # 环境配置示例
│   ├── requirements.txt        # Python依赖
│   ├── .gitignore              # Git忽略规则
│   └── README.md               # 项目主文档
│
├── 📁 docs/                    # 📚 所有文档
│   ├── README.md               # 文档目录说明
│   ├── ARCHITECTURE.md         # 详细架构文档（~1500行）
│   ├── ARCHITECTURE_QUICK.md   # 快速架构概览（~500行）
│   ├── ARCHITECTURE_DIAGRAMS.md # 架构可视化图表（12个Mermaid图）
│   ├── ARCHITECTURE_SUMMARY.md  # 架构整理总结
│   ├── CLAUDE.md               # Claude相关说明
│   ├── PROFILES.md             # Profile使用指南
│   ├── QUICK_REFERENCE.md      # 快速参考手册
│   ├── README_EN.md            # 英文README
│   │
│   └── templates/              # 📋 文档模板
│       ├── README.md           # 模板说明
│       ├── spec.md             # 产品规格模板
│       ├── contract.md         # Contract协商模板
│       └── feedback.md         # 评估反馈模板
│
├── 📁 tests/                   # 🧪 测试文件
│   ├── README.md               # 测试说明
│   ├── test_api.py             # API连接测试
│   └── test_api_connection.py  # 详细API检查
│
├── 📁 scripts/                 # 📜 脚本文件
│   ├── run_benchmark_v2.sh     # 基准测试脚本
│   └── analyze_results.py      # 结果分析脚本
│
├── 📁 benchmarks/              # 📊 基准测试数据
│   ├── README.md
│   ├── harbor_agent.py
│   └── tb2_tasks.json
│
├── 📁 profiles/                # 🎭 Profile配置
│   ├── __init__.py
│   ├── base.py                 # 基础Profile类
│   ├── app_builder.py          # Web应用开发
│   ├── terminal.py             # 终端任务
│   ├── swe_bench.py            # GitHub Issue修复
│   └── reasoning.py            # 知识问答
│
├── 📁 skills/                  # 🎓 技能库（37个技能）
│   ├── frontend-design/
│   ├── password-recovery/
│   ├── video-processing/
│   └── ... (34 more)
│
├── 📁 workspace/               # 📂 运行时输出（Git忽略）
│   └── latest/                 # 最新任务输出
│       ├── spec.md
│       ├── contract.md
│       ├── feedback.md
│       └── ... (生成的代码)
│
├── 📁 logs/                    # 📝 日志文件（Git忽略）
│   └── harness.log
│
└── 📁 vendor_wheels/           # 📦 离线依赖包
    └── *.whl
```

---

## 📊 整理对比

### 整理前
```
根目录文件数: ~25个
├── 核心代码: 9个.py
├── 文档: 6个.md ❌ 太分散
├── 测试: 2个.py ❌ 混在根目录
├── 脚本: 1个.sh ❌ 混在根目录
├── 临时文件: 5个 ❌ 应该忽略
└── 配置文件: 3个
```

### 整理后 ✅
```
根目录文件数: 13个（全部核心必需）
├── 核心代码: 9个.py ✅ 保持扁平，直接运行
├── 配置文件: 4个 ✅ 必需的配置
└── 主文档: 1个.md ✅ README

其他文件已分类:
├── docs/: 12个文档文件 ✅ 统一管理
├── tests/: 2个测试文件 ✅ 集中存放
└── scripts/: 2个脚本文件 ✅ 清晰分类
```

---

## 🎯 核心设计决策

### 1. 为什么核心代码保留在根目录？

**理由：**
- ✅ 符合用户"直接运行"的偏好：`python harness.py "..."`
- ✅ Python项目惯例：大多数开源项目核心模块在根目录
- ✅ 导入简单：`import agents` 而非 `from src import agents`
- ✅ 降低学习成本：新人更容易找到入口

**对比src/方案：**
```bash
# 根目录方案（当前）✅
python harness.py "Build a calculator"

# src/方案（未采用）❌
python src/harness.py "Build a calculator"
# 或需要安装为包
pip install -e .
harness "Build a calculator"
```

### 2. 为什么文档放到docs/？

**理由：**
- ✅ 根目录更清爽
- ✅ 文档集中管理，易于查找
- ✅ GitHub会自动渲染docs/中的Markdown
- ✅ 可以设置GitHub Pages指向docs/

### 3. 为什么测试放到tests/？

**理由：**
- ✅ 符合Python测试惯例（pytest默认查找tests/）
- ✅ 与生产代码分离
- ✅ 可以单独运行测试：`pytest tests/`

### 4. 为什么脚本放到scripts/？

**理由：**
- ✅ 与核心代码分离
- ✅ 明确用途：辅助工具而非主程序
- ✅ 便于维护和管理

---

## 🚀 常用命令

### 运行Harness
```bash
# 直接使用（最简洁）✅
python harness.py "Build a Pomodoro timer"

# 指定Profile
python harness.py --profile terminal "Fix broken symlinks"

# 查看帮助
python harness.py --help
```

### 运行测试
```bash
# 测试API连接
python tests/test_api.py

# 运行所有测试
pytest tests/
```

### 运行脚本
```bash
# 基准测试
bash scripts/run_benchmark_v2.sh

# 分析结果
python scripts/analyze_results.py
```

### 查看文档
```bash
# 快速架构概览
cat docs/ARCHITECTURE_QUICK.md

# 详细架构文档
cat docs/ARCHITECTURE.md

# 查看图表
cat docs/ARCHITECTURE_DIAGRAMS.md
```

---

## 📝 Git提交建议

整理后的提交信息：

```bash
git add .
git commit -m "refactor: 整理项目结构

- 移动文档到 docs/ 目录
- 移动测试到 tests/ 目录  
- 移动脚本到 scripts/ 目录
- 清理临时文件（trace, .env.temp）
- 更新 .gitignore
- 添加目录说明文档

保持核心代码在根目录，支持直接运行：
python harness.py \"...\"
"
```

---

## 🔍 文件分类规则

### 应该放在根目录的文件
- ✅ 核心Python模块（直接被import或运行）
- ✅ 项目配置文件（.env.template, requirements.txt）
- ✅ 主README.md

### 应该放到子目录的文件
- 📚 文档 → `docs/`
- 🧪 测试 → `tests/`
- 📜 脚本 → `scripts/`
- 📊 基准测试 → `benchmarks/`
- 🎭 Profile配置 → `profiles/`（已有）
- 🎓 技能库 → `skills/`（已有）
- 📂 运行时输出 → `workspace/`（Git忽略）

---

## 💡 未来扩展

如果需要进一步整理，可以考虑：

1. **添加examples/目录** - 存放示例用法
2. **添加tutorials/目录** - 教程文档
3. **创建setup.py** - 如果将来需要打包发布
4. **添加Dockerfile** - 容器化部署

但目前结构已经足够清晰，无需过度整理！

---

<div align="center">

**✨ 整理完成！项目结构更加清晰合理！**

*核心代码保持扁平，文档测试有序分类*

</div>