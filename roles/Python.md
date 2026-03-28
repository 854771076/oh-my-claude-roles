# Python企业级后端开发规范与最佳实践

**文档版本**: v1.0.0
**适用范围**: Python 3.14 + 全异步企业级后端项目
**更新日期**: 2026-03-27
**核心原则**: 能异步都异步、有框架用框架不手写重复代码、强类型安全、可测试、可维护、高性能

---

## 一、核心技术栈与定位

所有技术栈均经过企业级生产验证，严格遵循「不重复造轮子」原则，禁止手写替代框架已有能力的代码。

| 技术组件              | 版本要求   | 核心定位与使用规范                                                                     |
| --------------------- | ---------- | -------------------------------------------------------------------------------------- |
| Python                | 3.14+      | 基础运行环境，强制使用新特性类型提示、优化异步性能，禁止使用3.14以下版本               |
| FastAPI               | 最新稳定版 | 核心Web框架，全异步API开发，强制使用依赖注入、路由分层、原生异步支持                   |
| Pydantic              | v2+        | 数据校验、类型安全、序列化核心，所有入参出参、配置、数据模型必须使用，禁止手写参数校验 |
| Celery                | 最新稳定版 | 分布式异步任务队列，所有异步离线任务、定时任务必须使用，禁止手写多进程/线程任务        |
| Redis                 | 最新稳定版 | 分布式缓存、限流、Celery Broker/结果存储，配合cachetools做二级缓存                     |
| Flower                | 最新稳定版 | Celery任务监控面板，生产环境强制开启身份认证                                           |
| Pytest                | 最新稳定版 | 全量测试框架，遵循「不mock内部核心依赖」原则，覆盖单元、集成、接口全场景               |
| Loguru                | 最新稳定版 | 结构化日志框架，全项目统一日志入口，禁止使用print、原生logging                         |
| Pydantic Settings     | 最新稳定版 | 全环境配置管理，所有配置必须通过该组件加载，禁止硬编码、直接读取环境变量               |
| Pylint                | 最新稳定版 | 静态代码检查，强制准入门槛，代码评分≥9分方可提交                                      |
| LangChain + LangGraph | 最新稳定版 | 大模型应用开发框架，所有LLM相关逻辑、智能体、工具调用必须封装，禁止裸调用大模型API     |
| Typer                 | 最新稳定版 | 命令行工具开发框架，所有CLI脚本必须使用，禁止手写argparse                              |
| Tenacity              | 最新稳定版 | 重试逻辑框架，所有网络、IO、第三方调用的重试必须使用，禁止手写循环重试                 |
| Cachetools            | 最新稳定版 | 本地内存缓存，用于读多写少、低一致性要求的高频数据，配合Redis做二级缓存                |
| SQLAlchemy            | 2.0+       | 异步ORM框架，所有数据库操作必须使用异步模式，禁止原生SQL拼接、同步DB操作               |
| Httpx                 | 最新稳定版 | 异步HTTP客户端，所有第三方接口调用必须使用AsyncClient，禁止使用同步requests            |
| Aiofiles              | 最新稳定版 | 异步文件操作，所有文件读写必须使用，禁止同步open阻塞事件循环                           |

---

## 二、核心开发铁则（最高优先级）

### 1. 能异步都异步

- **强制全链路异步**：所有IO密集型操作（数据库、Redis、网络请求、文件读写、第三方API调用）必须使用异步库+async/await语法，禁止同步阻塞代码进入异步事件循环
- **禁止异步陷阱**：
  - 禁止在异步函数中调用同步IO操作（如同步requests、同步DB驱动、同步open）
  - 禁止在异步函数中使用time.sleep，必须使用asyncio.sleep
  - 禁止在同步上下文中直接调用异步函数，必须通过asyncio.run或线程池隔离
  - CPU密集型操作必须交给Celery任务执行，禁止阻塞FastAPI主事件循环
- **异步边界规范**：FastAPI路由→Service层→CRUD层→数据库/缓存/网络，全链路保持异步，无同步断点

### 2. 有框架用框架，禁止手写重复代码

