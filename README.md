# Oh-My-Claude-Roles

Claude Code 角色工具包管理器 - 从原始角色文档一键生成安装工具包。

## 特性

- 🤖 AI 驱动 - 自动从原始角色文档生成 Claude Code 工具包
- 📦 缓存机制 - 预打包缓存，减少 API 调用成本
- 🎯 一键安装 - 交互式菜单，选择角色一键安装到 `.claude/`
- 🎨 支持六种工具类型 - `CLAUDE.md` + `Hooks` + `Commands` + `Agents` + `Rules` + `Skills`
- 🔌 多 LLM 支持 - OpenAI、Anthropic、Azure、Google、Ollama

## 安装

```bash
pip install oh-my-claude-roles
```

## 配置

复制 `.env.example` 到 `.env`，配置你的 LLM API Key:

```bash
cp .env.example .env
# 编辑 .env 文件
```

## 使用

```bash
# 交互式安装
oh-roles install

# 列出所有可用角色
oh-roles list

# 强制重新生成
oh-roles generate backend/python

# 卸载
oh-roles uninstall backend/python

# 显示配置
oh-roles config

# 清理缓存
oh-roles clean
```

## 角色文档格式

角色文档使用 Markdown 格式，支持 YAML frontmatter:

```markdown
---
name: python
display_name: Python企业级后端开发规范
description: Python 3.11+ 全异步企业级后端项目开发规范
tags: [python, backend, async, fastapi]
version: 1.0.0
---

# Python企业级后端开发规范与最佳实践

...
```

## 许可证

MIT
