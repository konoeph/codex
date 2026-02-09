# 自动审查 Agent

此仓库提供一个轻量脚本，用于读取测试文件并生成自动审查报告，帮助你快速发现缺少断言、跳过测试或遗留注释等常见问题。

## 使用方法

```bash
python3 auto_review_agent.py path/to/test_file.py
```

不传路径时，脚本默认读取当前目录下的 `test file`。

## 输出示例

```
# Automated Review Report

## path/to/test_file.py
- **Coverage:** No assertions found; consider adding assertions to validate behavior.
- **Notes:** Contains TODO/FIXME markers to review.
```

## 适用场景

- 快速检查测试文件是否包含断言
- 识别被跳过的测试
- 发现测试中的临时打印语句或待办事项
