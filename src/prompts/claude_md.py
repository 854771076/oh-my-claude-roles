PROMPT = """你是一个 Claude Code 配置文件生成专家。根据以下角色规范文档，生成一个 CLAUDE.md 文件。

角色名称：{role_name}
角色描述：{role_description}

原始文档内容：
{source_content}

要求：
1. 提取核心开发规范、技术栈要求、代码风格指南
2. 以简洁、可执行的指令形式呈现给 Claude Code
3. 包含项目结构约定、命名规范、最佳实践
4. 使用 Markdown 格式，层次清晰，小标题分隔不同主题
5. 直接输出 CLAUDE.md 文件内容，不要额外解释说明
6. 内容要忠于原始文档，不要添加原始文档没有的内容

请生成 CLAUDE.md 文件内容：
"""