- 配置管理：必须用Pydantic Settings，禁止手写os.getenv、ini/yaml文件读取
- 参数校验：必须用Pydantic v2，禁止手写if-else参数合法性判断
- 重试逻辑：必须用Tenacity，禁止手写while循环+sleep重试
- 缓存逻辑：必须用Cachetools/Redis封装，禁止手写缓存判断逻辑
- 日志管理：必须用Loguru，禁止手写logging配置、print输出
- 命令行工具：必须用Typer，禁止手写参数解析逻辑
- 任务队列：必须用Celery，禁止手写多进程/线程任务调度
- 依赖管理：必须用FastAPI Depends，禁止手写单例、全局对象生命周期管理
- 鉴权逻辑：必须用FastAPI OAuth2体系，禁止手写鉴权逻辑
- LLM应用：必须用LangChain+LangGraph，禁止手写大模型调用循环、状态管理
- 异常处理：必须用全局异常处理器，禁止重复的try-except模板代码

---

## 三、企业级项目目录结构

严格遵循分层架构，职责单一，边界清晰，禁止跨层调用。

```
project_root/
├── .env.example                # 环境变量示例，禁止提交真实.env文件
├── .pylintrc                   # 统一pylint配置，团队共用禁止私自修改
├── .pre-commit-config.yaml     # pre-commit钩子配置
├── pytest.ini                  # pytest统一配置
├── pyproject.toml              # 项目依赖、black/isort配置
├── Dockerfile                  # 生产环境镜像构建文件
├── docker-compose.yml          # 全服务编排（FastAPI、Celery、Redis、DB等）
├── app/                        # 项目核心代码目录
│   ├── __init__.py
│   ├── main.py                 # 项目入口，FastAPI实例初始化、路由注册、生命周期管理
│   ├── api/                    # 接口层：仅负责参数接收、响应返回、鉴权，不写业务逻辑
│   │   ├── __init__.py
│   │   ├── dependencies.py     # 全局依赖（鉴权、DB会话、当前用户等）
│   │   ├── v1/                 # v1版本API，按业务模块拆分
│   │   │   ├── __init__.py
│   │   │   ├── api.py          # 路由汇总，统一注册当前版本所有endpoint
│   │   │   └── endpoints/      # 按业务模块拆分路由文件
│   │   │       ├── user.py
│   │   │       ├── order.py
│   │   │       └── common.py
│   │   └── common/             # 通用接口（健康检查、metrics等）
│   ├── core/                   # 核心配置与底层组件：禁止业务代码侵入
│   │   ├── __init__.py
│   │   ├── settings.py         # Pydantic Settings 全环境配置管理
│   │   ├── security.py         # 安全工具（密码加密、JWT、签名等）
│   │   ├── exceptions.py       # 自定义异常类、全局异常处理器
│   │   ├── logger.py           # Loguru统一日志配置
│   │   ├── db.py               # 数据库异步会话、连接池管理
│   │   ├── redis.py            # Redis异步客户端初始化
│   │   ├── celery_app.py       # Celery应用初始化、任务配置
│   │   └── middlewares.py      # 全局中间件（请求ID、CORS、限流、日志等）
│   ├── schemas/                 # Pydantic模型层：入参校验、出参序列化，无业务逻辑
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── order.py
│   │   └── common.py
│   ├── models/                  # SQLAlchemy ORM模型层：数据库表结构映射
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── order.py
│   ├── crud/                    # 数据访问层：仅负责单表的增删改查，无业务逻辑
│   │   ├── __init__.py
│   │   ├── base.py             # 通用CRUD基类，所有单表操作继承
│   │   ├── user.py
│   │   └── order.py
│   ├── services/                # 业务逻辑层：核心业务规则实现，唯一允许跨CRUD调用
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── order_service.py
│   │   └── llm/                 # LangChain+LangGraph相关业务封装
│   │       ├── __init__.py
│   │       ├── agents/
│   │       ├── tools/
│   │       └── prompts/
│   ├── tasks/                   # Celery异步任务层：仅负责任务调度，业务逻辑调用services层
│   │   ├── __init__.py
│   │   ├── user_tasks.py
│   │   ├── order_tasks.py
│   │   └── scheduled_tasks.py  # 定时任务
│   ├── utils/                   # 通用工具层：无状态纯函数，禁止业务逻辑侵入
│   │   ├── __init__.py
│   │   ├── date_utils.py
│   │   ├── encrypt_utils.py
│   │   └── validator_utils.py
│   ├── cli/                     # Typer命令行工具
│   │   ├── __init__.py
│   │   ├── main.py             # CLI入口
│   │   └── commands/
│   └── constants/               # 全局常量定义
│       ├── __init__.py
│       ├── common_constants.py
│       └── error_constants.py
├── tests/                       # 测试目录，与app目录结构一一对应
│   ├── __init__.py
│   ├── conftest.py             # pytest全局fixture
│   ├── unit/                    # 单元测试：工具函数、独立方法
│   ├── integration/             # 集成测试：services、crud层
│   └── api/                     # 接口测试：全链路API测试
├── logs/                        # 日志文件目录（gitignore）
└── docs/                        # 项目文档、API文档、设计文档
```

