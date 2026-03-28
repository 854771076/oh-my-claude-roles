---
name: python-enterprise-backend-spec
description: Python企业级后端开发规范与最佳实践，适用于全异步FastAPI项目开发
triggers:
- python.*后端.*规范
- python.*开发.*规范
- 企业级.*python.*后端
- python.*最佳实践
- fastapi.*开发规范
- 异步.*python.*开发
---

# Python企业级后端开发规范与最佳实践

## 概述

本规范定义了Python 3.14+全异步企业级后端项目的开发标准，遵循「能异步都异步、有框架用框架不手写重复代码、强类型安全、可测试、可维护、高性能」六大核心原则，帮助团队构建高质量、可维护的企业级后端系统。

## 核心技术栈

所有技术栈均经过生产验证，严格遵循「不重复造轮子」原则：

| 技术组件              | 版本要求   | 核心定位 |
| --------------------- | ---------- | -------- |
| Python                | 3.14+      | 基础运行环境，强制新特性与类型提示 |
| FastAPI               | 最新稳定版 | 核心Web框架，全异步API开发 |
| Pydantic              | v2+        | 数据校验、类型安全、序列化核心 |
| SQLAlchemy            | 2.0+       | 异步ORM框架，所有数据库操作 |
| Celery                | 最新稳定版 | 分布式异步任务队列、定时任务 |
| Redis                 | 最新稳定版 | 分布式缓存、限流、Celery Broker |
| Pytest                | 最新稳定版 | 全量测试框架 |
| Loguru                | 最新稳定版 | 结构化日志框架 |
| Pydantic Settings     | 最新稳定版 | 全环境配置管理 |
| Httpx                 | 最新稳定版 | 异步HTTP客户端 |
| Tenacity              | 最新稳定版 | 重试逻辑框架 |
| Cachetools            | 最新稳定版 | 本地内存缓存，配合Redis做二级缓存 |
| Aiofiles              | 最新稳定版 | 异步文件操作 |
| Typer                 | 最新稳定版 | 命令行工具开发框架 |
| LangChain + LangGraph | 最新稳定版 | 大模型应用开发框架 |

## 核心开发铁则（最高优先级）

### 1. 能异步都异步
- 强制全链路异步：所有IO密集型操作必须使用异步库+async/await，禁止同步阻塞进入事件循环
- 禁止异步陷阱：
  - 禁止在异步函数中调用同步IO（同步requests、同步DB、同步open）
  - 禁止使用`time.sleep`，必须使用`asyncio.sleep`
  - 禁止在同步上下文直接调用异步函数，必须通过`asyncio.run`或线程池隔离
  - CPU密集型操作必须交给Celery，禁止阻塞FastAPI主事件循环
- 全链路保持异步：FastAPI路由→Service→CRUD→数据库，无同步断点

### 2. 禁止手写重复代码
| 功能场景       | 必须使用框架组件          | 禁止手写实现 |
| -------------- | ------------------------ | ------------ |
| 配置管理       | Pydantic Settings        | `os.getenv`、手写文件读取 |
| 参数校验       | Pydantic v2              | `if-else`判断 |
| 重试逻辑       | Tenacity                 | `while`循环+sleep |
| 日志管理       | Loguru                   | `print`、原生logging |
| 命令行工具     | Typer                    | `argparse` |
| 任务队列       | Celery                   | 手写多进程/线程调度 |
| 依赖管理       | FastAPI Depends          | 手写单例、全局对象 |
| 鉴权逻辑       | FastAPI OAuth2           | 手写鉴权 |
| LLM应用开发    | LangChain + LangGraph    | 裸调用大模型API |
| 异常处理       | 全局异常处理器           | 重复`try-except`模板 |

## 企业级项目目录结构

