---
name: Next.js App Router 开发规范
description: 定义App Router下服务端/客户端组件分类、数据请求、状态管理的开发规则，充分发挥Next.js性能优势
triggers:
  - pattern: .*App Router.*开发规范.*
  - pattern: Next\.js.*服务端组件.*规则
  - pattern: Next\.js.*数据请求.*规范
---

# Next.js App Router 开发规范

## 核心原则
- 默认使用服务端组件，最小化客户端组件体积
- 服务端优先处理数据读写，客户端只处理交互
- 充分利用框架原生缓存，避免重复请求

---

## 1. 组件分类规范
- **强制使用App Router**，禁止新建Pages Router页面
- 默认使用**服务端组件**，仅以下场景必须加`'use client'`转为客户端组件：
  1. 使用React Hooks（`useState`、`useEffect`、`useRouter`等）
  2. 使用浏览器API（`window`、`document`、`localStorage`等）
  3. 使用事件监听（`onClick`、`onChange`等）
  4. 使用Zustand等客户端状态管理
- **客户端组件必须最小化**，仅将需要交互的部分抽离为客户端组件，其余逻辑保留在服务端组件
- 禁止在服务端组件中导入客户端组件以外的客户端库

### 正确示例
```tsx
// app/users/[id]/page.tsx - 服务端组件，无需'use client'
import { prisma } from '@/lib/prisma';
import UserProfileEdit from './UserProfileEdit'; // 客户端交互抽离

export default async function UserProfilePage({ params }: { params: { id: string } }) {
  // 服务端直接查询数据库，无需客户端请求
  const user = await prisma.user.findUnique({ where: { id: params.id } });
  
  return (
    <div>
      <h1>{user?.name}</h1>
      {/* 只有编辑交互是客户端组件 */}
      <UserProfileEdit initialData={user} />
    </div>
  );
}
```

```tsx
// app/users/[id]/UserProfileEdit.tsx - 仅交互部分转为客户端
'use client';

import { useState } from 'react';

export default function UserProfileEdit({ initialData }) {
  const [name, setName] = useState(initialData.name);
  
  return (
    <button onClick={() => setName('New Name')}>
      Edit Name
    </button>
  );
}
```

---

## 2. 数据请求规范
1. **服务端数据获取**：优先使用`Server Components + Prisma`直接查询数据库，写操作通过`Server Actions`处理
2. **客户端数据获取**：统一使用TanStack Query，禁止直接使用`fetch`或`axios`封装
3. **缓存策略**：
   - 服务端组件：利用Next.js原生`fetch`缓存，通过`cache: 'force-cache'`/`revalidate`控制
   - 客户端：利用TanStack Query缓存，合理设置`staleTime`、`gcTime`
4. **环境变量规范**：
   - 服务端环境变量：必须以`SERVER_`前缀开头，仅服务端可访问
   - 客户端环境变量：必须以`NEXT_PUBLIC_`前缀开头，会暴露到浏览器
   - 所有环境变量必须用Zod校验，提前捕获缺失问题

---

## 3. 状态管理规范
- **服务端状态**：由数据库、Next.js缓存、Auth.js会话管理，禁止使用客户端状态库
- **客户端全局状态**：统一使用Zustand，禁止使用Context API做全局状态（避免不必要重渲染）
- **客户端局部状态**：使用React原生`useState`、`useReducer`
- **URL状态**：使用`useSearchParams`、`useRouter`同步到URL，避免刷新丢失

---

## 4. 表单与认证规范
- 所有表单必须使用`React Hook Form + Zod`，禁止使用受控组件
- 服务端写操作必须通过`Server Actions`实现，禁止直接在客户端调用数据库或API
- 认证统一使用`Auth.js v5`，权限控制必须在服务端实现（Server Actions/API路由中校验会话），禁止仅在客户端做权限判断
- 敏感操作（如删除、支付）必须加二次确认或MFA校验

---

## 5. 异步任务与定时任务规范
- 异步任务（邮件发送、文件处理、第三方API调用）必须使用`BullMQ`，禁止在请求链路中同步执行
- Vercel部署环境：BullMQ必须搭配`Upstash Redis`作为存储
- 轻量级定时任务：使用`Vercel Cron Jobs`，在`vercel.json`中配置
- 生产级定时任务（高可靠、失败重试）：使用`BullMQ重复任务`
- 任务执行必须加Pino日志记录和Sentry错误追踪

---

## 6. LLM/智能体开发规范
- LangChain/LangGraph逻辑必须全部放在服务端（Server Components/Server Actions/API路由），禁止在客户端初始化或执行
- API密钥、模型配置必须通过服务端环境变量管理，禁止暴露到客户端
- 工具调用、结构化输出必须使用Zod定义Schema，一套Schema同时覆盖TS类型和LLM格式
- LangGraph必须启用`Checkpointer`（Upstash Redis/PostgreSQL）做状态持久化，支持中断恢复、人在回路
- 对话场景必须使用流式响应，配合V