---

## 四、代码书写规范

### 1. 命名规范（严格遵循PEP8）

| 命名对象    | 规范要求                                                             | 正确示例                                              | 错误示例                                           |
| ----------- | -------------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| 项目/包名   | 全小写，下划线分隔，禁止大写、点号                                   | user_service, order_manage                            | UserService, order.service                         |
| 文件名      | 全小写，下划线分隔，动词/名词清晰                                    | user_api.py, create_order.py                          | UserApi.py, userApi.py                             |
| 变量名      | 蛇形命名，全小写，下划线分隔，语义优先，禁止拼音、单字母（循环除外） | user_id, order_amount, max_retry_times                | userID, orderAmount, yonghu_id, x                  |
| 函数/方法名 | 蛇形命名，全小写，动词开头，语义优先，异步函数无需加async前缀        | get_user_by_id, create_order, async def get_user_info | GetUserInfo, async def async_get_user, createOrder |
| 类名        | 大驼峰命名，每个单词首字母大写，职责清晰                             | UserService, OrderCreateSchema, BusinessException     | userService, user_service, OrderCreate             |
| 常量名      | 全大写，下划线分隔，统一放在constants目录                            | MAX_PAGE_SIZE, DEFAULT_TOKEN_EXPIRE_SECONDS           | maxPageSize, default_expire                        |
| 私有成员    | 模块/类内部使用的成员，单下划线开头，禁止双下划线（名称改写）        | _get_user_internal, _user_password, _private_method   | __get_user, __password                             |
| 异常类      | 大驼峰，以Exception结尾                                              | BusinessException, NotFoundException                  | business_error, NotFoundError                      |
| 枚举类      | 大驼峰，以Enum结尾                                                   | UserStatusEnum, OrderTypeEnum                         | user_status, UserStatusType                        |

**强制禁止**：

- 拼音命名（通用行业术语除外，如zhifubao需统一，优先用英文alipay）
- 无意义命名：a、b、temp、data、info等模糊命名
- 缩写不统一：禁止同时使用usr和user、msg和message
- 关键字冲突：禁止使用id、type、class、def等Python关键字作为变量名，可加后缀如user_id、order_type

### 2. 注释规范

采用Google风格注释，核心原则：**必要注释，拒绝冗余，业务逻辑必注释，自解释代码不注释**

#### 2.1 文件头部注释

每个py文件开头必须添加，说明文件职责、作者、创建时间

```python
"""
用户模块业务逻辑实现
@Author: 张三
@CreateTime: 2026-03-27
@Description: 包含用户注册、登录、信息修改、权限管理等核心业务逻辑
"""
```

#### 2.2 类注释

```python
class UserService:
    """用户业务服务类

    封装用户全生命周期的业务逻辑，提供用户信息查询、修改、权限校验等能力
    所有方法均为异步方法，需在异步上下文中调用

    Attributes:
        crud_user: 用户数据访问对象
        crud_role: 角色数据访问对象
    """
```

#### 2.3 函数/方法注释

所有非私有函数、对外接口、复杂业务函数必须添加，简单工具函数可简化

