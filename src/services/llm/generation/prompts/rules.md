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

输出格式：
## 文件名: rules/{{filename}}.yaml
```yaml
name: {{rule_set_name}}
version: "1.0"
rules:
  - id: rule-id
    description: 规则描述
    pattern: 正则表达式
    severity: error
```
