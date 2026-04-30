# Harness 快速使用参考

## 基本用法

```bash
# Web 应用构建（默认 app-builder profile）
python harness.py "Build a todo app with React"

# 指定 Profile
python harness.py --profile terminal "Fix the broken git merge"
python harness.py --profile app-builder "Build a markdown editor"

# 详细输出
python harness.py --verbose "Build a calculator"

# 查看可用 Profile
python harness.py --list-profiles
```

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt
python -m playwright install chromium

# 运行后查看 workspace
ls workspace/
cat workspace/*/spec.md      # 查看规格说明书
cat workspace/*/feedback.md  # 查看评估反馈
```

## 调试

```bash
# 查看 Agent 决策跟踪
cat workspace/*/_trace_builder.jsonl

# 查看任务清单
cat workspace/*/_todo.md

# 查看上下文重置 checkpoint
cat workspace/*/progress.md
```

## 常见任务示例

```bash
# 构建 Web 应用
python harness.py "Build a weather app with geolocation"

# 修复 Bug（Terminal Profile）
python harness.py --profile terminal "Fix the segmentation fault in parser.c"

# 完整流程
python harness.py "Build a REST API with authentication"
# → 查看 spec.md
# → 查看 feedback.md（评估分数）
# → 自动迭代直到通过 PASS_THRESHOLD
```