```python
async def get_user_by_id(
    user_id: int,
    include_role: bool = False
) -> UserOut:
    """根据用户ID获取用户信息

    Args:
        user_id: 用户唯一ID，正整数，必填
        include_role: 是否返回用户关联的角色信息，默认False

    Returns:
        UserOut: 用户信息输出模型，符合Pydantic序列化规范

    Raises:
        NotFoundException: 用户ID不存在时抛出
        BusinessException: 用户状态异常时抛出
    """
```

#### 2.4 特殊注释规范

- **TODO注释**：必须带【责任人】【创建日期】【截止日期】【需求说明】，禁止无归属TODO
  ```python
  # TODO(张三, 2026-03-27, 2026-04-10): 优化用户列表查询性能，添加复合索引，需求链接: xxx
  ```
- **业务规则注释**：复杂业务判断、特殊逻辑必须添加注释，说明业务背景和规则
- **禁止**：注释掉的代码，废弃代码直接删除，git会保留历史记录
- **禁止**：冗余注释，如 `user_id = 1 # 给user_id赋值1`这种无意义注释

### 3. 代码格式规范

- 行宽限制：单行代码最大长度120字符，超过自动换行
- 缩进规范：4个空格缩进，禁止使用tab
- 空行规范：
  - 函数/类之间空2行
  - 类内方法之间空1行
  - 逻辑块之间空1行，禁止连续空行
- 导入规范：
  - 导入顺序：标准库 → 第三方库 → 内部模块，每组之间空1行
  - 禁止使用 `from xxx import *`通配符导入
  - 禁止循环导入，跨模块导入必须遵循层级规范
  - 使用isort自动格式化导入顺序，团队统一配置
- 字符串规范：
  - 单行字符串用双引号，多行字符串用三双引号
  - 字符串拼接优先使用f-string，禁止用+拼接大量字符串
- 语法规范：
  - 禁止使用全局变量，有状态对象必须通过依赖注入管理
  - 禁止使用eval、exec等危险函数
  - 禁止魔法数字，所有固定值必须定义为常量
  - 函数参数必须指定类型提示，返回值必须指定类型提示，禁止Any类型（特殊场景除外）
  - 圈复杂度：单个函数圈复杂度必须≤10，超过必须拆分

---

## 五、核心模块开发规范

### 1. FastAPI接口开发规范

- **路由分层**：禁止在main.py中写接口，必须按业务模块拆分到endpoints，按版本管理
- **职责单一**：接口层仅负责：参数接收、鉴权校验、调用service层、响应返回，禁止写业务逻辑
- **依赖注入**：所有重复逻辑（DB会话、当前用户、权限校验）必须封装为依赖，通过Depends注入
- **类型安全**：所有入参必须指定Pydantic模型，所有出参必须指定response_model，禁止无类型响应
- **接口规范**：
  - RESTful风格：GET（查询）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除）
  - 路径命名：全小写，下划线分隔，版本前缀，如 `/api/v1/users/{user_id}`
  - 状态码规范：200（成功）、201（创建成功）、400（参数错误）、401（未认证）、403（无权限）、404（资源不存在）、500（服务内部错误）
  - 统一响应格式：所有接口返回统一结构，如 `{"code": 200, "msg": "success", "data": {}}`
- **示例**：

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

@router.get("/{user_id}", response_model=UserOut, summary="根据ID获取用户信息")
async def get_user(user_id: int, current_user: UserOut = Depends(get_current_admin_user)):
    """根据用户ID获取用户详情，仅管理员可操作"""
    return await user_service.get_user_by_id(user_id=user_id)
```

### 2. Pydantic v2开发规范

- **模型分层**：入参模型（Create/Update）、出参模型（Out/Resp）、内部模型（Base）严格拆分
- **强制校验**：
  - 所有模型必须设置 `model_config = ConfigDict(extra="forbid")`，禁止传入未定义字段
  - 字符串字段必须设置strip_whitespace=True，自动去除首尾空格
  - 所有字段必须添加类型提示，禁止Any类型
  - 格式校验必须通过field_validator实现，禁止业务层手写校验
- **序列化规范**：
  - 出参模型必须设置from_attributes=True，支持ORM对象自动序列化
  - 敏感字段必须设置exclude=True，禁止返回给前端（如password、salt）
  - 使用model_dump()进行序列化，禁止使用旧版dict()方法
- **示例**：

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
            raise ValueError("手机号格式错误，必须为11位有效手机号")
        return v

class UserOut(UserBase):
    id: int = Field(description="用户ID")
    create_time: str = Field(description="创建时间")

    model_config = ConfigDict(from_attributes=True)
```

