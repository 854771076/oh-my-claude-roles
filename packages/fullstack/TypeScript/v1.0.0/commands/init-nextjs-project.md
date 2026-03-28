---
name: 初始化Next.js企业级项目
description: 根据规范初始化符合要求的TypeScript + Next.js企业级项目结构与配置
trigger: /init-nextjs-project
---

# 初始化Next.js企业级项目

根据TypeScript + Next.js企业级开发规范初始化项目，执行以下步骤：

1. **项目基础初始化**
   - 使用pnpm创建Next.js 15+项目，启用TypeScript严格模式
   - 配置tsconfig.json，确保开启所有严格模式选项：`strict: true`、`noImplicitAny`、`strictNullChecks`、`noUnusedLocals`、`noUnusedParameters`、`noImplicitReturns`、`noFallthroughCasesInSwitch`

2. **依赖安装**
   - 安装核心依赖：`@prisma/client next-auth@5 @tanstack/react-query zod react-hook-form @hookform/resolvers zustand shadcn-ui tailwindcss pino nextjs-pino`
   - 安装开发依赖：`eslint @typescript-eslint/eslint @typescript-eslint/parser prettier husky lint-staged vitest @testing-library/react @testing-library/jest-dom playwright msw @faker-js/faker sentry`

3. **项目结构创建**
   - 创建标准目录结构：`app/`(App Router路由)、`components/`(公共组件)、`lib/`(工具库)、`types/`(公共类型)、`hooks/`(自定义Hook)、`actions/`(Server Actions)、`prisma/`(Prisma配置)、`queues/`(BullMQ任务)、`e2e/`(Playwright E2E测试)

4. **规范配置校验**
   - 配置ESLint + Prettier
   - 配置Husky + lint-staged提交钩子
   - 配置Vitest + React Testing Library
   - 配置Playwright E2E测试
   - 配置环境变量示例文件`.env.example`，要求服务端变量加`SERVER_`前缀，客户端变量加`NEXT_PUBLIC_`前缀，使用Zod做环境变量校验

## 检查要点
- ✅ 使用Next.js 15+ App Router，未引入Pages Router
- ✅ TypeScript严格模式已开启，无隐含any
- ✅ 技术栈符合规范要求，未使用禁止依赖
- ✅ 目录命名符合全小写+连字符规则
- ✅ 环境变量前缀规则已落实

---