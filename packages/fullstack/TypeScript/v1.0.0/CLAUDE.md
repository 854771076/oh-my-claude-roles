# TypeScript + Next.js 企业级全栈开发规范

**文档版本**: v1.0.0

## 概述

本规范为 TypeScript + Next.js 企业级全栈项目提供统一开发标准，基于2026年最新生态与生产级最佳实践制定，严格遵循「技术栈统一、类型安全优先、生产环境验证、开发体验优化」原则，所有规则均为强制执行，特殊场景需技术委员会审批后方可调整。

核心原则：能异步都异步、有框架用框架不手写重复代码、强类型安全、可测试、可维护、高性能。

## 开发规范

### 核心要求
- 全项目 TypeScript 覆盖，零 JavaScript 文件
- 强制开启严格模式，保证类型安全
- 禁止使用 `any`，必须用 `unknown` 配合类型守卫替代
- 优先使用框架原生能力，不重复造轮子
- 强制遵循技术栈唯一首选制，禁止使用不推荐的替代方案
- 所有写操作必须在服务端完成，禁止客户端直接调用数据库
- 权限控制必须在服务端实现，禁止仅在客户端做判断
- 异步任务必须使用队列处理，禁止在请求链路中同步执行
- LLM/智能体逻辑必须全部放在服务端，禁止暴露密钥到客户端
- 核心业务逻辑测试覆盖率必须 ≥ 80%，测试失败禁止合并代码
- 代码合并必须经过 Code Review，禁止直接推送到主分支

### TypeScript 书写规范
- 强制开启 tsconfig.json 严格模式：
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
- 禁止非必要的类型断言，优先使用类型守卫或 Zod 运行时校验
- 禁止使用 `// @ts-ignore`，必须用 `// @ts-expect-error` 并添加注释说明原因
- 类型/接口使用 PascalCase 命名，接口禁止加 `I` 前缀
- 优先使用 `type` 定义联合类型、交叉类型、工具类型，`interface` 仅用于对象类型且需要扩展的场景
- 函数参数与返回值必须显式定义类型，禁止依赖类型推导（箭头函数简短场景除外）
- 复杂类型必须添加注释说明用途
- 禁止重复定义类型，公共类型统一放在 `types/` 目录
- 与 Prisma、Zod 集成时，优先使用 `z.infer`、`Prisma.User` 自动生成类型，避免手动重复定义

### Next.js 开发规范
- 强制使用 App Router，禁止新建 Pages Router 页面
- 默认使用服务端组件，仅以下场景必须加 `'use client'` 转为客户端组件：
  - 使用 React Hooks（`useState`、`useEffect`、`useRouter` 等）
  - 使用浏览器 API（`window`、`document`、`localStorage` 等）
  - 使用事件监听（`onClick`、`onChange` 等）
  - 使用 Zustand 等客户端状态管理
- 客户端组件必须最小化，仅将需要交互的部分抽离为客户端组件
- 禁止在服务端组件中导入客户端组件以外的客户端库
- 服务端数据获取：优先使用 Server Components + Prisma 直接查询，写操作通过 Server Actions 处理
- 客户端数据获取：统一使用 TanStack Query，禁止直接使用 `fetch` 或 `axios` 封装
- 服务端环境变量必须以 `SERVER_` 前缀开头，客户端环境变量必须以 `NEXT_PUBLIC_` 前缀开头
- 所有环境变量必须用 Zod/envalid 校验
- 服务端状态由数据库、Next.js 缓存、Auth.js 会话管理，禁止使用客户端状态库
- 客户端全局状态统一使用 Zustand，禁止使用 Context API 做全局状态
- 客户端局部状态使用 React 原生 `useState`、`useReducer`
- URL 状态使用 `useSearchParams`、`useRouter` 同步到 URL
- 所有表单必须使用 React Hook Form + Zod，禁止使用受控组件
- 敏感操作必须加二次确认或 MFA 校验
- 异步任务必须使用 BullMQ，Vercel 环境搭配 Upstash Redis
- 轻量定时任务使用 Vercel Cron Jobs，生产级定时任务使用 BullMQ 重复任务
- 任务执行必须加日志记录和错误追踪

### 测试规范
- 单元/组件/集成测试使用 Vitest + React Testing Library，E2E 测试使用 Playwright
- 测试覆盖范围：核心业务逻辑、工具函数、自定义Hook、复杂组件、核心用户流程
- 组件测试专注于用户行为而非内部实现，禁止测试组件内部状态或方法
- API Mock 统一使用 MSW，禁止修改业务代码做 Mock
- 测试用例必须独立、可重复执行，禁止依赖外部服务或数据库
- CI/CD 必须自动执行所有测试，测试失败禁止合并/部署
- E2E 测试必须使用独立的测试数据库，禁止使用生产或开发数据

