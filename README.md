# Oh-My-Claude-Roles

<p align="center">
<em>Claude Code 角色工具包管理器 - 从原始角色规范文档一键生成完整 Claude Code 工具包</em>
</p>

<p align="center">
<a href="https://pypi.org/project/oh-my-claude-roles"><img src="https://img.shields.io/pypi/v/oh-my-claude-roles.svg" alt="PyPI version"></a>
<a href="https://pypi.org/project/oh-my-claude-roles"><img src="https://img.shields.io/pypi/pyversions/oh-my-claude-roles.svg" alt="Python versions"></a>
<a href="https://github.com/854771076/oh-my-claude-roles/blob/master/LICENSE"><img src="https://img.shields.io/github/license/854771076/oh-my-claude-roles.svg" alt="License"></a>
</p>

## 📖 目录

- [🤖 什么是 Oh-My-Claude-Roles](#-什么是-oh-my-claude-roles)
- [✨ 特性](#-特性)
- [🎯 典型使用场景](#-典型使用场景)
- [📦 安装](#-安装)
- [⚙️ 配置](#️-配置)
- [🚀 使用](#-使用)
- [🎨 内置示例角色](#-内置示例角色)
- [📝 角色文档格式](#-角色文档格式)
- [📁 项目结构](#-项目结构)
- [❓ 常见问题](#-常见问题)
- [🤝 贡献](#-贡献)
- [🧪 开发](#-开发)
- [📊 测试覆盖率](#-测试覆盖率)
- [🎯 支持的 Claude Code 组件](#-支持的-claude-code-组件)
- [⭐ 支持](#-支持)
- [📜 许可证](#-许可证)

## 🤖 什么是 Oh-My-Claude-Roles

Oh-My-Claude-Roles 是一个命令行工具，帮助你管理领域特定的 Claude Code 开发规范。你只需要编写一份纯文本的角色规范文档，Oh-My-Claude-Roles 会自动利用 AI 帮你生成：

- `CLAUDE.md` - 给 Claude 的核心指令文件
- `hooks/` - Claude Code 钩子脚本（前置检查、后置处理）
- `commands/` - 斜杠命令封装常见开发任务
- `agents/` - 专用子代理配置（代码审查、安全扫描等）
- `rules/` - 自动检测的编码规则
- `skills/` - 技能模块，自动触发领域知识

通过缓存机制，生成一次后可以重复安装，不需要重复调用 AI。

## ✨ 特性

- 🤖 **AI 驱动** - 自动从原始角色文档生成 Claude Code 完整工具包
- 📦 **缓存机制** - 预打包缓存，减少 API 调用成本
- 🎯 **一键安装** - 交互式菜单，选择角色一键安装到 `.claude/`
- 🎨 **六种工具类型** - 完整支持 Claude Code 所有扩展能力
- 🔌 **多 LLM 支持** - OpenAI、Anthropic、Azure、Google、Ollama 全都支持
- ✅ **TDD 开发** - 高测试覆盖率，每个模块都有完整测试
- 🔧 **自动配置** - 首次运行时自动检测并配置环境变量
- 📁 **多目录支持** - 优先使用用户目录配置，回退到当前项目目录
- ⚙️ **配置管理** - 提供 `config` 和 `config-set` 命令管理配置
- 🗑️ **卸载功能** - 支持卸载已安装的角色工具包
- 🔄 **配置热更新** - 修改配置后自动重新加载设置

## 🎯 典型使用场景

- **团队规范统一**：编写一份团队开发规范，所有成员一键安装到任何项目
- **多项目维护**：在多个项目之间共享 Claude Code 配置，避免重复劳动
- **领域特定角色**：为前端、后端、数据科学等不同领域创建专用开发角色
- **学习最佳实践**：收集整理社区优秀的 Claude Code 使用规范，随时安装使用
- **跨项目复用**：在用户目录保存常用角色，在任何项目中都可以快速安装
- **环境隔离**：为不同项目配置不同的 LLM 提供商和模型
- **快速配置**：使用 `config-set` 命令快速切换配置，无需手动编辑文件

## 📦 安装

```bash
pip install oh-my-claude-roles
```

## ⚙️ 配置

配置文件默认保存在用户目录的 `~/.oh-my-claude-roles/.env`。第一次运行时会自动提示配置，或者手动创建：

```bash
# 配置文件位置
~/.oh-my-claude-roles/.env
```

**自动配置**：第一次运行 `create` 或 `generate` 命令时，会自动引导你完成配置。

**手动配置**：创建 `.env` 文件并填写以下内容：

```bash
OH_ROLES_LLM_PROVIDER=openai
OH_ROLES_LLM_API_KEY=your-api-key
OH_ROLES_LLM_MODEL=gpt-4o
OH_ROLES_LLM_BASE_URL=
OH_ROLES_LLM_TIMEOUT=120
OH_ROLES_LLM_MAX_RETRIES=3
OH_ROLES_LLM_CONCURRENCY=3
```

配置项说明:

| 环境变量                     | 说明                                                 | 默认值       |
| ---------------------------- | ---------------------------------------------------- | ------------ |
| `OH_ROLES_LLM_PROVIDER`    | LLM 提供商: openai, anthropic, azure, gemini, ollama | `openai`   |
| `OH_ROLES_LLM_API_KEY`     | LLM API 密钥                                         | -            |
| `OH_ROLES_LLM_MODEL`       | 模型名称                                             | `gpt-4o`   |
| `OH_ROLES_LLM_BASE_URL`    | 自定义 API 地址（代理/本地模型）                     | -            |
| `OH_ROLES_LLM_TIMEOUT`     | API 超时（秒）                                       | `120`      |
| `OH_ROLES_LLM_MAX_RETRIES` | 失败重试次数                                         | `3`        |
| `OH_ROLES_LLM_CONCURRENCY` | 并发生成数                                           | `3`        |
| `OH_ROLES_ROLES_DIR`       | 角色文档存放目录（当前目录）                         | `roles`    |
| `OH_ROLES_PACKAGES_DIR`    | 缓存目录（当前目录）                                 | `packages` |

## 🚀 使用

### 交互式安装

```bash
oh-roles install
```

这个命令会:

1. 扫描 `roles/` 目录下所有角色文档
2. 交互式选择要安装的角色
3. 选择要安装哪些组件类型
4. 检查缓存，如果有最新缓存直接用，否则调用 AI 生成
5. 检测冲突，交互式选择处理方式
6. 安装到目标项目的 `.claude/` 目录

### 指定角色直接安装

```bash
oh-roles install backend/python
```

### 列出所有可用角色

```bash
oh-roles list
```

### AI 交互式创建新角色

```bash
oh-roles create                  # 交互式创建，自动保存
oh-roles create roles/my-role.md # 指定输出路径
```

这个命令会:

1. 启动交互式 AI 对话，引导你完成角色设计
2. 一步步询问角色的领域、技术栈、规范要求
3. 自动生成完整的角色文档 Markdown 文件
4. 保存到 `roles/` 目录，可以直接使用 `oh-roles install` 安装

### 强制重新生成（忽略缓存）

```bash
oh-roles generate backend/python
```

### 显示当前配置

```bash
oh-roles config
```

### 修改配置

```bash
# 修改单个配置项
oh-roles config-set --provider anthropic --model claude-3-opus-20240229

# 修改 API 密钥
oh-roles config-set --api-key your-new-api-key

# 修改超时时间和重试次数
oh-roles config-set --timeout 60 --max-retries 5
```

### 卸载角色

```bash
# 卸载已安装的角色工具包
oh-roles uninstall backend/python
```

### 清理缓存

```bash
oh-roles clean          # 清理全部
oh-roles clean backend/python  # 清理指定角色
```

## 🎨 内置示例角色

仓库已经内置了几个开箱可用的角色规范：

| 角色                         | 领域      | 说明                                |
| ---------------------------- | --------- | ----------------------------------- |
| `backend/python`           | 后端      | Python 企业级后端开发规范           |
| `fullstack/typescript`     | 全栈      | TypeScript 全栈开发规范             |
| `frontend/vue3`            | 前端      | Vue 3 + TypeScript 全栈开发助手规范 |
| `blockchain/ETHBlockChain` | 区块链    | 以太坊 Solidity 智能合约开发        |
| `ai/Prompt`                | AI 提示词 | AI 提示词工程企业级开发规范         |

直接安装使用：

```bash
oh-roles install backend/python
```

## 📝 角色文档格式

角色文档使用标准 Markdown 格式，支持 YAML frontmatter 来定义元数据:

```markdown
---
name: python
display_name: Python企业级后端开发规范
description: Python 3.11+ 全异步企业级后端项目开发规范
tags: [python, backend, async, fastapi]
version: 1.0.0
---

# Python企业级后端开发规范与最佳实践

在这里写上你的完整开发规范，包括:
- 技术栈要求
- 代码风格指南
- 项目结构约定
- 命名规范
- 最佳实践
- 禁止事项

...
```

如果不写 frontmatter 也可以，Oh-My-Claude-Roles 会自动从内容提取:

- 名称 = 文件名
- 标题 = 第一个 `#` 标题
- 描述 = 标题后的第一段
- 标签 = 从 `<!-- tags: a, b -->` 提取

## 📁 项目结构

### 用户配置目录（默认）

```
~/.oh-my-claude-roles/
├── .env                       # 配置文件
├── roles/                     # 用户角色文档（优先查询）
│   └── backend/
│       └── python.md          # 示例: Python 后端开发规范
└── packages/                  # 用户包缓存（优先查询）
    └── backend_python_1.0.0/  # 缓存的工具包
```

### 项目本地目录（可选）

```
oh-my-claude-roles/
├── roles/                      # 原始角色文档目录（当前目录）
│   └── backend/
│       └── python.md           # 示例: Python 后端开发规范
├── packages/                   # 本地包缓存（当前目录）
├── src/
│   ├── __init__.py
│   ├── cli.py                  # CLI 入口
│   ├── config.py               # Pydantic Settings 配置
│   ├── models.py               # 数据模型
│   ├── exceptions.py          # 自定义异常
│   ├── logger.py              # 日志配置
│   ├── scanner.py              # 角色文档扫描器
│   ├── validator.py           # LLM 输出验证器
│   ├── generator.py           # LLM 工具包生成器
│   ├── packager.py            # 打包缓存管理器
│   ├── installer.py           # 工具包安装器
│   └── prompts/               # LLM 提示词模板
│       ├── __init__.py
│       ├── claude_md.py
│       ├── hooks.py
│       ├── commands.py
│       ├── agents.py
│       ├── rules.py
│       └── skills.py
├── tests/                     # 测试
├── .env.example               # 环境变量示例
├── pyproject.toml             # 项目配置
└── README.md
```

## ❓ 常见问题

### Q: 为什么需要 Oh-My-Claude-Roles？

A: 当你在多个项目中使用 Claude Code 时，通常需要在每个项目重复编写相同的开发规范。Oh-My-Claude-Roles 让你一次编写，随处安装，并且利用 AI 自动生成完整的 Claude Code 工具链。

### Q: 生成的工具包存储在哪里？

A: 系统会优先使用用户目录的配置：
- 配置文件：`~/.oh-my-claude-roles/.env`
- 用户角色文档：`~/.oh-my-claude-roles/roles/`
- 用户包缓存：`~/.oh-my-claude-roles/packages/`

如果用户目录没有找到，会回退到当前项目目录：
- 当前项目角色文档：`roles/`
- 当前项目包缓存：`packages/`

安装时会复制到目标项目的 `.claude/` 目录。

### Q: 可以分享我的角色吗？

A: 当然可以！欢迎提交 Pull Request 将你的角色添加到仓库中，分享给社区。

### Q: 如何更新已安装的角色？

A: 重新运行 `oh-roles install <role>` 即可更新到最新版本。

### Q: 支持自定义提示词模板吗？

A: 支持。你可以通过环境变量指定自定义提示词模板目录，或者直接修改源码中的模板。

## 🤝 贡献

欢迎贡献代码！如果你有好的想法或发现了 Bug，请：

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的改动 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 🧪 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 查看覆盖率
pytest tests/ -v --cov=src --cov-report=term --cov-report=html

# 类型检查（mypy）
mypy src/

# 代码风格检查（ruff）
ruff check src/
ruff check src/ --fix  # 自动修复可修复的问题
```

## 📊 测试覆盖率

当前测试覆盖率: **~59%** overall.

未覆盖部分主要是:

- `cli.py` - CLI 接口（难以自动化测试，手动验证通过）
- `logger.py` - 简单日志配置
- `prompts/` - 纯提示词模板

所有核心业务逻辑模块测试覆盖率:

- `config.py` - 100%
- `exceptions.py` - 100%
- `models.py` - 100%
- `scanner.py` - 86%
- `packager.py` - 53%
- `validator.py` - 52%

## 🎯 支持的命令

| 命令          | 说明                                       |
| ------------- | ------------------------------------------ |
| `install`    | 安装角色工具包到目标项目                   |
| `generate`   | 强制重新生成并打包角色工具包，不安装       |
| `list`       | 列出所有可用角色                           |
| `uninstall`  | 卸载已安装的角色工具包                     |
| `config`     | 显示当前配置                               |
| `config-set` | 修改配置                                   |
| `clean`      | 清理缓存                                   |
| `version`    | 显示版本信息                               |
| `create`     | AI 交互式创建新角色文档                    |

## 🎯 支持的 Claude Code 组件

| 组件类型      | 说明                           |
| ------------- | ------------------------------ |
| `CLAUDE.md` | 核心指令，Claude 每次都会读取  |
| `hooks`     | Hooks 脚本，在特定时机自动触发 |
| `commands`  | 斜杠命令                       |
| `agents`    | 子代理配置                     |
| `rules`     | 自动检测的代码规则             |
| `skills`    | 自动触发的技能模块             |

## ⭐ 支持

如果你觉得这个项目对你有帮助，欢迎给一个 **Star** ⭐️，这对我很重要。

## 📜 许可证

MIT
