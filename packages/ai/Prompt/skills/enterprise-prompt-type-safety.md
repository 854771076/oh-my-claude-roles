---
name: 企业级提示词类型安全强制规范
description: 与企业TS全栈开发规范对齐，实现提示词全链路类型安全，杜绝类型断层导致的业务故障
triggers:
  - pattern: 提示词.*类型安全
  - pattern: Zod.*提示词.*校验
  - pattern: 结构化.*输出.*提示词
  - pattern: 输入输出.*Schema.*提示词
---

# 企业级提示词类型安全强制规范

与企业TypeScript全栈开发规范完全对齐，实现提示词全链路类型安全，杜绝类型断层导致的业务故障。

## 强制规范要求

1. **输入类型安全**：所有提示词的输入变量必须定义TS类型与Zod校验Schema，输入内容必须先经过Zod校验，校验不通过直接拦截，禁止传入模型

```typescript
// 输入Schema示例
import { z } from "zod";

export const GeneratePrismaModelInputSchema = z.object({
  businessDemand: z.string().max(1000),
  tableName: z.string().regex(/^[a-z0-9_]+$/),
});

export type GeneratePrismaModelInput = z.infer<typeof GeneratePrismaModelInputSchema>;
```

2. **输出类型安全**：所有提示词的输出必须定义Zod Schema，强制使用LangChain结构化输出能力，约束模型严格按照Schema生成内容

```typescript
// 输出Schema示例
export const GeneratePrismaModelOutputSchema = z.object({
  code: z.string(),
  remark: z.string(),
  isComplete: z.boolean(),
});

export type GeneratePrismaModelOutput = z.infer<typeof GeneratePrismaModelOutputSchema>;
```

3. **输出二次校验**：输出内容必须经过Zod二次校验，校验不通过直接触发异常处理流程，禁止将不符合格式的内容传入下游业务系统

```typescript
// 校验流程示例
const structuredLlm = llm.withStructuredOutput(GeneratePrismaModelOutputSchema);
const rawOutput = await structuredLlm.invoke(prompt);
const parsedOutput = GeneratePrismaModelOutputSchema.safeParse(rawOutput);
if (!parsedOutput.success) {
  // 触发异常处理
  return { error: "输出格式非法" };
}
```

4. **类型复用**：Schema定义必须与业务代码复用同一套类型定义，禁止重复定义导致类型不一致

5. **工具调用类型安全**：工具调用场景的提示词，必须与Zod定义的工具入参Schema完全一致，禁止模型调用未授权的工具、传入不符合Schema的参数

## 核心优势

- 一套Schema覆盖TS类型推导、LLM输出约束、运行时校验
- 全链路类型安全，编译时即可发现类型问题
- 杜绝格式异常导致的业务故障，降低线上问题率
- 与企业现有TS技术栈无缝对齐，减少额外学习成本

---