### 3. 业务层（Services）开发规范

- **唯一业务层**：所有业务逻辑、规则判断、事务管理必须写在services层，禁止分散到api/crud层
- **全异步实现**：所有方法必须为async异步方法，调用crud/第三方接口必须使用await
- **职责边界**：
  - 允许跨CRUD调用，实现多表关联业务
  - 允许调用其他services层方法
  - 禁止直接操作数据库，必须通过crud层
  - 禁止直接返回响应给前端，必须返回模型对象/基础数据
- **事务管理**：多表操作必须开启事务，异常时自动回滚
- **示例**：

```python
# app/services/user_service.py
from app.crud.user import crud_user
from app.crud.role import crud_role
from app.schemas.user import UserCreate, UserOut
from app.core.exceptions import BusinessException, NotFoundException
from app.core.security import get_password_hash
from app.core.db import async_session
from sqlalchemy.exc import IntegrityError

class UserService:
    async def get_user_by_id(self, user_id: int, include_role: bool = False) -> UserOut:
        async with async_session() as session:
            user = await crud_user.get(session, id=user_id)
            if not user:
                raise NotFoundException(f"用户ID {user_id} 不存在")
            if not user.is_active:
                raise BusinessException("用户已被禁用，无法查询")
            user_out = UserOut.model_validate(user)
            if include_role:
                user_out.roles = await crud_role.get_roles_by_user_id(session, user_id=user_id)
            return user_out

    async def create_user(self, user_in: UserCreate) -> UserOut:
        async with async_session() as session:
            async with session.begin(): # 开启事务
                # 校验用户名是否存在
                exist_user = await crud_user.get_by_username(session, username=user_in.username)
                if exist_user:
                    raise BusinessException(f"用户名 {user_in.username} 已存在")
                # 密码加密
                user_in.password = get_password_hash(user_in.password)
                try:
                    user = await crud_user.create(session, obj_in=user_in)
                except IntegrityError:
                    raise BusinessException("用户创建失败，数据冲突")
                return UserOut.model_validate(user)

user_service = UserService()
```

### 4. 数据访问层（CRUD）开发规范

- **单表职责**：每个CRUD类仅负责对应单表的增删改查，禁止多表关联、业务逻辑
- **全异步实现**：所有方法必须为async异步方法，使用SQLAlchemy 2.0异步模式
- **通用基类**：所有CRUD类必须继承通用BaseCRUD基类，复用基础增删改查能力，禁止重复代码
- **禁止**：原生SQL拼接，必须使用ORM参数化查询，防止SQL注入
- **示例**：

```python
# app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        return db_obj

    # 通用update、remove、list等方法
```

### 5. Celery异步任务开发规范

- **职责边界**：任务层仅负责任务调度、重试、异常处理，业务逻辑必须调用services层，禁止在任务中写业务逻辑
- **幂等性要求**：所有任务必须保证幂等，重复执行不会产生副作用
- **参数规范**：任务参数仅支持可序列化的基础类型（ID、字符串、数字），禁止传递大对象、DB连接、文件句柄
- **重试规范**：使用Tenacity或Celery自带重试机制，指定重试异常类型、最大次数、退避策略，禁止无限重试
- **队列拆分**：按任务类型拆分队列，CPU密集型、IO密集型、定时任务分队列部署，避免互相阻塞
- **结果管理**：不需要的任务结果必须设置ignore_result=True，减少Redis存储压力
- **示例**：

