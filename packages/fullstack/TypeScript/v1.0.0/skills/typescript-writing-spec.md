---
name: TypeScript 企业级书写规范
description: 定义TypeScript严格模式下的书写规则，确保全项目类型安全，减少运行时错误
triggers:
  - pattern: .*TypeScript.*书写.*规范.*
  - - pattern: .*TS.*类型定义.*规则
  - - pattern: tsconfig.*严格模式.*配置
---

# TypeScript 企业级书写规范

## 核心原则
- 全项目强类型覆盖，禁止隐式类型
- 优先自动生成类型，避免手动重复定义
- 零any，运行时校验用Zod保证类型安全

---

## 基础配置规范
强制开启`tsconfig.json`严格模式：
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

### 基础规则
1. **禁止使用`any`类型**，必须用`unknown`替代，配合类型守卫使用
2. **禁止非必要的类型断言**（`as`），优先使用类型守卫或Zod运行时校验
3. **禁止使用`// @ts-ignore`**，必须用`// @ts-expect-error`并添加注释说明原因

---

## 类型定义规范

### 命名规则
- 类型/接口使用`PascalCase`命名，接口禁止加`I`前缀（如`User`而非`IUser`）

### 类型选择规则
- 优先使用`type`定义联合类型、交叉类型、工具类型
- `interface`仅用于对象类型且需要扩展的场景

### 通用规则
1. 函数参数与返回值必须显式定义类型，禁止依赖类型推导（箭头函数简短场景除外）
2. 复杂类型必须添加注释说明用途
3. 禁止重复定义类型，公共类型统一放在`types/`目录下，通过`@/types/*`导入
4. 与Prisma、Zod集成时，优先使用`z.infer`、`Prisma.User`自动生成类型，避免手动重复定义

---

## 正确示例

```typescript
// 正确：用Zod定义Schema，自动推导TS类型
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2),
  email: z.string().email(),
  age: z.number().int().min(18).optional()
});

export type User = z.infer<typeof UserSchema>;

// 正确：类型守卫替代类型断言
function isUser(value: unknown): value is User {
  return UserSchema.safeParse(value).success;
}

// 正确：显式定义参数和返回值类型
function getUserById(id: string): Promise<User | null> {
  return prisma.user.findUnique({ where: { id } });
}

// 正确：布尔变量前缀规范
const isLoading: boolean = false;
const hasPermission: boolean = true;
```

## 错误示例

```typescript
// 错误：使用any
function getUser(id: any): any { ... }

// 错误：接口加I前缀
interface IUser { ... }

// 错误：手动重复定义类型，Zod已经生成
type User = { id: string; name: string };
const UserSchema = z.object({ ... });

// 错误：@ts-ignore替代@ts-expect-error
// @ts-ignore
const user = value as User;
```

---