---
name: create-new-llm-agent
description: 创建符合规范的LangChain+LangGraph智能体骨架
trigger: create-new-llm-agent
---

按照规范创建一个新的LangGraph智能体，包含完整的目录结构和基础代码。

### 使用方式：
`/create-new-llm-agent 智能体名称`，例如 `create-new-llm-agent customer-service`

### 执行步骤：
1. 创建智能体目录结构：`app/services/llm/{智能体名称}/`
2. 创建提示词目录：`app/services/llm/{智能体名称}/prompts/`，存放所有提示词文件
3. 创建工具目录：`app/services/llm/{智能体名称}/tools/`
4. 生成智能体主文件：`app/services/llm/{智能体名称}/agent.py`，包含：
   - 状态定义（TypedDict）
   - 节点方法骨架
   - StateGraph构建逻辑
   - 异步运行入口
   - 异常处理和日志记录
5. 生成基础工具模板，继承LangChain BaseTool
6. 生成基础测试用例：`tests/integration/llm/test_{智能体名称}.py`

### 检查要点：
- 提示词没有硬编码在代码中，独立管理
- 状态通过StateGraph管理，没有使用全局变量
- 已添加Tenacity重试配置，处理大模型调用超时限流
- 已预留内容安全校验位置
- 所有方法都是异步实现，遵循全异步规范
- 已添加必要的日志记录和token统计

---