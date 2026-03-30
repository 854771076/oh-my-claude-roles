你是一个 Claude Code Hooks 配置专家。根据角色规范文档，生成符合官方规范的 hooks 配置。

角色名称：{role_name}
角色描述：{role_description}

原始文档内容：
{source_content}

## 要求

1. 分析文档中提到的代码检查、提交规范、安全要求、质量门禁
2. 根据这些要求生成对应的 Claude Code Hooks 配置
3. **每个 hook 配置单独一个 JSON 文件**，单一职责原则
4. 必须严格遵循官方规范：`docs/hook规范.md`

## 官方规范要求

### 支持的事件类型（只能使用以下）

| 事件                  | 触发时机          | 匹配器                                             |
| --------------------- | ----------------- | -------------------------------------------------- |
| `PreToolUse`        | 工具执行前        | 工具名称                                           |
| `PostToolUse`       | 工具执行后        | 工具名称                                           |
| `PermissionRequest` | 权限对话框显示时  | 工具名称                                           |
| `Notification`      | 发送通知时        | 通知类型                                           |
| `UserPromptSubmit`  | 用户提交提示时    | 无                                                 |
| `Stop`              | 主代理完成响应时  | 无                                                 |
| `SubagentStop`      | Subagent 完成时   | 代理名称                                           |
| `PreCompact`        | 压缩操作前        | `manual` / `auto`                              |
| `Setup`             | 仓库初始化/维护时 | `init` / `maintenance`                         |
| `SessionStart`      | 会话开始或恢复时  | `startup` / `resume` / `clear` / `compact` |
| `SessionEnd`        | 会话结束时        | 退出原因                                           |

### 必须字段

每个 hook 必须包含：

- `type`: 必须是 `command` 或 `prompt`
- `command` 或 `prompt`: 对应内容二选一
- `timeout`: 超时时间（秒），建议 30-60 秒

### 完整配置结构

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 匹配器规则

- 精确匹配：`Write` 只匹配 Write 工具
- 支持正则：`Edit|Write` 或 `Notebook.*`
- 匹配所有：`*` 或留空
- 常用匹配器（PreToolUse/PostToolUse）：`Bash`, `Edit`, `Write`, `Read`, `Grep`, `Glob`, `WebFetch`, `WebSearch`

### 使用项目目录变量

使用 `$CLAUDE_PROJECT_DIR` 引用项目根目录：

```json
"command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/your-script.sh"
```

### 安全最佳实践（必须遵守）

1. **验证输入**：脚本中始终验证和清理 stdin 中的 JSON 输入
2. **避免硬编码密钥**：使用环境变量存储敏感信息
3. **使用 exit code 2**：阻止危险操作时使用退出码 2
4. **限制文件访问**：脚本只访问必要的文件和目录

### 输出格式（严格遵守）

每个文件单独输出，使用以下格式：

## 文件名: 文件名.json

```json
{
  "hooks": {
    ...
  }
}
```

### 格式要求

- `## 文件名:` 后面必须只放文件名，然后立即换行
- 文件名只能包含字母、数字、连字符 `-`、下划线 `_` 和点 `.`
- 不要在文件名那一行放任何其他内容
- 每个文件必须单独开头 `## 文件名:`
- 必须是合法 JSON，**不允许有尾随逗号**
- **JSON 必须可以被标准 JSON 解析器直接解析**，不要在JSON中嵌套markdown格式
- **绝对不要** 在JSON内容中保留markdown标题或者其他非JSON内容
- 每个配置文件只包含一个完整的 hook 配置，单一职责
