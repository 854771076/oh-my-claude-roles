---
name: typescript-nextjs-enterprise-dev
description: TypeScript + Next.js 企业级全栈开发规范，强制执行技术栈统一、类型安全、生产级最佳实践。创建新项目、开发功能、代码评审时使用。
user-invocable: true
allowed-tools: Read, Grep, Bash(npm:*, pnpm:*, git:*)
---

# TypeScript + Next.js 企业级全栈开发规范

**版本**: v1.0.0  
**适用范围**: TS企业级全栈项目  
**核心原则**: 能异步都异步、有框架用框架不手写重复代码、强类型安全、可测试、可维护、高性能

本规范基于2026年最新生态与生产级最佳实践，严格遵循「技术栈统一、类型安全优先、生产环境验证、开发体验优化」原则，所有规则均为**强制执行**，特殊场景需技术委员会审批后方可调整。

---

## 一、技术栈限制（唯一首选制）

### 1.1 核心框架

| 方向     | 唯一首选技术栈             | 禁止/不推荐替代方案          | 说明                                                   |
| -------- | -------------------------- | ---------------------------- | ------------------------------------------------------ |
| 全栈框架 | Next.js 15+ (App Router)   | Pages Router、纯React、Remix | 强制使用App Router，Pages Router仅用于历史遗留项目迁移 |
| 语言     | TypeScript 5.5+ (严格模式) | JavaScript、Flow             | 全项目TS覆盖，零JS文件                                 |
| 包管理   | pnpm 9+                    | npm、yarn                    | monorepo场景强制Turbo + pnpm                           |
| 构建工具 | Turbo (Turborepo)          | Nx、Lerna                    | monorepo架构唯一首选，单项目可省略                     |

### 1.2 业务开发库

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

### 1.3 工程化与测试

| 方向               | 唯一首选技术栈                 | 禁止/不推荐替代方案 | 说明                     |
| ------------------ | ------------------------------ | ------------------- | ------------------------ |
| 代码检查           | ESLint + @typescript-eslint    | TSLint              | TS官方推荐               |
| 代码格式化         | Prettier                       | 无                  | 统一团队代码风格         |
| Git Hooks          | Husky + lint-staged            | 无                  | 提交前强制检查与格式化   |
| 单元/组件/集成测试 | Vitest + React Testing Library | Jest                | 速度快5-10倍，TS原生支持 |
| E2E端到端测试      | Playwright                     | Cypress             | 跨浏览器、稳定、TS原生   |
| 错误追踪           | Sentry                         | 自建监控            | 全栈错误追踪行业标准     |

---

## 二、TypeScript 书写规范

### 2.1 基础配置

- 强制开启 `tsconfig.json` 严格模式：
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "noImplicitAny": true,
      "strictNullChecks": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noImplicitReturns": true,
      "noFallthroughCasesInSwitch": true
    }
  }
  ```
- 禁止使用 `any` 类型，必须用 `unknown` 替代，配合类型守卫使用
- 禁止非必要的类型断言（`as`），优先使用类型守卫或Zod运行时校验
- 禁止使用 `// @ts-ignore`，必须用 `// @ts-expect-error` 并添加注释说明原因

### 2.2 类型定义规范

- 类型/接口使用 `PascalCase` 命名，接口禁止加 `I` 前缀（如 `User` 而非 `IUser`）
- 优先使用 `type` 定义联合类型、交叉类型、工具类型，`interface` 仅用于对象类型且需要扩展的场景
- 函数参数与返回值必须显式定义类型，禁止依赖类型推导（箭头函数简短场景除外）
- 复杂类型必须添加注释说明用途
- 禁止重复定义类型，公共类型统一放在 `types/` 目录下，通过 `@/types/*` 导入
- 与Prisma、Zod集成时，优先使用 `z.infer`、`Prisma.User` 自动生成类型，避免手动重复定义

---

## 三、命名规范

### 3.1 文件与目录命名

- 组件文件：`PascalCase.tsx`（如 `UserProfile.tsx`）
- 工具函数/钩子文件：`camelCase.ts`（如 `useAuth.ts`、`formatDate.ts`）
- API路由/Server Actions：`kebab-case.ts`（如 `route.ts`、`submit-order.ts`）
- 类型定义文件：`PascalCase.ts`（如 `User.ts`）
- 测试文件：与源文件同名，加 `.test.ts`/`.spec.tsx` 后缀（如 `UserProfile.test.tsx`）
- 目录命名：全小写，用连字符分隔（如 `user-profile/`、`api/`）

