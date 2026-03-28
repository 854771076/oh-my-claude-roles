---
name: create-new-api-module
description: 创建新业务模块的全分层API代码骨架
trigger: create-new-api-module
---

按照规范为新业务模块创建从接口层到模型层的全分层代码骨架。

### 使用方式：
`/create-new-api-module 模块名称`，例如 `create-new-api-module product`

### 执行步骤：
1. 创建API端点文件：`app/api/v1/endpoints/{模块名}.py`，生成路由模板，遵循FastAPI开发规范
2. 创建Pydantic模型：`app/schemas/{模块名}.py`，生成Base/Create/Update/Out分层模型，包含Pydantic v2配置
3. 创建SQLAlchemy ORM模型：`app/models/{模块名}.py`，生成基础模型模板
4. 创建CRUD数据访问层：`app/crud/{模块名}.py`，继承基础CRUD基类
5. 创建业务服务层：`app/services/{模块名}_service.py`，生成服务类模板
6. 创建Celery任务文件：`app/tasks/{模块名}_tasks.py`，生成任务模板
7. 创建对应测试文件：`tests/integration/test_{模块名}_service.py`，生成基础测试用例骨架

### 检查要点：
- 所有文件命名符合蛇形小写规范
- 已添加正确的文件头部注释
- Pydantic模型已设置`model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)`
- 所有函数参数和返回值都添加了类型提示
- 所有方法都是异步实现，遵循全异步规范
- 严格遵循各层职责边界，没有跨层逻辑

---