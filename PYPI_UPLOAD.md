# 上传到 PyPI 操作指南

## 前置准备

1. 在 [PyPI](https://pypi.org/) 注册账号
2. 在账号设置中创建 API Token

## 步骤 1: 安装构建和上传工具

```bash
python -m pip install --upgrade build twine
```

## 步骤 2: 构建分发包

```bash
python -m build
```

这会在 `dist/` 目录下生成两个文件：
- `.tar.gz` - 源代码压缩包
- `.whl` - Python wheel 包

## 步骤 3: 上传到 PyPI

### 上传到正式 PyPI

```bash
python -m twine upload dist/*
```

按提示输入：
- `username`: 输入 `__token__`
- `password`: 输入你的 API Token

### 上传到 TestPyPI（测试用）

```bash
python -m twine upload --repository testpypi dist/*
```

## 步骤 4: 测试安装

上传成功后，可以测试安装：

**从正式 PyPI：**
```bash
pip install oh-my-claude-roles
```

**从 TestPyPI：**
```bash
pip install --index-url https://test.pypi.org/simple/ --no-cache-dir oh-my-claude-roles
```

## 发布新版本

更新版本后，重新执行：

```bash
# 先清理旧的构建
rm -rf dist/

# 重新构建
python -m build

# 上传
python -m twine upload dist/*
```

## 备注

- 版本号在 `pyproject.toml` 中修改
- 确保 `description` 和 `readme` 信息正确
- 上传前可以用 `twine check dist/*` 检查包是否正确

## GitHub Action 自动发布

本项目已配置 GitHub Action，当你推送 tag 或创建 Release 时，会自动构建并发布到 PyPI。

### 配置步骤

1. 在 GitHub 仓库中进入 Settings → Secrets and variables → Actions
2. 点击 New repository secret
3. 添加一个名为 `PYPI_API_TOKEN` 的 secret，值为你的 PyPI API Token

### 使用方式

1. 修改 `pyproject.toml` 中的版本号
2. 创建并推送 tag:
```bash
git tag v0.1.0
git push origin v0.1.0
```
3. GitHub Action 会自动构建并发布到 PyPI

或者，你可以在 GitHub 上手动创建一个 Release，Action 也会自动触发发布。
