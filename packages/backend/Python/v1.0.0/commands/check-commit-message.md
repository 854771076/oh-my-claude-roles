---
name: check-commit-message
description: 检查提交信息是否符合Conventional Commits规范
trigger: check-commit-message
---

检查当前待提交的代码的提交信息是否符合规范要求，如果不符合给出修正建议。

### 检查要点：
1. 是否符合格式：`<type>(<scope>): <subject>`
2. type是否使用了规定的类型（feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert）
3. subject是否简洁清晰，中文描述，不超过50字符
4. 是否存在模糊无意义的提交信息
5. 是否一次提交包含多个不相关变更

### 输出要求：
- 如果符合规范，确认通过
- 如果不符合，说明问题，给出多个修正后的示例供选择

---