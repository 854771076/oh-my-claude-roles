---
name: 企业级提示词版本与权限管理规范
description: 提示词资产化管理规范，包含版本管控、环境隔离、权限管理要求
triggers:
  - pattern: 提示词.*版本管理
  - pattern: 提示词.*权限管理
  - pattern: 提示词.*环境隔离
  - pattern: 提示词资产.*管理
---

# 企业级提示词版本与权限管理规范

所有提示词为企业核心数字资产，必须纳入与代码一致的版本、权限管理体系，禁止散落在个人文档、聊天记录、业务代码中。

## 版本管理强制规范

1. **存储规范**：所有提示词必须统一存放于独立的Git仓库，按业务模块分子目录管理，禁止硬编码在业务代码中，禁止散落在多个仓库

```
# 推荐目录结构
prompts/
├── code-generation/
│   ├── generate-prisma-model/
│   │   �── index.prompt.ts
│   │   �── schema.ts
│   │   �── prompt.md
│   │   └── test/
│   │       └── generate-prisma-model.test.ts
│   └── ...
├── rag/
├── agent/
└── compliance/
```

2. **文件规范**：提示词必须以独立的配置文件形式存放，推荐使用 `.prompt.ts`格式封装LangChain PromptTemplate，配套对应的Zod Schema文件，禁止使用纯文本文件

```typescript
// index.prompt.ts 示例
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { GeneratePrismaModelInputSchema } from "./schema";

export const generatePrismaModelPrompt = ChatPromptTemplate.fromMessages([
  ["system", `
# 1. 角色定位
你是企业级TypeScript+Next.js全栈开发工程师...
// 完整提示词内容
`],
  ["user", `业务需求: {businessDemand}\n表名: {tableName}`],
]);
```

3. **版本号规范**：必须遵循语义化版本规则 `主版本号.次版本号.补丁版本号`：
   - 主版本号：不兼容的架构变更、核心规则变更、业务目标变更
   - 次版本号：功能新增、规则优化、示例补充，向下兼容
   - 补丁版本号：bug修复、文案优化、约束补充，向下兼容

4. **变更管理规范**：
   - 每次变更必须提交Git，提交信息必须遵循Conventional Commits规范，明确变更内容、变更原因
   - 每次变更必须附带完整的测试报告，验证变更后的效果、合规性、稳定性，测试不通过禁止合并
   - 变更必须经过Code Review，至少1名AI提示词工程师与1名业务负责人审批通过，方可合并
   - 每个生产环境上线的版本必须打Git Tag，关联对应的测试报告、上线审批记录，永久归档

5. **回滚机制**：必须建立快速回滚机制，线上出现异常时，可立即回滚至上一个稳定版本，禁止无回滚方案的变更上线