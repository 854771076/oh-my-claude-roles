---
name: init-ts-next-project
description: 按照企业级规范初始化 TypeScript + Next.js 全栈项目
trigger: init-ts-next-project
argument-hint: "[project-name]"
allowed-tools: Bash, Write, Read
---

# 初始化符合规范的 TypeScript + Next.js 项目

请根据 TypeScript + Next.js 企业级开发规范，初始化一个全新的项目。参数为：
$ARGUMENTS

执行步骤：
1. 使用 pnpm 初始化 Next.js 15+ 项目，启用 TypeScript 严格模式，配置 App Router
2. 按照规范配置技术栈：
   - 安装依赖：Prisma、TanStack Query v5、Auth.js v5、Zod、Zustand、React Hook Form、shadcn/ui + Tailwind CSS v4
   - 配置工程化：ESLint + @typescript-eslint、Prettier、Husky + lint-staged、Vitest + React Testing Library、Playwright、Pino + nextjs-pino、Sentry
3. 生成符合规范的目录结构和命名规则
4. 配置 tsconfig.json 开启所有严格模式选项
5. 创建 .env.example，添加环境变量规范（服务端变量加 SERVER_ 前缀，客户端加 NEXT_PUBLIC_ 前缀），并用 Zod 配置环境变量校验
6. 生成符合规范的 README.md 文档

检查要点：
- 所有依赖版本符合规范要求，使用 pnpm 包管理
- tsconfig.json 严格模式全部开启，禁止 any 类型
- 技术栈完全符合唯一首选要求，没有使用禁止替代方案
- 目录和文件命名符合规范
- 工程化配置完整，包含代码检查和格式化规则正确
```

---