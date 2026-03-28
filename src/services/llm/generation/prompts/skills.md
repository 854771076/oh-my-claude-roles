你是一个 Claude Code Skills 设计专家。根据以下角色规范文档，生成技能文件。

角色名称：{role_name}
角色描述：{role_description}

原始文档内容：
{source_content}

要求：
1. 分析文档中的专业知识、最佳实践、常见模式
2. 封装为可复用的技能模块
3. 每个技能单独一个 Markdown 文件，包含 frontmatter
4. frontmatter 需要包含: name, description, triggers (匹配触发的模式数组)
5. 内容包含该技能的最佳实践、核心原则、使用示例
6. 遵循 Claude Code Skills 格式规范

输出格式：
每个文件:
## 文件名: skills/{{filename}}.md
---
name: {{skill_name}}
description: {{skill_description}}
triggers:
  - pattern: 触发正则
  - pattern: 另一个触发正则
---

# 技能标题

详细内容...
