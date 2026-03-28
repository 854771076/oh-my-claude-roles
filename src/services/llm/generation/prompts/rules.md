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

## Claude 合规要求

1. **Schema 规范**：严格遵循 Claude Code Rules YAML schema 规范
2. **必填字段**：根级别必须包含：
   - `name`: 规则集名称
   - `version`: 规则集版本
   - `rules`: 规则数组
3. **规则字段**：每个规则必须包含：
   - `id`: 规则唯一 ID
   - `description`: 规则描述（说明为什么禁止/警告）
   - `pattern`: 匹配违规代码的正则表达式
   - `severity`: 严重等级：`error` / `warning` / `info`
4. **正则质量**：`pattern` 必须是合法的正则表达式，避免过于宽泛的匹配，减少误报
5. **相关性**：只提取原始文档中明确提到的禁止项和强制要求，不添加额外规则

输出格式（严格遵守）：

每个文件单独输出，使用以下格式：

## 文件名: 文件名.yaml

<文件内容>

重点强调：
- `## 文件名:` 后面**必须只放文件名**，然后立即换行
- 文件名只能包含字母、数字、连字符 `-`、下划线 `_` 和点 `.`
- 不要在文件名那一行放任何其他内容
- 每个文件必须单独开头 `## 文件名:`
