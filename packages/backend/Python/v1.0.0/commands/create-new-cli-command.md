---
name: create-new-cli-command
description: 创建符合Typer规范的新命令行命令
trigger: create-new-cli-command
---

按照规范创建一个新的Typer命令行命令。

### 使用方式：
`/create-new-cli-command 命令模块名称 命令名称`，例如 `create-new-cli-command user create-admin-user`

### 执行步骤：
1. 如果模块不存在，创建模块文件：`app/cli/commands/{模块名称}.py`
2. 在模块中生成命令模板，包含：
   - 帮助文档
   - 参数类型提示和帮助信息
   - 敏感参数自动添加hide_input和确认提示
   - 异常处理和友好错误输出
   - 结果成功/失败的清晰提示
3. 在`app/cli/main.py`中注册新命令

### 检查要点：
- 参数都添加了类型提示和帮助文档
- 复杂逻辑调用service层，不直接写业务逻辑
- 异常处理友好，输出清晰错误信息
- 符合Typer最佳实践，支持--help自动生成帮助

---