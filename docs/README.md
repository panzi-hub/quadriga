# Harness Engineering - 文档中心 📚

> **完整的文档体系，帮助你快速理解和使用Harness**

---

## 🗺️ 新手入门路径

### 第1步：了解项目（5分钟）
👉 [快速架构概览](ARCHITECTURE_QUICK.md)  
快速了解Harness的核心组件和工作流程

### 第2步：运行示例（10分钟）
👉 返回 [主README](../README.md)  
按照快速开始指南运行第一个任务

### 第3步：深入理解（30分钟）
👉 [详细架构文档](ARCHITECTURE.md)  
全面了解系统架构、设计模式和扩展方法

### 第4步：查看图表（15分钟）
👉 [架构可视化图表](ARCHITECTURE_DIAGRAMS.md)  
通过12个Mermaid图表直观理解系统

---

## 📖 文档分类

### 🏗️ 架构文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [ARCHITECTURE_QUICK.md](ARCHITECTURE_QUICK.md) | 5分钟快速概览 | 所有人 ⭐ |
| [ARCHITECTURE.md](ARCHITECTURE.md) | 完整架构详解 | 开发者、研究者 |
| [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) | 12个可视化图表 | 视觉学习者 |
| [ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md) | 架构整理总结 | 维护者 |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 项目结构说明 | 所有人 |

### 📋 使用指南

| 文档 | 说明 |
|------|------|
| [PROFILES.md](PROFILES.md) | Profile配置和使用指南 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速参考手册（命令速查） |
| [CLAUDE.md](CLAUDE.md) | Claude相关配置说明 |

### 🌍 多语言

| 文档 | 说明 |
|------|------|
| [README_EN.md](README_EN.md) | English version of README |
| [README.md](../README.md) | 中文主文档 |

### 📝 模板文件

位于 [templates/](templates/) 目录：
- `spec.md` - 产品规格模板
- `contract.md` - Contract协商模板
- `feedback.md` - 评估反馈模板

---

## 🎯 按角色推荐阅读

### 👶 初学者
1. [快速架构概览](ARCHITECTURE_QUICK.md)
2. [主README](../README.md) - 快速开始部分
3. [快速参考手册](QUICK_REFERENCE.md)

### 👨‍💻 开发者
1. [详细架构文档](ARCHITECTURE.md)
2. [架构可视化图表](ARCHITECTURE_DIAGRAMS.md)
3. [Profiles使用指南](PROFILES.md)
4. [项目结构说明](PROJECT_STRUCTURE.md)

### 🔬 研究者
1. [详细架构文档](ARCHITECTURE.md) - 设计模式部分
2. [架构整理总结](ARCHITECTURE_SUMMARY.md)
3. [架构可视化图表](ARCHITECTURE_DIAGRAMS.md) - 数据流图

### 🛠️ 维护者
1. [架构整理总结](ARCHITECTURE_SUMMARY.md)
2. [项目结构说明](PROJECT_STRUCTURE.md)
3. [详细架构文档](ARCHITECTURE.md) - 扩展指南部分

---

## 📊 文档统计

| 类型 | 数量 | 总行数 |
|------|------|--------|
| 架构文档 | 5 | ~3500行 |
| 使用指南 | 3 | ~800行 |
| 模板文件 | 3 | ~200行 |
| **总计** | **11** | **~4500行** |

---

## 🔍 快速查找

### 想了解...

- **整体架构？** → [ARCHITECTURE_QUICK.md](ARCHITECTURE_QUICK.md) 第1节
- **核心组件？** → [ARCHITECTURE.md](ARCHITECTURE.md) 第2节
- **数据流向？** → [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) 图表9
- **如何扩展？** → [ARCHITECTURE.md](ARCHITECTURE.md) 第5节
- **性能优化？** → [ARCHITECTURE.md](ARCHITECTURE.md) 第6节
- **目录结构？** → [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **可用命令？** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 💡 使用技巧

### GitHub在线查看
所有Markdown文件都可以在GitHub上直接浏览，支持：
- ✅ Mermaid图表渲染
- ✅ 代码高亮
- ✅ 目录导航

### 本地查看
```bash
# 使用VS Code预览Markdown
code docs/ARCHITECTURE.md

# 或使用其他Markdown阅读器
open docs/ARCHITECTURE.md  # macOS
xdg-open docs/ARCHITECTURE.md  # Linux
```

### 搜索文档
```bash
# 在文档中搜索关键词
grep -r "Context管理" docs/*.md

# 查找特定主题
grep -l "Profile" docs/*.md
```

---

## 📝 贡献文档

欢迎改进文档！你可以：

1. **修正错误** - 发现拼写或技术错误
2. **补充内容** - 添加缺失的说明
3. **改进结构** - 让文档更清晰易懂
4. **翻译文档** - 添加其他语言版本

提交Pull Request时，请说明：
- 修改了哪些文档
- 为什么需要这些修改
- 对读者有什么帮助

---

## 🔄 文档更新记录

### 2024-XX-XX
- ✨ 创建完整的架构文档体系
- 📊 添加12个Mermaid可视化图表
- 📁 整理项目结构，创建文档目录
- 📝 编写项目结构说明文档

---

<div align="center">

**📚  Happy Reading! 享受阅读！**

*有问题？欢迎提交Issue或Pull Request*

</div>