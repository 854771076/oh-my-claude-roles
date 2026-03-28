---
name: 创建规范LLM功能
description: 根据规范创建LangChain + LangGraph LLM功能
trigger: /add-llm-function
---

# 创建规范LLM功能

根据规范创建企业级LLM/智能体功能，执行以下步骤：

1. **代码位置**
   - 所有LLM逻辑必须放在服务端（Server Components/Server Actions/API路由）
   - 禁止在客户端初始化LangChain/LangGraph或存储API密钥

2. **配置管理**
   - LLM API密钥、模型配置必须放在服务端环境变量（前缀`SERVER_`）
   - 禁止暴露到客户端

3. **结构化输出定义**
   - 工具调用、模型输出必须使用Zod定义Schema
   - 使用`z.infer`自动推导TS类型，一套Schema覆盖类型和运行时校验

4. **LangGraph配置**
   - 必须启用Checkpointer，使用Upstash Redis/PostgreSQL做状态持久化
   - 支持中断恢复、人在回路能力

5. **流式响应**
   - 对话场景必须使用流式响应，配合Vercel AI SDK实现打字机效果
   - 降低用户等待感知

6. **限流与保护**
   - 添加调用超时、失败重试配置
   - 添加调用次数限流，避免成本失控
   - 所有调用添加日志记录和错误追踪

## 检查要点
- ✅ 所有LLM逻辑都在服务端，未暴露敏感配置到客户端
- ✅ 使用Zod定义Schema，自动推导类型，无重复类型定义
- ✅ LangGraph已启用Checkpointer状态持久化
- ✅ 对话场景已实现流式响应
- ✅ 已添加超时、重试、限流保护
- ✅ 日志和错误追踪已配置