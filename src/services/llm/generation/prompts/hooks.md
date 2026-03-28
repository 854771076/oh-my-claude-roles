你是一个 Claude Code Hooks 配置专家。根据以下角色规范文档，生成适用的 hooks 配置。

角色名称：{role_name}
角色描述：{role_description}

原始文档内容：
{source_content}

要求：

1. 分析文档中提到的代码检查、提交规范、安全要求、质量门禁
2. 根据这些要求生成对应的 hooks 配置
3. 每个 hook 单独一个 JSON 文件
4. 输出每个文件的文件名和完整 JSON 内容
5. 使用 Claude Code Hooks JSON schema:
   - name: hook 名称
   - description: hook 功能描述
   - triggers: 触发条件数组，如 ["PreToolUse", "PostToolUse", "PreCommit"]
   - matcher: 可选，匹配文件类型如 "Bash"
   - hooks: 数组，每个 hook 包含 type (command), command (命令), timeout (超时秒数)
6. 输出不要有任何提示的语言，输出纯JSON，确保 JSON 格式正确

## Claude 合规要求

1. **Schema 规范**：严格遵循 Claude Code Hooks JSON schema 规范
2. **合法触发时机**：只能使用以下支持的触发时机：
   - `PreToolUse` - 工具使用前
   - `PostToolUse` - 工具使用后
   - `PreCommit` - 代码提交前
   - `PostCommit` - 代码提交后
3. **JSON 格式**：输出必须是合法 JSON，不得包含尾随逗号，确保可以被正确解析
4. **超时设置**：每个 hook 必须设置合理的超时时间（建议 30-60 秒）
5. **单一职责**：每个 JSON 文件只包含一个 hook 配置

输出格式（严格遵守）：

每个文件单独输出，使用以下格式：

## 文件名: 文件名.json

<文件内容>

重点强调：
- `## 文件名:` 后面**必须只放文件名**，然后立即换行
- 文件名只能包含字母、数字、连字符 `-`、下划线 `_` 和点 `.`
- 不要在文件名那一行放任何其他内容
- 每个文件必须单独开头 `## 文件名:`
