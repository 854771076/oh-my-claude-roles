---
name: run-pre-commit-checks
description: 执行所有pre-commit检查项，验证代码是否符合提交要求
trigger: run-pre-commit-checks
---

按照规范执行所有代码提交前的检查项，确保代码符合准入要求。

### 执行检查：
1. black代码格式化检查
2. isort导入顺序检查
3. pylint静态代码检查，验证评分≥9分
4. mypy类型安全检查
5. 敏感信息扫描，检查是否误提交密钥密码
6. 运行单元测试smoke校验

### 输出要求：
- 列出每个检查项的结果：通过/失败
- 对于失败项，说明问题和修复建议
- 所有检查通过后，确认可以提交代码