---
name: 创建规范Server Action
description: 根据规范创建符合要求的Next.js Server Action
trigger: /create-server-action
---

# 创建规范Server Action

根据规范创建Next.js服务端操作，执行以下步骤：

1. **文件命名与路径**
   - 文件命名使用kebab-case命名，后缀为`.ts`
   - 统一放在`actions/`目录或对应业务模块目录

2. **权限校验**
   - 必须先校验Auth.js v5会话，获取当前用户信息
   - 必须判断用户是否有对应操作权限，禁止未授权操作
   - 权限校验必须在服务端完成，禁止仅依赖客户端判断

3. **类型与参数校验**
   - 所有输入参数必须定义类型，使用Zod Schema做运行时校验
   - 返回结果必须显式定义类型，统一返回格式：`{ success: boolean; data?: T; error?: string }`

4. **异步与错误处理**
   - 强制使用async异步声明，符合"能异步都异步"原则
   - 使用Pino记录操作日志，错误自动上报Sentry
   - 数据库操作必须使用Prisma，禁止手写SQL避免注入

5. **异步任务处理**
   - 耗时操作（邮件、文件处理、第三方调用）必须放入BullMQ队列，禁止同步执行
   - 任务必须添加日志记录和错误追踪

## 检查要点
- ✅ 文件命名符合kebab-case规则
- ✅ 已做Auth.js会话校验与权限判断
- ✅ 输入参数使用Zod校验，类型安全
- ✅ 耗时操作已放入BullMQ队列
- ✅ 错误处理与日志记录已添加
- ✅ 未在Server Action中暴露敏感信息

---