### 安全规范
- 所有 API 路由、Server Actions 必须校验 Auth.js 会话，禁止未授权访问
- 数据库操作必须使用 Prisma 参数化查询，禁止 SQL injection
- 禁止非必要使用 `dangerouslySetInnerHTML`，防止 XSS 攻击
- 依赖定期使用 `pnpm audit` 检查安全漏洞，及时升级

## 技术栈

### 核心框架
- 全栈框架：Next.js 15+ (App Router)，禁止使用 Pages Router、纯React、Remix 做新开发
- 语言：TypeScript 5.5+ (严格模式)，禁止使用 JavaScript、Flow
- 包管理：pnpm 9+，禁止使用 npm、yarn
- 构建工具：Turbo (Turborepo)（monorepo 场景强制），禁止使用 Nx、Lerna

### 业务开发库
- 日志：Pino + nextjs-pino，禁止使用 Winston、console.log
- 类型校验：Zod，禁止使用 Valibot、Yup、Joi
- 数据请求：TanStack Query (React Query) v5+，禁止使用 SWR、自定义 fetch 封装
- 数据库 ORM：Prisma 5+，禁止使用 Drizzle、TypeORM
- 认证与权限：Auth.js (NextAuth.js) v5，禁止使用 Clerk、Lucia、自建认证
- 表单处理：React Hook Form + @hookform/resolvers (Zod)，禁止使用 Formik、受控组件
- 客户端状态管理：Zustand，禁止使用 Redux Toolkit、Jotai
- UI组件/设计系统：shadcn/ui + Tailwind CSS v4，禁止使用 MUI、Ant Design、Chakra UI
- 队列与异步任务：BullMQ + Upstash Redis，禁止使用 Bee-Queue、自建队列
- 定时任务：Vercel Cron Jobs (轻量) / BullMQ 重复任务 (生产级)，禁止使用 node-cron、agenda
- LLM/智能体：LangChain TS + LangGraph TS，禁止自建 LLM 编排

### 工程化与测试
- 代码检查：ESLint + @typescript-eslint，禁止使用 TSLint
- 代码格式化：Prettier
- Git Hooks：Husky + lint-staged
- 单元/组件/集成测试：Vitest + React Testing Library，禁止使用 Jest
- E2E 端到端测试：Playwright，禁止使用 Cypress
- 错误追踪：Sentry

## 代码风格

### 命名规范

#### 文件与目录命名
- 组件文件：`PascalCase.tsx`（如 `UserProfile.tsx`）
- 工具函数/钩子文件：`camelCase.ts`（如 `useAuth.ts`、`formatDate.ts`）
- API 路由/Server Actions：`kebab-case.ts`（如 `route.ts`、`submit-order.ts`）
- 类型定义文件：`PascalCase.ts`（如 `User.ts`）
- 测试文件：与源文件同名，加 `.test.ts`/`.spec.tsx` 后缀（如 `UserProfile.test.tsx`）
- 目录命名：全小写，用连字符分隔（如 `user-profile/`、`api/`）

#### 变量与函数命名
- 变量、普通函数：`camelCase`（如 `userName`、`getUserById`）
- 常量：`UPPER_SNAKE_CASE`（如 `MAX_RETRY_COUNT`、`API_BASE_URL`）
- React 组件：`PascalCase`（如 `UserProfile`）
- 自定义 Hook：必须以 `use` 开头（如 `useAuth`、`useCart`）
- 布尔值变量：必须以 `is`/`has`/`should` 等前缀开头（如 `isLoading`、`hasPermission`）
- 私有变量/函数（仅模块内部使用）：加下划线前缀（如 `_internalHelper`）

#### 数据库与API命名
- Prisma 模型：`PascalCase`（如 `User`、`Order`）
- Prisma 字段：`camelCase`（如 `userName`、`createdAt`）
- API 路由路径：`kebab-case`（如 `/api/users/[userId]/orders`）
- URL 参数：`camelCase`（如 `userId`、`orderId`）

### 格式与注释
- 统一使用 Prettier 做代码格式化
- 复杂类型、业务逻辑必须添加注释说明用途
- 公共 API 必须添加注释说明输入输出

## 项目结构

