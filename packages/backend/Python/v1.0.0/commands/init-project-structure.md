---
name: init-project-structure
description: 按照企业级规范初始化Python后端项目目录结构
trigger: init-project-structure
---

按照本规范要求，在当前目录初始化符合Python企业级后端开发规范的项目目录结构，生成所有基础配置文件和目录骨架。

### 执行步骤：
1. 创建完整的分层目录结构，和规范中定义的保持完全一致
2. 生成所有基础配置文件：
   - `.env.example`：包含常见环境变量示例
   - `.pylintrc`：使用推荐的企业级配置，设置评分要求≥9分
   - `.pre-commit-config.yaml`：配置pre-commit钩子检查项
   - `pytest.ini`：统一pytest配置
   - `pyproject.toml`：配置依赖、black、isort
   - `Dockerfile`：多阶段构建生产镜像，非root运行
   - `docker-compose.yml`：编排FastAPI、Celery、Redis、PostgreSQL
3. 为每个目录创建`__init__.py`文件
4. 生成核心模块的基础模板：
   - `app/main.py`：FastAPI入口模板
   - `app/core/settings.py`：Pydantic Settings配置模板
   - `app/core/logger.py`：Loguru日志配置模板
   - `app/core/db.py`：异步数据库会话模板
   - `app/core/celery_app.py`：Celery初始化模板
   - `app/crud/base.py`：通用CRUD基类模板

### 检查要点：
- 严格遵循分层架构，职责边界清晰
- 所有文件编码为UTF-8
- 基础模板已包含核心规范要求的导入和结构
- 已添加`.gitignore`文件，排除日志、env、依赖、缓存等

---