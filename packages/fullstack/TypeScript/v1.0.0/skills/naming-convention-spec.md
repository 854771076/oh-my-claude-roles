---
name: 企业级命名规范
description: 统一文件、目录、变量、函数、数据库、API的命名规则，提升代码可读性和可维护性
triggers:
  - pattern: .*命名规范.*
  - pattern: 文件目录.*命名.*规则
  - pattern: 变量函数.*命名.*规范
---

# 企业级命名规范

## 核心原则
统一命名风格，减少认知负担，通过命名即可快速识别资源类型

---

## 1. 文件与目录命名

| 资源类型                | 命名规则          | 示例                     |
| ----------------------- | ----------------- | ------------------------ |
| 组件文件                | `PascalCase.tsx`  | `UserProfile.tsx`        |
| 工具函数/自定义Hook文件 | `camelCase.ts`    | `useAuth.ts`、`formatDate.ts` |
| API路由/Server Actions  | `kebab-case.ts`   | `route.ts`、`submit-order.ts` |
| 类型定义文件            | `PascalCase.ts`   | `User.ts`                |
| 测试文件                | 源文件名加后缀    | `UserProfile.test.tsx`、`formatDate.spec.ts` |
| 目录                    | 全小写连字符分隔  | `user-profile/`、`api/`  |

---

## 2. 变量与函数命名

| 资源类型                | 命名规则          | 示例                     |
| ----------------------- | ----------------- | ------------------------ |
| 变量、普通函数          | `camelCase`       | `userName`、`getUserById` |
| 常量                    | `UPPER_SNAKE_CASE`| `MAX_RETRY_COUNT`、`API_BASE_URL` |
| React组件               | `PascalCase`      | `UserProfile`            |
| 自定义Hook              | 必须以`use`开头   | `useAuth`、`useCart`     |
| 布尔值变量              | 必须以`is/has/should`前缀开头 | `isLoading`、`hasPermission`、`shouldSubmit` |
| 模块内私有变量/函数      | 加下划线前缀      | `_internalHelper`        |

---

## 3. 数据库与API命名

| 资源类型                | 命名规则          | 示例                     |
| ----------------------- | ----------------- | ------------------------ |
| Prisma模型              | `PascalCase`      | `User`、`Order`          |
| Prisma字段              | `camelCase`       | `userName`、`createdAt`  |
| API路由路径             | `kebab-case`      | `/api/users/[userId]/orders` |
| URL参数                 | `camelCase`       | `userId`、`orderId`      |

---

## 常见错误示例

❌ 错误：组件文件用小驼峰 `userProfile.tsx`  
✅ 正确：`UserProfile.tsx`

❌ 错误：自定义Hook不用use前缀 `auth.ts`  
✅ 正确：`useAuth.ts`

❌ 错误：布尔变量不用前缀 `loading = true`  
✅ 正确：`isLoading = true`

❌ 错误：API路由用大驼峰 `submitOrder.ts`  
✅ 正确：`submit-order.ts`

❌ 错误：目录用大驼峰 `UserProfile/`  
✅ 正确：`user-profile/`

---