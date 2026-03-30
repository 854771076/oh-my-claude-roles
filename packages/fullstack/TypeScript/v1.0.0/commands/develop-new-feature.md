---
name: develop-new-feature
description: 按照规范开发新功能
trigger: develop-new-feature
argument-hint: "[feature-description]"
allowed-tools: Read, Write, Grep, Edit
---

# 按照企业级规范开发新功能

需求描述：
$ARGUMENTS

执行步骤：
1. 分析功能需求，确定功能类型（页面、API、异步任务等）
2. 根据规范定义类型：
   - 所有类型优先自动推导，用 Zod 定义运行时 Schema，再通过 z.infer 得到 TS 类型
   - 公共类型放在 @/types 目录，禁止重复定义
   - 所有函数参数和返回值显式声明类型
3. 按照 Next.js 规范创建文件和目录：
   - 默认使用服务端组件，仅交互部分抽离为客户端组件
   - 服务端写操作使用 Server Actions，禁止客户端直接调用数据库
   - 客户端数据获取使用 TanStack Query，合理配置缓存策略
   - 表单必须使用 React Hook Form + Zod 校验
   - 异步任务使用 BullMQ，禁止在请求链路同步执行
4. 开发完成后，编写对应测试：
   - 核心业务逻辑编写单元/集成测试，覆盖率不低于 80%
   - 核心用户流程编写 E2E 测试
5. 本地运行 ESLint 和测试用例，确保全部通过
6. 提交代码遵循 Conventional Commits 规范

检查要点：
- 所有代码强类型安全，没有隐式 any，没有非必要类型断言
- 组件分类正确，客户端组件最小化
- 权限控制在服务端实现，禁止仅在客户端做权限判断
- 数据库操作使用 Prisma 参数化查询，避免安全问题
- 测试用例独立可重复，不依赖外部服务
- 命名和文件结构完全符合规范要求
```

---