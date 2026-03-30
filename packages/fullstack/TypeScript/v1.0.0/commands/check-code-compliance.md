---
name: check-code-compliance
description: 检查当前项目代码是否符合企业级开发规范
trigger: check-code-compliance
allowed-tools: Read, Grep, Glob, Bash
---

# 检查当前项目代码，验证是否符合 TypeScript + Next.js 企业级开发规范

执行步骤：
1. 全局扫描项目代码：
   - 检查是否存在 JavaScript 文件，确保全项目 TS 覆盖
   - 检查是否存在 any 类型使用，确保用 unknown 替代
   - 检查是否存在非法 // @ts-ignore，替换为 // @ts-expect-error
   - 验证类型/接口命名是否符合规范，接口没有 I 前缀
2. 检查技术栈使用：
   - 确认使用 Next.js 15+ App Router，没有新建 Pages Router 页面
   - 确认服务端组件默认使用，仅必要场景添加 'use client'
   - 确认数据请求：服务端直接查询，客户端使用 TanStack Query v5
   - 确认类型校验统一使用 Zod，表单使用 React Hook Form
   - 确认客户端状态使用 Zustand，认证使用 Auth.js v5，ORM 使用 Prisma 5+
3. 检查命名规范：
   - 组件文件 PascalCase，工具/钩子 camelCase，API 路由 kebab-case
   - 布尔变量以 is/has/should 开头，自定义 Hook 以 use 开头
4. 检查工程化配置：
   - ESLint、Prettier、Husky 配置正确
   - 测试文件符合规范，核心业务覆盖率达标
   - 环境变量前缀规则正确，服务端密钥没有暴露到客户端
5. 输出检查报告，列出所有不符合规范的问题，并提供修复建议

检查要点：
- 严格按照文档规则逐一检查，不遗漏任何规则
- 区分强制规则和建议，明确指出违反强制规则的问题必须修复
- 所有不符合规范的代码给出具体修复方案
```

---