约定以下目录结构：
```
/
├── app/                # Next.js App Router 路由目录
│   ├── api/            # API 路由
│   └── [route]/        # 页面路由
├── components/         # 通用组件
│   ├── ui/             # shadcn/ui 基础组件
│   └── [feature]/      # 业务组件
├── lib/                # 工具库、客户端初始化代码
├── server/             # 服务端代码
│   ├── actions/        # Server Actions
│   ├── queues/         # BullMQ 队列定义
│   └── auth.ts         # Auth.js 配置
├── hooks/              # 自定义 React Hooks
├── store/              # Zustand store 定义
├── types/              # 公共类型定义
├── utils/              # 工具函数
├── prisma/             # Prisma schema 与迁移
├── public/             # 静态资源
├── tests/              # 测试工具、测试数据
└── e2e/                # Playwright E2E 测试
```

- 公共类型统一放在 `types/` 目录，通过 `@/types/*` 导入
- 测试文件与源文件同目录，或统一放在 `__tests__` 目录
- E2E 测试统一放在 `e2e/` 目录
- 环境变量：仅允许提交 `.env.example` 到 Git，禁止提交 `.env` 文件

## 工作流程

### 分支管理
- `main`：主分支，对应生产环境
- `develop`：开发分支
- `feature/*`：功能开发分支
- `hotfix/*`：紧急修复分支

### 代码提交
- 必须遵循 Conventional Commits 规范（如 `feat: add user login`、`fix: resolve order payment bug`）
- 提交前必须通过 Husky + lint-staged 检查，保证 ESLint/Prettier 合规

### 代码合并要求
1. 本地测试通过
2. ESLint/Prettier 检查通过
3. CI/CD 自动化测试通过
4. 至少 1 名同事 Code Review 批准

### 环境与部署
- 强制使用三个环境：`development`（本地开发）、`staging`（预发布）、`production`（生产）
- 不同环境资源必须隔离，禁止共用 API 密钥、数据库
- 强制使用 Vercel 作为部署平台，禁止自建服务器除非特殊审批
- 优先使用 Edge Runtime 部署轻量 API 路由和中间件
- 错误追踪使用 Sentry，日志使用 Pino 结构化输出，性能监控使用 Vercel Analytics
- 部署前必须校验环境变量完整性，避免线上故障

### 文档维护
- 项目 README 必须包含：技术栈说明、本地开发步骤、环境变量配置、部署流程
- 复杂业务逻辑、API 接口必须添加注释或文档
- 定期更新规范文档，确保与实际开发一致

---

## 组件索引

本角色包包含以下附加组件，已自动安装：

### Hooks (钩子脚本)

- `.claude/hooks/TypeScript.json` - TypeScript 开发规范自动检查钩子
- `.claude/hooks/setup-init-check.json` - 项目初始化环境检查钩子
- `.claude/hooks/pre-write-check-ts.json` - 代码写入前 TypeScript 合规检查钩子
- `.claude/hooks/pre-write-check-pages-router.json` - 禁止新建 Pages Router 页面检查钩子
- `.claude/hooks/post-write-lint-check.json` - 代码写入后 ESLint/Prettier 检查钩子
- `.claude/hooks/pre-commit-check.json` - 提交前合规检查钩子
- `.claude/hooks/final-stop-check.json` - 开发完成后合规性总检查钩子
- `.claude/hooks/pre-compact-reminder.json` - 压缩前规范提醒钩子

### Commands (斜杠命令)

- `.claude/commands/TypeScript.md` - TypeScript 开发规范查询命令
- `.claude/commands/init-ts-next-project.md` - 初始化符合规范的 TypeScript Next.js 项目命令
- `.claude/commands/check-code-compliance.md` - 检查当前代码是否符合规范命令
- `.claude/commands/develop-new-feature.md` - 新功能开发流程引导命令
- `.claude/commands/code-review-compliance.md` - 代码合规性评审命令

### Agents (子代理)

- `.claude/agents/typescript-nextjs-enterprise-dev.md` - TypeScript + Next.js 企业级全栈开发子代理

### Rules (规则文件)

- `.claude/rules/typescript-nextjs-enterprise-fullstack-dev-spec.md` - 企业级全栈开发核心规则

### Skills (技能模块)

- `.claude/skills/typescript-nextjs-enterprise-dev/SKILL.md` - TypeScript + Next.js 企业级开发技能入口
- `.claude/skills/typescript-nextjs-enterprise-dev/reference.md` - 开发规范参考文档
- `.claude/skills/TypeScript.md` - TypeScript 基础开发技能
```