---
name: 创建规范API路由
description: 根据规范创建Next.js App Router API路由
trigger: /create-api-route
---

# 创建规范API路由

根据规范创建Next.js App Router API路由，执行以下步骤：

1. **路由路径与文件命名**
   - 路由路径使用kebab-case命名，参数使用camelCase
   - 文件名为`route.ts`，符合App Router规范

2. **运行时选择**
   - 轻量API优先使用Edge Runtime降低冷启动时间
   - 添加`export const runtime = 'edge';`声明

3. **权限与会话校验**
   - 必须校验Auth.js v5会话，获取当前登录用户
   - 必须做权限判断，禁止未授权访问
   - 禁止仅在客户端做权限控制

4. **类型与参数校验**
   - 请求参数（路径参数、查询参数、请求体）必须使用Zod Schema校验
   - 响应类型必须显式定义，确保返回类型安全

5. **错误与日志处理**
   - 使用Pino记录请求与错误日志
   - 错误自动捕获并上报Sentry
   - 返回统一格式的错误响应

6. **缓存策略配置**
   - 可缓存公共数据配置合理的`Cache-Control`头，利用Vercel Edge Cache

## 检查要点
- ✅ 路由路径符合kebab-case规范，URL参数符合camelCase
- ✅ 已做Auth.js会话校验和权限判断
- ✅ 请求参数使用Zod做运行时校验
- ✅ 错误处理和日志记录已添加
- ✅ 未在API中直接执行耗时异步任务，已放入BullMQ队列

---