### 3.2 变量与函数命名

- 变量、普通函数：`camelCase`（如 `userName`、`getUserById`）
- 常量：`UPPER_SNAKE_CASE`（如 `MAX_RETRY_COUNT`、`API_BASE_URL`）
- React组件：`PascalCase`（如 `UserProfile`）
- 自定义Hook：必须以 `use` 开头（如 `useAuth`、`useCart`）
- 布尔值变量：必须以 `is`/`has`/`should` 等前缀开头（如 `isLoading`、`hasPermission`）
- 私有变量/函数（仅模块内部使用）：加下划线前缀（如 `_internalHelper`）

### 3.3 数据库与API命名

- Prisma模型：`PascalCase`（如 `User`、`Order`）
- Prisma字段：`camelCase`（如 `userName`、`createdAt`）
- API路由路径：`kebab-case`（如 `/api/users/[userId]/orders`）
- URL参数：`camelCase`（如 `userId`、`orderId`）

---

## 四、Next.js 开发规范

### 4.1 App Router 与组件分类

- 强制使用 App Router，禁止新建 Pages Router 页面
- 默认使用**服务端组件**，仅以下场景必须加 `'use client'` 转为客户端组件：
  - 使用 React Hooks（`useState`、`useEffect`、`useRouter` 等）
  - 使用浏览器 API（`window`、`document`、`localStorage` 等）
  - 使用事件监听（`onClick`、`onChange` 等）
  - 使用 Zustand 等客户端状态管理
- 客户端组件必须最小化，仅将需要交互的部分抽离为客户端组件，其余逻辑保留在服务端组件
- 禁止在服务端组件中导入客户端组件以外的客户端库（如 `react-dom/client`）

### 4.2 数据请求规范

- 服务端数据获取：优先使用 **Server Components + Prisma** 直接查询数据库，或通过 **Server Actions** 处理写操作
- 客户端数据获取：统一使用 **TanStack Query**，禁止直接使用 `fetch` 或 `axios` 封装
- 数据缓存：
  - 服务端组件：利用 Next.js 原生 `fetch` 缓存（`cache: 'force-cache'`/`revalidate`）
  - 客户端：利用 TanStack Query 缓存策略，合理设置 `staleTime`、`gcTime`
- 环境变量：
  - 服务端环境变量：必须以 `SERVER_` 前缀开头（如 `SERVER_DATABASE_URL`），仅服务端可访问
  - 客户端环境变量：必须以 `NEXT_PUBLIC_` 前缀开头（如 `NEXT_PUBLIC_API_URL`），会暴露到浏览器
  - 所有环境变量必须用 Zod/envalid 校验，提前捕获缺失问题

### 4.3 状态管理规范

- 服务端状态：由数据库、Next.js 缓存、Auth.js 会话管理，禁止使用客户端状态库
- 客户端全局状态：统一使用 **Zustand**，禁止使用 Context API 做全局状态（避免不必要的重渲染）
- 客户端局部状态：使用 React 原生 `useState`、`useReducer`
- URL状态：使用 `useSearchParams`、`useRouter` 同步到URL，避免刷新丢失

### 4.4 表单与认证规范

- 所有表单必须使用 **React Hook Form + Zod**，禁止使用受控组件
- 服务端写操作必须通过 **Server Actions** 实现，禁止直接在客户端调用数据库或API
- 认证统一使用 **Auth.js v5**，权限控制必须在服务端实现（Server Actions/API路由中校验会话），禁止仅在客户端做权限判断
- 敏感操作（如删除、支付）必须加二次确认或MFA校验

### 4.5 队列与定时任务规范

- 异步任务（邮件发送、文件处理、第三方API调用）必须使用 **BullMQ**，禁止在请求链路中同步执行
- Vercel部署环境：BullMQ 必须搭配 **Upstash Redis** 作为存储
- 轻量级定时任务（如每日数据同步）：使用 **Vercel Cron Jobs**，在 `vercel.json` 中配置，触发API路由/Server Actions
- 生产级定时任务（高可靠、失败重试）：使用 **BullMQ 重复任务**
- 任务执行必须加日志记录（Pino）和错误追踪（Sentry）

### 4.6 LLM/智能体开发规范

- LangChain/LangGraph 逻辑**必须全部放在服务端**（Server Components/Server Actions/API路由），禁止在客户端初始化或执行
- API密钥、模型配置必须通过服务端环境变量管理，禁止暴露到客户端
- 工具调用、结构化输出必须使用 **Zod** 定义Schema，一套Schema同时覆盖TS类型和LLM格式
- LangGraph 必须启用 **Checkpointer**（Upstash Redis/PostgreSQL）做状态持久化，支持中断恢复、人在回路
- 对话场景必须使用**流式响应**，配合 Vercel AI SDK 实现打字机效果
- LLM调用必须加超时、重试、限流保护，避免成本失控

