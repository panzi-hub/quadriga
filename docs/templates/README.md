# Templates - 模板文件目录

本目录包含Harness运行时生成的文档模板，供参考使用。

## 📁 文件说明

- **spec.md** - 产品规格文档模板
- **contract.md** - Sprint Contract协商模板  
- **feedback.md** - Evaluator反馈模板

## 💡 使用说明

这些文件是Harness运行时的**输出示例**，展示了：

1. **spec.md** - Planner生成的产品规格格式
2. **contract.md** - Builder和Evaluator协商的验收标准
3. **feedback.md** - Evaluator的评估反馈和评分

## 🔍 查看实际输出

运行Harness后，在`workspace/latest/`目录中会生成实际的文档：

```bash
python harness.py "Build a calculator"
cat workspace/latest/spec.md
cat workspace/latest/contract.md
cat workspace/latest/feedback.md
```

## 📝 自定义模板

如果你想修改输出格式，可以编辑：
- `prompts.py` - 修改Agent的系统提示词
- `profiles/*.py` - 修改特定Profile的输出格式