```python
# app/tasks/user_tasks.py
from app.core.celery_app import celery_app
from app.services.user_service import user_service
from app.core.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from httpx import TimeoutException, ConnectionError

@celery_app.task(
    queue="io_queue",
    ignore_result=False,
    retry_backoff=True,
    max_retries=3
)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((TimeoutException, ConnectionError)),
    before_sleep=lambda retry_state: logger.warning(f"用户同步任务重试中，次数：{retry_state.attempt_number}")
)
def sync_user_third_party_info(user_id: int):
    """同步用户第三方信息异步任务"""
    try:
        logger.info(f"开始同步用户{user_id}第三方信息")
        # 调用service层业务逻辑
        user_service.sync_user_third_party_info(user_id=user_id)
        logger.info(f"用户{user_id}第三方信息同步成功")
        return True
    except Exception as e:
        logger.error(f"用户{user_id}第三方信息同步失败：{str(e)}", exc_info=True)
        raise
```

### 6. LangChain+LangGraph开发规范

- **封装隔离**：所有LLM相关逻辑必须封装在services/llm目录下，禁止与业务代码耦合
- **提示词管理**：所有提示词必须放在独立的prompts目录下，禁止硬编码在代码中
- **工具封装**：所有外部工具必须继承LangChain BaseTool，统一接口、统一异常处理、统一日志
- **状态管理**：复杂智能体必须使用LangGraph StateGraph管理状态，禁止使用全局变量、字典管理对话状态
- **重试与限流**：所有大模型调用必须使用Tenacity做重试，处理限流、超时异常，记录token消耗
- **安全校验**：大模型输入、输出必须做内容安全校验，防止敏感内容、注入攻击
- **示例**：

```python
# app/services/llm/agents/customer_service_agent.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from app.services.llm.tools.order_query_tool import OrderQueryTool
from app.core.settings import settings
from app.core.logger import logger

# 状态定义
class CustomerServiceState(TypedDict):
    user_id: str
    user_query: str
    conversation_history: list
    tool_result: dict
    response: str

# 智能体构建
class CustomerServiceAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
            timeout=30,
            max_retries=2
        )
        self.tools = [OrderQueryTool()]
        self.memory = MemorySaver()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(CustomerServiceState)
        # 节点定义
        workflow.add_node("query_understand", self._query_understand)
        workflow.add_node("call_tool", self._call_tool)
        workflow.add_node("generate_response", self._generate_response)
        # 边定义
        workflow.set_entry_point("query_understand")
        workflow.add_conditional_edges("query_understand", self._route_query)
        workflow.add_edge("call_tool", "generate_response")
        workflow.add_edge("generate_response", END)
        return workflow.compile(checkpointer=self.memory)

    # 节点方法实现
    async def arun(self, state: CustomerServiceState, config: dict) -> dict:
        """异步运行智能体"""
        try:
            return await self.workflow.ainvoke(state, config=config)
        except Exception as e:
            logger.error(f"客服智能体运行失败：{str(e)}", exc_info=True)
            raise
```

### 7. Typer CLI开发规范

- **命令拆分**：按功能模块拆分命令，禁止写超长单文件命令
- **参数校验**：所有参数必须添加帮助文档、类型提示，复杂参数使用Pydantic模型校验
- **用户体验**：敏感参数（密码、密钥）必须使用hide_input=True，确认提示
- **异常处理**：友好处理异常，输出清晰的错误信息，禁止抛出完整异常栈给用户
- **示例**：

```python
# app/cli/main.py
import typer
from typing_extensions import Annotated
from app.services.user_service import user_service
from app.schemas.user import UserCreate
from app.core.exceptions import BusinessException

app = typer.Typer(help="企业级后端管理CLI工具", no_args_is_help=True)

@app.command()
def create_admin_user(
    username: Annotated[str, typer.Option(help="管理员用户名", prompt="请输入管理员用户名")],
    password: Annotated[str, typer.Option(help="管理员密码", prompt=True, hide_input=True, confirmation_prompt=True)],
    phone: Annotated[str, typer.Option(help="管理员手机号", prompt="请输入管理员手机号")],
):
    """创建超级管理员用户"""
    try:
        user_in = UserCreate(username=username, password=password, phone=phone, is_admin=True)
        user = user_service.create_user(user_in=user_in)
        typer.echo(f"✅ 管理员用户 {username} 创建成功，用户ID：{user.id}")
    except BusinessException as e:
        typer.echo(f"❌ 创建失败：{str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
```

---

## 六、测试规范（核心要求：不mock内部依赖）

### 1. 核心测试原则