---

## 五、测试规范

### 5.1 单元/组件/集成测试（Vitest）

- 测试覆盖范围：核心业务逻辑、工具函数、自定义Hook、复杂组件
- 测试覆盖率要求：核心业务逻辑覆盖率 ≥ 80%，禁止低于此标准合并代码
- 测试文件必须与源文件放在同一目录，或统一放在 `__tests__` 目录下
- 组件测试必须使用 **React Testing Library**，专注于用户行为而非内部实现，禁止测试组件内部状态或方法
- API Mock 统一使用 **MSW**，禁止修改业务代码做Mock
- 测试数据生成使用 **@faker-js/faker**
- 测试用例必须独立、可重复执行，禁止依赖外部服务或数据库
- CI/CD流程中必须自动执行所有测试，测试失败禁止合并代码

### 5.2 E2E端到端测试（Playwright）

- E2E测试覆盖范围：核心用户流程（如登录、下单、支付）、关键业务路径
- E2E测试文件统一放在 `e2e/` 目录下
- 测试环境必须使用独立的测试数据库，禁止使用生产或开发环境数据
- 测试用例必须稳定、可重复执行，避免因网络波动、第三方服务导致的 flaky tests
- CI/CD流程中必须自动执行E2E测试（可仅在主分支执行），测试失败禁止部署
- 定期清理测试数据，避免测试环境数据膨胀

---

## 六、部署与Vercel规范

### 6.1 环境管理

- 强制使用三个环境：`development`（本地开发）、`staging`（预发布）、`production`（生产）
- 环境变量通过 **Vercel Dashboard** 管理，禁止提交 `.env` 文件到Git仓库（`.env.example` 除外）
- 不同环境的环境变量必须隔离，禁止共用API密钥、数据库等资源
- 部署前必须通过 `envalid` 校验环境变量完整性，避免线上故障

### 6.2 Vercel部署配置

- 强制使用 **Vercel** 作为部署平台，禁止自建服务器除非特殊审批
- `vercel.json` 配置必须包含：
  - 构建命令、输出目录
  - 重定向、重写规则
  - Cron Jobs配置（如需要）
  - 缓存策略
- 优先使用 **Edge Runtime** 部署轻量API路由和中间件，降低冷启动时间
- 数据库优先使用托管服务（如Neon PostgreSQL、Upstash Redis），无需自建运维
- 静态资源利用 **Vercel Edge Cache** 缓存，设置合理的 `Cache-Control` 头

### 6.3 监控与日志

- 错误追踪统一使用 **Sentry**，全栈覆盖（前端、服务端、Edge Functions）
- 日志统一使用 **Pino** 结构化输出，通过 **Vercel Log Drain** 对接日志聚合平台（如Datadog、ELK）
- 性能监控使用 **Vercel Analytics** + **Web Vitals**，关注Core Web Vitals指标
- 定期检查Sentry错误、Vercel部署日志，及时发现并修复线上问题

### 6.4 安全规范

- 所有API路由、Server Actions必须校验Auth.js会话，禁止未授权访问
- 数据库操作必须使用Prisma参数化查询，禁止SQL注入
- XSS防护：React自动转义，禁止非必要使用 `dangerouslySetInnerHTML`
- CSRF防护：Auth.js内置CSRF保护，表单提交必须使用 `csrfToken`
- 依赖管理：定期使用 `pnpm audit` 检查安全漏洞，及时升级依赖
- 代码合并必须经过Code Review，禁止直接推送到主分支

---

## 七、工程化与协作规范

- 代码提交必须遵循 **Conventional Commits** 规范（如 `feat: add user login`、`fix: resolve order payment bug`）
- 分支管理：`main`（主分支，对应生产环境）、`develop`（开发分支）、`feature/*`（功能分支）、`hotfix/*`（紧急修复分支）
- 代码合并必须经过：
  1. 本地测试通过
  2. ESLint/Prettier检查通过
  3. CI/CD自动化测试通过
  4. 至少1名同事Code Review批准
- 文档维护：
  - 项目README必须包含：技术栈说明、本地开发步骤、环境变量配置、部署流程
  - 复杂业务逻辑、API接口必须添加注释或文档
  - 定期更新规范文档，确保与实际开发一致