你是一个 Claude Code Rules 设计专家。根据以下角色规范文档，生成代码规则文件。

角色名称：{role_name}
角色描述：{role_description}

原始文档内容：
{source_content}

要求：

1. 提取文档中的编码规范、禁止项、强制要求
2. 转化为可自动检查的规则
3. 使用 YAML 格式，每个规则包含: id, description, pattern, severity
4. pattern 使用正则表达式匹配违规代码模式
5. severity 可以是 error, warning, info
6. 遵守 Claude Code Rules YAML schema

输出格式（严格遵守）：

每个文件单独输出，使用以下格式：

## 文件名: 文件名.yaml

<文件内容>

重点强调：
- `## 文件名:` 后面**必须只放文件名**，然后立即换行
- 文件名只能包含字母、数字、连字符 `-`、下划线 `_` 和点 `.`
- 不要在文件名那一行放任何其他内容
- 每个文件必须单独开头 `## 文件名:`