- **禁止mock内部核心依赖**：数据库、Redis、Celery、Services、CRUD等内部可控组件，必须使用真实测试环境实例，禁止mock，保证测试真实性
- **仅允许mock的场景**：外部不可控、有成本的第三方服务（如支付API、短信接口、大模型API），内部服务绝对禁止mock
- **测试分层**：单元测试→集成测试→接口测试，全量覆盖核心业务代码
- **覆盖率要求**：核心业务代码覆盖率≥90%，工具类代码覆盖率100%
- **测试隔离**：每个测试用例独立，互不影响，测试结束后自动清理测试数据

### 2. 测试环境规范

- 本地开发、CI流水线必须使用独立的测试环境实例（测试DB、测试Redis），禁止使用开发/生产环境
- 使用docker-compose一键启动测试环境，保证团队环境统一
- 测试DB每次运行测试前自动创建表结构，测试结束后自动清理数据，使用事务回滚保证隔离性

### 3. 用例编写规范

- **命名规范**：`test_<功能>_<场景>_<预期结果>`，语义清晰，一眼看懂测试目的
- **异步测试**：所有异步方法测试必须使用@pytest.mark.asyncio装饰器
- **fixture规范**：通用测试数据、依赖封装为fixture，按作用域管理（function/module/session）
- **断言规范**：明确断言预期结果，禁止使用assert True、assert is not None等模糊断言
- **异常测试**：使用pytest.raises校验预期抛出的异常
- **示例**：

```python
# tests/integration/test_user_service.py
import pytest
from app.services.user_service import user_service
from app.schemas.user import UserCreate
from app.core.exceptions import NotFoundException, BusinessException
from app.core.db import async_session

@pytest.fixture(scope="function")
async def test_user():
    """测试用户fixture，测试结束后自动删除"""
    async with async_session() as session:
        user_in = UserCreate(username="test_user_001", password="Test@123456", phone="13800138000")
        user = await user_service.create_user(user_in=user_in)
        yield user
        # 测试结束清理数据
        await user_service.delete_user(user_id=user.id)

@pytest.mark.asyncio
async def test_get_user_by_id_success(test_user):
    """测试：根据ID获取用户，正常场景，返回正确用户信息"""
    # 执行测试
    user = await user_service.get_user_by_id(user_id=test_user.id)
    # 断言
    assert user.id == test_user.id
    assert user.username == test_user.username
    assert user.phone == test_user.phone

@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    """测试：根据ID获取用户，用户不存在，抛出NotFoundException"""
    with pytest.raises(NotFoundException):
        await user_service.get_user_by_id(user_id=99999999)

@pytest.mark.asyncio
async def test_create_user_username_exist(test_user):
    """测试：创建用户，用户名已存在，抛出BusinessException"""
    user_in = UserCreate(username=test_user.username, password="Test@654321", phone="13900139000")
    with pytest.raises(BusinessException):
        await user_service.create_user(user_in=user_in)
```

### 4. 测试运行规范

- 提交代码前必须本地运行测试，保证所有用例通过
- CI流水线必须自动运行全量测试，测试不通过禁止合并代码
- 定期生成覆盖率报告，排查未覆盖的业务场景
- 禁止跳过测试，特殊场景必须添加注释说明原因

---

## 七、代码提交规范

采用**Conventional Commits**规范，提交信息必须结构化，可追溯，可自动化生成CHANGELOG

### 1. 提交格式

```
<type>(<scope>): <subject>
```

### 2. 类型说明（type）

| 类型     | 说明                                                 |
| -------- | ---------------------------------------------------- |
| feat     | 新增功能、新特性                                     |
| fix      | 修复bug                                              |
| docs     | 文档更新（README、开发规范、API文档等）              |
| style    | 代码格式调整，不影响业务逻辑（空格、缩进、格式化等） |
| refactor | 代码重构，不新增功能、不修复bug                      |
| perf     | 性能优化                                             |
| test     | 测试用例新增、修改                                   |
| build    | 项目构建、依赖包变更                                 |
| ci       | CI/CD流水线配置变更                                  |
| chore    | 日常琐事、废弃代码清理、配置调整等不影响业务的变更   |
| revert   | 回滚之前的提交                                       |

