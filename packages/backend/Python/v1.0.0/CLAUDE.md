# Python企业级后端开发规范与最佳实践

**版本**: v1.0.0
**适用范围**: Python 3.14 + 全异步企业级后端项目
**核心原则**: 能异步都异步、有框架用框架不手写重复代码、强类型安全、可测试、可维护、高性能

---

## 核心技术栈要求

严格遵循「不重复造轮子」原则，禁止手写替代框架已有能力的代码：

| 技术组件              | 版本要求   | 核心使用规范                                                                     |
| --------------------- | ---------- | -------------------------------------------------------------------------------- |
| Python                | 3.14+      | 强制使用新特性类型提示、优化异步性能，禁止使用3.14以下版本               |
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

## 核心开发铁则（最高优先级）

### 1. 能异步都异步
- 强制全链路异步：所有IO密集型操作必须使用异步库+async/await语法，禁止同步阻塞代码进入异步事件循环
- 禁止异步陷阱：
  - 禁止在异步函数中调用同步IO操作（如同步requests、同步DB驱动、同步open）
  - 禁止在异步函数中使用time.sleep，必须使用asyncio.sleep
  - 禁止在同步上下文中直接调用异步函数，必须通过asyncio.run或线程池隔离
  - CPU密集型操作必须交给Celery任务执行，禁止阻塞FastAPI主事件循环
- 异步边界规范：FastAPI路由→Service层→CRUD层→数据库/缓存/网络，全链路保持异步，无同步断点

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

## 企业级项目目录结构

严格遵循分层架构，职责单一，边界清晰，禁止跨层调用：

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

## 代码书写规范

### 命名规范（严格遵循PEP8）

| 命名对象    | 规范要求                                                             |
| ----------- | -------------------------------------------------------------------- |
| 项目/包名   | 全小写，下划线分隔，禁止大写、点号                                   |
| 文件名      | 全小写，下划线分隔，动词/名词清晰                                    |
| 变量名      | 蛇形命名，全小写，下划线分隔，语义优先，禁止拼音、单字母（循环除外） |
| 函数/方法名 | 蛇形命名，全小写，动词开头，语义优先，异步函数无需加async前缀        |
| 类名        | 大驼峰命名，每个单词首字母大写，职责清晰                             |
| 常量名      | 全大写，下划线分隔，统一放在constants目录                            |
| 私有成员    | 模块/类内部使用的成员，单下划线开头，禁止双下划线（名称改写）        |
| 异常类      | 大驼峰，以Exception结尾                                              |
| 枚举类      | 大驼峰，以Enum结尾                                                   |

**强制禁止**：
- 拼音命名（通用行业术语除外）
- 无意义命名：a、b、temp、data、info等模糊命名
- 缩写不统一
- 关键字冲突：禁止使用id、type、class、def等Python关键字作为变量名，可加后缀如user_id

### 注释规范

采用Google风格注释，核心原则：**必要注释，拒绝冗余，业务逻辑必注释，自解释代码不注释**

- **文件头部注释**：每个py文件开头必须添加，说明文件职责、作者、创建时间
- **类注释**：必须说明类职责、属性含义
- **函数/方法注释**：所有非私有函数、对外接口、复杂业务函数必须添加，包含Args、Returns、Raises
- **TODO注释**：必须带【责任人】【创建日期】【截止日期】【需求说明】，禁止无归属TODO
- 禁止注释掉的代码，废弃代码直接删除；禁止冗余无意义注释

### 代码格式规范

- 行宽限制：单行最大120字符，超过自动换行
- 缩进规范：4个空格缩进，禁止使用tab
- 空行规范：函数/类之间空2行，类内方法之间空1行，逻辑块之间空1行，禁止连续空行
- 导入规范：
  - 导入顺序：标准库 → 第三方库 → 内部模块，每组之间空1行
  - 禁止使用 `from xxx import *` 通配符导入
  - 禁止循环导入，使用isort自动格式化导入顺序
- 字符串规范：单行字符串用双引号，多行用三双引号，拼接优先使用f-string，禁止用+拼接大量字符串
- 语法规范：
  - 禁止使用全局变量，有状态对象必须通过依赖注入管理
  - 禁止使用eval、exec等危险函数
  - 禁止魔法数字，所有固定值必须定义为常量
  - 函数参数必须指定类型提示，返回值必须指定类型提示，禁止Any类型（特殊场景除外）
  - 单个函数圈复杂度必须≤10，超过必须拆分

