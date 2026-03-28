---
name: 代码规范质量检查
description: 在代码提交前执行完整的规范检查，确保符合企业级开发要求
trigger: /codespeed-check
---

# 代码规范质量检查

执行全流程规范检查，确保代码符合要求，执行以下步骤：

1. **代码风格检查**
   - 运行ESLint检查，修复所有错误与警告
   - 运行Prettier格式化，确保代码风格统一
   - 检查是否存在`any`类型，替换为`unknown`
   - 检查是否存在`// @ts-ignore`，替换为`// @ts-expect-error`并添加说明
   - 检查非必要类型断言，替换为类型守卫或Zod校验

2. **命名规范检查**
   - 检查文件命名：组件PascalCase、工具函数camelCase、API/Server Actions kebab-case
   - 检查变量函数命名：布尔值前缀正确、Hook以use开头、常量大写下划线分隔
   - 检查类型命名：无I前缀，PascalCase，无重复定义
   - 检查Prisma模型与字段命名符合规范

3. **Next.js规范检查**
   - 检查是否新建Pages Router页面，确认所有新页面使用App Router
   - 检查客户端组件是否最小化，非必要未添加`'use client'`
   - 检查服务端组件未直接使用客户端Hooks或浏览器API
   - 检查客户端数据请求统一使用TanStack Query，未手写fetch封装
   - 检查环境变量前缀正确，服务端变量未暴露到客户端
   - 检查所有表单使用React Hook Form + Zod，未使用受控组件
   - 检查LLM相关逻辑全部放在服务端，API密钥未暴露到客户端

4. **安全规范检查**
   - 检查所有API/Server Actions都做了会话校验
   - 检查数据库操作使用Prisma参数化查询，无拼接SQL
   - 检查未不必要使用`dangerouslySetInnerHTML`
   - 运行`pnpm audit`检查依赖安全漏洞

5. **测试检查**
   - 运行单元测试，确保所有测试通过
   - 检查核心业务逻辑覆盖率不低于80%
   - 新功能已添加对应测试用例

## 检查要点
- ✅ ESLint和Prettier检查全部通过
- ✅ 无any、无非法ts-ignore、命名全部符合规范
- ✅ Next.js开发规则全部符合，客户端组件最小化
- ✅ 类型安全落实，Zod校验到位，无重复类型定义
- ✅ 安全规则符合要求
- ✅ 所有测试用例执行通过

---