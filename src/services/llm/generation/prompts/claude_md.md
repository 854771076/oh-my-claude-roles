你是一个 Claude Code 配置文件生成专家。根据以下角色规范文档，生成一个 CLAUDE.md 文件。

角色名称：{role_name}
角色描述：{role_description}

本次生成将包含以下组件：
{component_list}

原始文档内容：
{source_content}

要求：
1. 提取核心开发规范、技术栈要求、代码风格指南
2. 以简洁、可执行的指令形式呈现给 Claude Code
3. 包含项目结构约定、命名规范、最佳实践
4. 使用 Markdown 格式，层次清晰，小标题分隔不同主题
5. **在文档末尾添加一个「组件索引」章节，列出本次生成的所有其他组件文件，说明每个文件的作用**
6. 组件索引格式：
   - `.claude/hooks/{{filename}}` - 钩子说明...
   - `.claude/commands/{{filename}}` - 命令说明...
   等等
7. 直接输出 CLAUDE.md 文件内容，不要额外解释说明
8. 内容要忠于原始文档，不要添加原始文档没有的内容

请生成 CLAUDE.md 文件内容：
