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
6. 确保 JSON 格式正确

输出格式：
每个文件:
## 文件名: hooks/{filename}.json
```json
{...}
```
