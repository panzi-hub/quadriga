# Tests - 测试文件目录

本目录包含Harness Engineering的测试和工具脚本。

## 📁 文件说明

- **test_api.py** - API连接测试脚本
- **test_api_connection.py** - 详细的API连通性检查

## 🚀 使用方法

### 测试API连接

```bash
# 快速测试
python tests/test_api.py

# 详细测试
python tests/test_api_connection.py
```

### 前置要求

确保已配置`.env`文件：

```bash
cp .env.template .env
# 编辑.env，填入你的API Key
```

## 📝 添加新测试

在此目录中添加新的测试文件，命名规范：
- `test_*.py` - 单元测试
- `check_*.py` - 检查脚本
- `demo_*.py` - 演示脚本

## 🔧 运行所有测试

```bash
# 使用pytest（如果安装）
pytest tests/

# 或手动运行
for test in tests/test_*.py; do
    echo "Running $test..."
    python "$test"
done
```