### 3. 范围说明（scope）

可选，说明提交影响的模块，如api、services、user、order、db、celery等

### 4. 主题说明（subject）

- 简洁明了，说明本次提交的核心内容，不超过50个字符
- 中文描述，禁止无意义的提交信息（如“修改代码”、“更新”、“fix bug”）
- 结尾不加句号
- 一个提交只做一件事，禁止大杂烩提交

### 5. 正确示例

```
feat(user): 新增用户密码重置功能
fix(order): 修复订单支付状态更新的并发安全问题
docs: 更新开发规范文档，补充异步开发要求
style: 格式化代码，修复pylint警告
refactor(core): 重构全局异常处理器，统一异常响应格式
perf(db): 优化用户列表查询，添加复合索引
test(user): 新增用户模块集成测试用例
build: 更新SQLAlchemy版本到2.0.30
ci: 优化GitHub Actions流水线，添加测试覆盖率检查
chore: 清理废弃的接口和代码
revert: 回滚feat(user): 新增用户密码重置功能的提交
```

### 6. 强制禁止

- 提交密码、密钥、Token、环境变量等敏感信息
- 提交大文件、二进制文件、依赖包
- 提交未通过pylint检查、测试用例失败的代码
- 模糊的提交信息，如“修改代码”、“更新”、“修复bug”
- 一次提交包含多个不相关的功能/修复

### 7. 前置校验（pre-commit）

必须配置pre-commit钩子，提交代码前自动执行以下检查，不通过禁止提交：

1. black代码格式化
2. isort导入排序
3. pylint静态代码检查（评分≥9分）
4. mypy类型检查
5. 单元测试smoke校验
6. 敏感信息扫描

---

## 八、安全与运维规范

### 1. 安全规范

- **配置安全**：所有敏感配置（DB密码、API密钥、JWT密钥）必须从环境变量加载，禁止提交到git仓库
- **密码安全**：用户密码必须使用bcrypt/argon2加密存储，禁止明文、弱哈希算法
- **输入安全**：所有用户输入必须经过Pydantic校验，禁止未校验的输入进入业务层，防止注入攻击
- **鉴权安全**：所有敏感接口必须添加鉴权依赖，严格校验用户权限，禁止越权访问
- **输出安全**：敏感信息必须脱敏后返回/打印，禁止明文输出手机号、身份证、密码、Token
- **接口安全**：配置严格的CORS规则，禁止使用*通配符；接口添加限流，防止恶意攻击
- **审计日志**：所有敏感操作（登录、修改密码、删除数据）必须记录审计日志，可追溯

### 2. 部署规范

- **容器化部署**：使用Docker多阶段构建，减小镜像体积，禁止root用户运行服务
- **进程管理**：FastAPI生产环境使用gunicorn + uvicorn worker，worker数为CPU核心数*2+1
- **服务编排**：使用Kubernetes/docker-compose编排服务，实现高可用、弹性伸缩
- **监控告警**：使用Prometheus+Grafana监控服务指标，ELK/Loki收集日志，配置异常告警
- **健康检查**：配置服务健康检查接口，自动重启不健康的服务实例
- **灰度发布**：生产环境采用灰度发布，验证无误后全量上线，保留快速回滚能力

---

## 九、附录

### 1. 禁用清单

- 禁止使用同步requests库，必须使用httpx.AsyncClient
- 禁止使用同步DB驱动，必须使用SQLAlchemy 2.0异步模式
- 禁止使用print输出，必须使用loguru
- 禁止使用裸except，必须指定具体异常类型
- 禁止硬编码配置，必须使用Pydantic Settings
- 禁止手写参数校验，必须使用Pydantic v2
- 禁止手写重试逻辑，必须使用Tenacity
- 禁止mock内部核心依赖，测试必须使用真实实例

### 2. 参考文档

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Pydantic v2官方文档](https://docs.pydantic.dev/latest/)
- [PEP8 Python编码规范](https://peps.python.org/pep-0008/)
- [Conventional Commits规范](https://www.conventionalcommits.org/)
- [Celery官方文档](https://docs.celeryq.dev/)
- [LangGraph官方文档](https://langchain-ai.github.io/langgraph/)
