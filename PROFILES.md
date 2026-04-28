# Profile 快速对比

## App Builder Profile

**用途**：Web 应用构建（Anthropic 文章原始场景）

**启用组件**：
- ✅ Planner (7% 时间)
- ✅ Builder (83% 时间)
- ✅ Evaluator (10% 时间) + browser_test
- ✅ Contract Negotiation (proposer + reviewer)
- ⚪ Middlewares (无)

**工具集**：完整 TOOL_SCHEMAS
- read_file, write_file, edit_file, list_files, run_bash
- read_skill_file, delegate_task
- web_search, web_fetch
- browser_test, stop_dev_server

**适用场景**：
- 从零构建 Web 应用
- 需要 Playwright 浏览器测试
- 有产品规格说明书需要规划

**示例**：
```bash
python harness.py --profile app-builder "Build a markdown editor with preview"
python harness.py --profile app-builder "Create a dashboard with charts"
```

---

## Terminal Profile

**用途**：CLI 任务（Terminal-Bench 2.0 风格）

**启用组件**：
- ⚪ Planner (短任务跳过)
- ✅ Builder (100% 时间)
- ⚪ Evaluator (无)
- ⚪ Contract Negotiation (无)

**中间件**（全部启用）：
- ✅ LoopDetectionMiddleware — 检测文件编辑次数 / 命令重复
- ✅ PreExitVerificationMiddleware — 退出前强制验证
- ✅ TimeBudgetMiddleware — 时间预算警告
- ✅ TaskTrackingMiddleware — 强制 _todo.md
- ✅ SkeletonDetectionMiddleware — 防止忽略 TODO 文件
- ✅ ErrorGuidanceMiddleware — 错误恢复指导

**工具集**：TB2_TOOL_SCHEMAS（简化版，无网络/子 Agent）
- read_file, write_file, edit_file, list_files, run_bash

**适用场景**：
- 修复已存在的代码库问题
- CLI 工具 / 脚本任务
- 短时间任务（≤30 分钟）

**示例**：
```bash
python harness.py --profile terminal "Fix the memory leak in server.c"
python harness.py --profile terminal "Add --json flag to the CLI tool"
```

---

## 关键差异

| 特性 | App Builder | Terminal |
|------|-------------|----------|
| 规划阶段 | ✅ 有 | ❌ 无 |
| 浏览器测试 | ✅ 有 | ❌ 无 |
| 合同协商 | ✅ 有 | ❌ 无 |
| 中间件 | 无 | 6 个全开 |
| 网络工具 | ✅ 有 | ❌ 无 |
| 子 Agent | ✅ 有 | ❌ 无 |
| 时间预算 | 弹性分配 | 固定（如 1800s） |

---

## 选择指南

```
需要规划产品方向？
  ├─ YES → App Builder
  └─ NO → 继续...

任务是 CLI 脚本/Bug 修复？
  ├─ YES → Terminal
  └─ NO → 继续...

需要浏览器测试？
  ├─ YES → App Builder
  └─ NO → Terminal
```