```
project_root/
├── .env.example
├── .pylintrc
├── .pre-commit-config.yaml
├── pytest.ini
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── app/                          # 核心代码目录
│   ├── main.py                   # 项目入口，FastAPI初始化
│   ├── api/                      # 接口层：仅参数接收、响应返回
│   │   ├── dependencies.py       # 全局依赖（鉴权、DB会话等）
│   │   ├── v1/                   # v1版本API
│   │   │   ├── api.py            # 路由汇总
│   │   │   └── endpoints/        # 按业务模块拆分
│   │   └── common/               # 通用接口（健康检查等）
│   ├── core/                     # 核心配置与底层组件，无业务代码
│   │   ├── settings.py           # Pydantic Settings配置
│   │   ├── exceptions.py         # 自定义异常、全局异常处理器
│   │   ├── logger.py             # Loguru配置
│   │   ├── db.py                 # 数据库异步会话管理
│   │   ├── redis.py              # Redis客户端初始化
│   │   ├── celery_app.py         # Celery初始化
│   │   └── middlewares.py        # 全局中间件
│   ├── schemas/                  # Pydantic模型层，无业务逻辑
│   ├── models/                   # SQLAlchemy ORM模型层
│   ├── crud/                     # 数据访问层，仅单表增删改查
│   │   └── base.py               # 通用CRUD基类
│   ├── services/                 # 业务逻辑层，唯一允许跨CRUD调用
│   │   └── llm/                  # LLM应用封装
│   ├── tasks/                    # Celery异步任务层
│   ├── utils/                    # 通用工具，纯函数无业务
│   ├── cli/                      # Typer命令行工具
│   └── constants/                # 全局常量
├── tests/                        # 测试目录，与app结构一一对应
│   ├── conftest.py               # pytest全局fixture
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── api/                      # 接口测试
├── logs/                         # 日志目录（gitignore）
└── docs/                         # 项目文档
```

## 代码书写规范

### 命名规范（严格遵循PEP8）

| 命名对象    | 规范要求 |
| ----------- | -------- |
| 项目/包名   | 全小写，下划线分隔 |
| 文件名      | 全小写，下划线分隔 |
| 变量名      | 蛇形小写，语义优先，禁止拼音、无意义命名 |
| 函数/方法名 | 蛇形小写，动词开头，异步无需加async前缀 |
| 类名        | 大驼峰，每个单词首字母大写 |
| 常量名      | 全大写，下划线分隔，统一放constants目录 |
| 私有成员    | 单下划线开头，禁止双下划线名称改写 |
| 异常类      | 大驼峰，以Exception结尾 |
| 枚举类      | 大驼峰，以Enum结尾 |

### 注释规范（Google风格）

- 文件头部必须说明职责、作者、创建时间
- 类必须说明职责、属性描述
- 非私有函数必须说明功能、参数、返回值、抛出异常
- TODO必须带责任人、创建日期、截止日期、需求说明
- 禁止冗余注释、禁止注释掉废弃代码

### 格式规范

- 单行最大120字符，4空格缩进，禁止tab
- 函数/类之间空2行，类内方法之间空1行
- 导入顺序：标准库 → 第三方库 → 内部模块，禁止通配符导入
- 单行字符串用双引号，拼接优先使用f-string
- 所有函数参数、返回值必须指定类型提示，禁止无意义`Any`
- 单个函数圈复杂度必须≤10，超过必须拆分

## 核心模块开发规范示例

### FastAPI接口开发示例

```python
# app/api/v1/endpoints/user.py
from fastapi import APIRouter, Depends, status
from app.schemas.user import UserOut, UserCreate
from app.services.user_service import user_service
from app.api.dependencies import get_current_admin_user

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="创建用户")
async def create_user(
    user_in: UserCreate,
    current_user: UserOut = Depends(get_current_admin_user)
):
    """创建新用户，仅管理员可操作"""
    return await user_service.create_user(user_in=user_in)
```

### Pydantic v2模型示例

