---
name: Next.js 企业级技术栈选型规范
description: 定义TypeScript + Next.js全栈项目的强制技术栈选型，遵循唯一首选制，确保生态统一、生产级稳定
triggers:
  - pattern: .*技术栈.*选型.*Next\.js.*
  - pattern: 选什么技术栈.*Next.*TS
  - pattern: 企业级.*技术栈.*推荐
---

# Next.js 企业级技术栈选型规范

## 核心原则
技术栈采用**唯一首选制**，所有规则强制执行，特殊场景需技术委员会审批后方可调整，遵循：
- 技术栈统一、类型安全优先
- 生产环境验证、开发体验优化
- 能异步都异步、有框架用框架不手写重复代码
- 强类型安全、可测试、可维护、高性能

---

## 核心框架选型

| 方向     | 唯一首选技术栈             | 禁止/不推荐替代方案          | 说明                                                   |
| -------- | -------------------------- | ---------------------------- | ------------------------------------------------------ |
| 全栈框架 | Next.js 15+ (App Router)   | Pages Router、纯React、Remix | 强制使用App Router，Pages Router仅用于历史遗留项目迁移 |
| 语言     | TypeScript 5.5+ (严格模式) | JavaScript、Flow             | 全项目TS覆盖，零JS文件                                 |
| 包管理   | pnpm 9+                    | npm、yarn                    | monorepo场景强制Turbo + pnpm                           |
| 构建工具 | Turbo (Turborepo)          | Nx、Lerna                    | monorepo架构唯一首选，单项目可省略                     |

---

## 业务开发库选型

| 方向            | 唯一首选技术栈                                    | 禁止/不推荐替代方案        | 说明                                        |
| --------------- | ------------------------------------------------- | -------------------------- | ------------------------------------------- |
| 日志            | Pino + nextjs-pino                                | Winston、console.log       | 生产环境结构化日志唯一方案                  |
| 类型校验        | Zod                                               | Valibot、Yup、Joi          | 全链路类型安全基石，一套Schema覆盖TS+运行时 |
| 数据请求        | TanStack Query (React Query) v5+                  | SWR、fetch封装             | 全栈数据请求与缓存管理标准                  |
| 数据库ORM       | Prisma 5+                                         | Drizzle、TypeORM           | 类型安全数据库操作首选                      |
| 认证与权限      | Auth.js (NextAuth.js) v5                          | Clerk、Lucia、自建认证     | 官方推荐，无供应商锁定                      |
| 表单处理        | React Hook Form + @hookform/resolvers (Zod)       | Formik、受控组件           | 性能最优，类型安全                          |
| 客户端状态管理  | Zustand                                           | Redux Toolkit、Jotai       | 极简API，零样板代码                         |
| UI组件/设计系统 | shadcn/ui + Tailwind CSS v4                       | MUI、Ant Design、Chakra UI | 100%可定制，服务端组件友好                  |
| 队列与异步任务  | BullMQ + Upstash Redis                            | Bee-Queue、自建队列        | 生产级队列唯一方案                          |
| 定时任务        | Vercel Cron Jobs (轻量) / BullMQ重复任务 (生产级) | node-cron、agenda          | Vercel环境优先官方Cron Jobs                 |
| LLM/智能体      | LangChain TS + LangGraph TS                       | 自建LLM编排                | 类型安全的AI应用开发标准                    |

---

## 工程化与测试选型

| 方向               | 唯一首选技术栈                 | 禁止/不推荐替代方案 | 说明                     |
| ------------------ | ------------------------------ | ------------------- | ------------------------ |
| 代码检查           | ESLint + @typescript-eslint    | TSLint              | TS官方推荐               |
| 代码格式化         | Prettier                       | 无                  | 统一团队代码风格         |
| Git Hooks          | Husky + lint-staged            | 无                  | 提交前强制检查与格式化   |
| 单元/组件/集成测试 | Vitest + React Testing Library | Jest                | 速度快5-10倍，TS原生支持 |
| E2E端到端测试      | Playwright                     | Cypress             | 跨浏览器、稳定、TS原生   |
| 错误追踪           | Sentry                         | 自建监控            | 全栈错误追踪行业标准     |

---

## 使用示例
> 新建项目初始化技术栈：
```bash
pnpm create next-app@latest --typescript --eslint --tailwind --app
pnpm add @prisma/client zod @tanstack/react-query next-auth@beta react-hook-form @hookform/resolvers zustand
pnpm add -D prisma pino nextjs-pino vitest @testing-library/react @playwright/test msw @faker-js/faker husky lint-staged
```

---