---

## 核心模块开发规范

### 1. FastAPI接口开发规范
- 路由分层：禁止在main.py中写接口，必须按业务模块拆分到endpoints，按版本管理
- 职责单一：接口层仅负责参数接收、鉴权校验、调用service层、响应返回，禁止写业务逻辑
- 依赖注入：所有重复逻辑必须封装为依赖，通过Depends注入
- 类型安全：所有入参必须指定Pydantic模型，所有出参必须指定response_model，禁止无类型响应
- 接口规范：
  - RESTful风格：GET（查询）、POST（创建）、PUT（全量更新）、PATCH（部分更新）、DELETE（删除）
  - 路径命名：全小写，下划线分隔，版本前缀，如 `/api/v1/users/{user_id}`
  - 统一响应格式：所有接口返回统一结构 `{"code": 200, "msg": "success", "data": {}}`

### 2. Pydantic v2开发规范
- 模型分层：入参模型（Create/Update）、出参模型（Out/Resp）、内部模型（Base）严格拆分
- 强制校验：
  - 所有模型必须设置 `model_config = ConfigDict(extra="forbid")`，禁止传入未定义字段
  - 字符串字段必须设置strip_whitespace=True，自动去除首尾空格
  - 所有字段必须添加类型提示，禁止Any类型
  - 格式校验必须通过field_validator实现，禁止业务层手写校验
- 序列化规范：
  - 出参模型必须设置from_attributes=True，支持ORM对象自动序列化
  - 敏感字段必须设置exclude=True，禁止返回给前端
  - 使用model_dump()进行序列化，禁止使用旧版dict()方法

### 3. 业务层（Services）开发规范
- 唯一业务层：所有业务逻辑、规则判断、事务管理必须写在services层，禁止分散到api/crud层
- 全异步实现：所有方法必须为async异步方法，调用crud/第三方接口必须使用await
- 职责边界：允许跨CRUD、跨services调用，禁止直接操作数据库，禁止直接返回响应给前端
- 事务管理：多表操作必须开启事务，异常时自动回滚

### 4. 数据访问层（CRUD）开发规范
- 单表职责：每个CRUD类仅负责对应单表的增删改查，禁止多表关联、业务逻辑
- 全异步实现：所有方法必须为async异步方法，使用SQLAlchemy 2.0异步模式
- 通用基类：所有CRUD类必须继承通用BaseCRUD基类，复用基础增删改查能力，禁止重复代码
- 禁止原生SQL拼接，必须使用ORM参数化查询，防止SQL注入

### 5. Celery异步任务开发规范
- 职责边界：任务层仅负责任务调度、重试、异常处理，业务逻辑必须调用services层
- 幂等性要求：所有任务必须保证幂等，重复执行不会产生副作用
- 参数规范：任务参数仅支持可序列化的基础类型，禁止传递大对象、DB连接、文件句柄
- 重试规范：指定重试异常类型、最大次数、退避策略，禁止无限重试
- 队列拆分：按任务类型拆分队列，避免互相阻塞
- 结果管理：不需要的任务结果必须设置ignore_result=True，减少存储压力

### 6. LangChain+LangGraph开发规范
- 封装隔离：所有LLM相关逻辑必须封装在services/llm目录下，禁止与业务代码耦合
- 提示词管理：所有提示词必须放在独立的prompts目录下，禁止硬编码在代码中
- 工具封装：所有外部工具必须继承LangChain BaseTool，统一接口、异常处理、日志
- 状态管理：复杂智能体必须使用LangGraph StateGraph管理状态，禁止使用全局变量
- 重试与限流：所有大模型调用必须使用Tenacity做重试，记录token消耗
- 安全校验：大模型输入、输出必须做内容安全校验，防止敏感内容、注入攻击

### 7. Typer CLI开发规范
- 命令拆分：按功能模块拆分命令，禁止写超长单文件命令
- 参数校验：所有参数必须添加帮助文档、类型提示，复杂参数使用Pydantic模型校验
- 用户体验：敏感参数必须使用hide_input=True，确认提示
- 异常处理：友好处理异常，