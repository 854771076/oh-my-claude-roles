<content>
---
name: 生成符合规范的Commit信息
description: 根据你的修改内容生成符合Conventional Commits规范的提交信息
trigger: /vue3-commit
---

## 执行步骤
1. 根据修改类型确定type：
   - `feat`: 新增功能
   - `fix`: 修复bug
   - `docs`: 文档修改
   - `style`: 代码格式修改
   - `refactor`: 代码重构（不新增功能不修复bug）
   - `perf`: 性能优化
   - `test`: 测试用例修改
   - `chore`: 构建/工具链相关修改
2. 添加影响的scope（可选，如`user`、`components`、`pagination`）
3. 用中文清晰描述修改内容，不超过50字，结尾不加句号
4. 如果需要添加详细说明，在body部分补充
5. 关闭issue可以在footer添加相关信息

## 输出示例
```
feat(user): 添加用户登录验证码功能

fix(components): 修复表格多选状态不更新问题

refactor: 重构商品列表逻辑抽离到组合式函数
```

## 检查要点
- ✅ type符合Conventional Commits定义
- ✅ 描述清晰简洁，不超过50字，结尾无句号
- ✅ 中文描述，方便团队理解
- ✅ 提交前已经通过ESLint检查和单元测试
</content>