```python
# app/schemas/user.py
from pydantic import BaseModel, Field, field_validator, ConfigDict
import re

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="用户名")
    phone: str = Field(description="手机号")
    is_active: bool = Field(default=True, description="是否激活")

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=32, description="密码")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r"^1[3-9]\d{9}$", v):
            raise ValueError("手机号格式错误")
        return v

class UserOut(UserBase):
    id: int = Field(description="用户ID")
    create_time: str = Field(description="创建时间")

    model_config = ConfigDict(from_attributes=True)
```

### Service业务层示例

```python
# app/services/user_service.py
from app.crud.user import crud_user
from app.schemas.user import UserCreate, UserOut
from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import get_password_hash
from app.core.db import async_session
from sqlalchemy.exc import IntegrityError

class UserService:
    async def get_user_by_id(self, user_id: int) -> UserOut:
        async with async_session() as session:
            user = await crud_user.get(session, id=user_id)
            if not user:
                raise NotFoundException(f"用户ID {user_id} 不存在")
            if not user.is_active:
                raise BusinessException("用户已被禁用")
            return UserOut.model_validate(user)

    async def create_user(self, user_in: UserCreate) -> UserOut:
        async with async_session() as session:
            async with session.begin():
                exist_user = await crud_user.get_by_username(session, username=user_in.username)
                if exist_user:
                    raise BusinessException(f"用户名 {user_in.username} 已存在")
                user_in.password = get_password_hash(user_in.password)
                try:
                    user = await crud_user.create(session, obj_in=user_in)
                except IntegrityError:
                    raise BusinessException("用户创建失败，数据冲突")
                return UserOut.model_validate(user)

user_service = UserService()
```

## 测试规范

- 核心原则：**禁止mock内部核心依赖**，数据库、Redis等内部组件必须使用真实测试实例，仅允许mock第三方不可控服务
- 测试分层：单元测试→集成测试→接口测试
- 覆盖率要求：核心业务≥90%，工具类100%
- 测试隔离：每个用例独立，测试结束自动清理数据
- 用例命名规范：`test_<功能>_<场景>_<预期结果>`

### 测试用例示例

```python
# tests/integration/test_user_service.py
import pytest
from app.services.user_service import user_service
from app.schemas.user import UserCreate
from app.core.exceptions import NotFoundException

@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    """测试：查询不存在用户，抛出NotFoundException"""
    with pytest.raises(NotFoundException):
        await user_service.get_user_by_id(user_id=999999)
```

## 代码提交规范（Conventional Commits）

提交格式：
```
<type>(<scope>): <subject>
```

类型说明：
- `feat`: 新增功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试用例修改
- `build`: 依赖/构建变更
- `ci`: CI配置变更
- `chore`: 不影响业务的调整
- `revert`: 回滚提交

正确示例：
```
feat(user): 新增用户密码重置功能
fix(order): 修复订单支付状态并发更新问题
docs: 更新开发规范文档
```

## 安全与运维规范

- 配置安全：敏感配置必须从环境变量加载，禁止提交git
- 密码安全：必须使用bcrypt/argon2加密存储
- 输入安全：所有用户输入必须Pydantic校验，防止注入攻击
- 部署：容器化部署，使用gunicorn+uvicorn worker，配置监控告警与健康检查
- 发布：生产环境采用灰度发布，保留回滚能力

## 禁用清单

- ❌ 禁止使用同步requests，必须使用httpx.AsyncClient
- ❌ 禁止使用同步DB驱动，必须使用SQLAlchemy 2.0异步模式
- ❌ 禁止使用print输出，必须使用loguru
- ❌ 禁止使用裸`except`，必须指定具体异常类型
- ❌ 禁止硬编码配置，必须使用Pydantic Settings
- ❌ 禁止手写参数校验，必须使用Pydantic v2
- ❌ 禁止手写重试逻辑，必须使用Tenacity
- ❌ 禁止mock内部核心依赖，测试必须使用真实实例

---

## Claude 开发规范

创建新技能必须使用 `skill-create` / `skill-creator` 技能，遵循技能创建流程，不得手动创建。