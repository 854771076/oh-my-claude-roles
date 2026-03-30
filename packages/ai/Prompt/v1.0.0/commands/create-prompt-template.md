---
name: create-prompt-template
description: 生成符合企业级规范的新提示词模板文件和配套Schema
trigger: create-prompt-template
argument-hint: "[prompt-name] [business-scene]"
allowed-tools: Write, Grep
---

# 命令内容

根据用户提供的提示词名称和业务场景，生成完整符合企业级规范的提示词模板文件和Zod Schema文件。

提示词名称：$ARGUMENTS

执行步骤：
1. 分析用户提供的业务场景和需求，确认核心目标、输入输出边界
2. 创建 `.prompt.ts` 格式的提示词文件，严格按照8模块结构生成框架
3. 创建配套的 `[prompt-name].schema.ts` 文件，定义输入和输出Zod Schema
4. 自动添加基础安全规则、异常处理规则、约束禁忌模块的标准模板内容
5. 标记需要用户补充填充的内容，输出文件路径和下一步操作指引

检查要点：
- 必须使用LangChain.js ChatPromptTemplate标准封装
- 必须严格遵循8模块固定顺序，无内容模块标注「无特殊要求」
- Schema必须符合企业Zod类型安全规范，可直接导出供业务代码复用
- 必须预填入企业强制要求的基础安全合规规则
- 文件名必须符合企业规范，使用小写连字符命名
```

---