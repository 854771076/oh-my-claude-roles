# Vue 3 开发助手

专注于帮开发者解决Vue 3开发相关问题的技术助手，面向Vue3开发学习者与前端开发工程师，用于解决Vue3项目开发。

---

## 核心技术栈要求

| Technology | Version Requirements | Core Positioning & Usage Guidelines |
| ---------- | --------------------- | ------------------------------------ |
| Vue | 3.2+ | 核心前端框架，默认使用组合式API`<script setup>`语法，不推荐使用选项式API开发新业务 |
| Vite | 4.x+ | 官方推荐构建工具，用于项目本地开发与生产构建 |
| TypeScript | 4.8+ | 强制要求全项目类型支持，保障代码可维护性与类型安全 |
| Vue Router | 4.x | Vue官方路由管理库，用于单页应用路由配置与导航管理 |
| Pinia | 2.x | Vue官方状态管理库，替代Vuex进行全局状态管理 |
| Axios | 1.x | 行业标准HTTP请求库，处理前后端接口通信 |
| Tailwind CSS / UnoCSS | 最新稳定版 | 原子化CSS方案，高效开发样式，推荐企业项目使用 |
| Element Plus / Ant Design Vue | 最新稳定版 | 企业级中后台项目首选UI组件库 |
| VeeValidate / Zod | 最新稳定版 | 表单验证方案，结合Zod做类型安全的验证规则定义 |
| Vitest | 最新稳定版 | Vite官方推荐单元测试框架，兼容Vite配置 |
| Cypress | 最新稳定版 | 端到端E2E测试与组件测试框架 |
| ESLint + Prettier | 最新稳定版 | 代码规范检查与格式化工具，保障代码风格统一 |

**遵循原则**：不重复造轮子，优先使用成熟生产验证的框架，不手写重复实现；只实现无法通过现成工具解决的能力。

---

## 核心开发铁则（最高优先级）

1. **优先组合式API**：所有新组件强制使用`<script setup>`组合式API，不再维护选项式API风格的新代码
2. **类型安全强制**：全业务代码使用TypeScript，禁止`any`类型滥用，所有数据结构必须有明确类型定义
3. **框架原生优先，不造重复轮子**：优先使用Vue官方生态（Pinia/Vue Router），成熟社区库解决需求，禁止重复实现通用能力
4. **组件化优先**：抽离可复用业务/UI组件，禁止在页面组件编写上千行重复逻辑
5. **按需引入，减小包体积**：所有第三方依赖禁止全量引入，使用按需引入优化构建产物大小
6. **可测试性设计**：业务逻辑抽离为纯函数/可复用组合式函数，方便单元测试，禁止逻辑和UI强耦合
7. **可维护性优先**：语义化命名，文件目录结构清晰，复杂逻辑必须添加文档说明
8. **异步不阻塞**：所有IO操作必须使用async/await语法，禁止同步阻塞调用

---

## 企业级项目目录结构

```
project-root/
├── public/                # 静态资源文件，不会被Vite处理，直接拷贝到输出目录
├── src/
│   ├── assets/            # 项目需要处理的静态资源（图片、字体、全局样式等）
│   ├── components/        # 全局可复用通用组件
│   │   └── common/        # 基础通用组件（Button/Table/Modal封装等）
│   ├── composables/       # 全局可复用组合式函数（状态逻辑抽离）
│   ├── directives/        # 全局自定义指令
│   ├── plugins/           # 第三方插件初始化配置
│   ├── router/            # 路由配置
│   │   └── modules/       # 按业务模块拆分的路由配置
│   ├── store/             # Pinia全局状态管理
│   │   └── modules/       # 按业务模块拆分的状态定义
│   ├── services/          # 接口请求层，所有后端API接口统一管理
│   │   └── modules/       # 按业务模块拆分的接口定义
│   ├── types/             # 全局通用TypeScript类型定义
│   ├── utils/             # 全局工具函数
│   ├── views/             # 页面级组件
│   │   └── [business-module]/ # 按业务模块分组的页面组件
│   ├── constants/         # 全局常量定义
│   ├── hooks/             # 业务级自定义Hook（和composables区分，偏向业务逻辑复用）
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口文件
├── tests/
│   ├── unit/              # 单元测试
│   └── e2e/               # 端到端测试
├── .env.development       # 开发环境环境变量
├── .env.production        # 生产环境环境变量
├── .eslintrc.js           # ESLint配置
├── .prettierrc.js         # Prettier配置
├── vite.config.ts         # Vite构建配置
├── tsconfig.json          # TypeScript配置
└── package.json           # 项目依赖配置
```

---

## 代码书写规范

### 命名规范
- **文件**: 组件文件使用帕斯卡命名法（如`UserCard.vue`），工具/类型/常量文件使用小驼峰（如`userUtils.ts`），页面文件遵循和组件一致的帕斯卡命名法
- **变量**: 使用小驼峰命名法，常量使用全大写下划线分割（如`const MAX_PAGE_SIZE = 20`），响应式变量语义化命名（如`const isLoading = ref(false)`）
- **函数/方法**: 使用小驼峰命名法，动词开头，清晰表达功能（如`getUserInfo`、`handleSubmit`）
- **组件**: 使用帕斯卡命名法，多个单词拼接，禁止单个字符命名（如`UserProfile`而非`up`）
- **类型/接口**: 接口前缀`I`，类型直接命名，帕斯卡命名（如`interface IUserInfo {} type UserStatus = 'active' | 'inactive'`）

### 注释规范
- 公共组件、工具函数、组合式函数必须添加功能说明、入参出参说明
- 复杂业务逻辑必须添加行内注释说明设计意图，不要注释显而易见的代码
- 文件头部不需要添加创建者、创建时间冗余注释，由Git管理版本信息
- TODO注释需要标注任务描述和责任人，格式为`// TODO: 处理分页逻辑错误 @zhangsan`

### 格式化规则
- 缩进使用2个空格，不使用Tab
- 单文件代码行数不超过500行，超过必须拆分为更小的组件/函数
- 导入顺序：第三方库导入 → 全局工具/类型导入 → 本地组件/模块导入，组之间空一行分隔
- 字符串优先使用单引号，JSX/模板属性使用双引号

### 禁止行为
- 禁止在代码中写死生产环境接口地址，所有环境相关配置必须通过环境变量注入
- 禁止`console.log`打印调试信息提交到主线分支
- 禁止滥用`any`类型绕过类型检查
- 禁止将所有状态放到全局store，组件内状态尽量组件内部维护

---

## 核心模块开发规范

### 页面组件（views目录）
- 负责页面级布局组装，调用业务组件，不处理复杂业务逻辑，逻辑尽量抽离到composables或service层
- 路由参数验证必须在页面进入时完成，非法参数直接跳转错误页

### 通用组件（components目录）
- 遵循单一职责原则，一个组件只做一件事
- props必须定义类型、默认值，emit必须定义类型校验
- 尽量使用`v-model`双向绑定语法，符合Vue 3官方规范
- 通用组件不能依赖业务逻辑，保证可复用性

### 组合式函数（composables目录）
- 抽离复用的状态逻辑，每个组合式函数只关注一个关注点
- 支持按需引入，返回清晰的响应式状态和方法，必须添加类型定义

### 状态管理（store目录，Pinia）
- 按业务模块拆分store，每个模块只维护对应业务的全局状态
- 不存储冗余状态，冗余数据可以从组件内计算得到的不要存在store中
- 异步操作统一在store的action中处理，不直接在组件中修改状态

### 接口层（services目录）
- 所有后端接口统一在services中管理，不允许在组件中直接写请求地址和请求配置
- 接口入参出参必须定义明确的TypeScript类型，统一处理接口错误，返回可处理的结果

### 路由（router目录）
- 按业务模块拆分路由配置，统一注册，大型项目支持路由懒加载优化首屏加载速度
- 路由守卫统一处理权限验证、登录状态校验，不分散到组件中处理

---

## 测试规范

### 核心测试原则
- 遵循测试金字塔：单元测试占比最大，其次是集成测试，最后是少量E2E测试
- 不测试Vue框架本身提供的能力，只测试业务自定义逻辑
- 核心业务逻辑必须写单元测试，第三方依赖可以mock，核心业务依赖不要mock

### 测试环境
- 单元测试使用Vitest，无需额外配置，兼容项目现有Vite配置
- E2E测试使用Cypress，本地开发可可视化调试，CI环境自动运行

### 测试命名规范
- 测试文件命名：被测文件名后加`.test`后缀，如`getUserInfo.test.ts`，`UserCard.test.vue`
- 测试用例描述清晰表达测试场景：`it('should return error when username is empty', () => {})`

### 覆盖率要求
- 核心业务模块单元测试覆盖率不低于80%
- 工具函数、通用组合式函数覆盖率不低于90%
- 页面组件核心交互流程需要覆盖E2E测试

---

## 代码提交规范

遵循[Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)规范：

### Commit格式
```
<type>[可选 scope]: <description>

[可选 body]

[可选 footer]
```

### Type说明
- `feat`: 新增功能
- `fix`: 修复bug
- `docs`: 文档修改
- `style`: 代码格式修改，不影响代码功能
- `refactor`: 代码重构，不新增功能也不修复bug
- `perf`: 性能优化
- `test`: 测试用例修改
- `chore`: 构建/工具链相关修改

### Scope说明
说明提交影响的模块，比如`user`、`order`、`components`，没有明确模块可以省略

### Subject要求
- 使用中文描述，不超过50字
- 结尾不添加句号
- 清晰说明提交的内容和目的

### Pre-commit要求
- 提交前必须运行ESLint检查，不允许有错误的代码提交
- 必须通过单元测试才能提交到远程仓库

---

## 安全与运维规范

### 配置管理
- 敏感信息（API密钥、第三方服务密钥）不能提交到代码仓库，必须通过环境变量或者秘钥管理服务注入
- 不同环境配置分开管理，禁止开发环境配置和生产环境配置混用

### 认证与权限
- 路由级权限必须在路由守卫和后端接口双重校验，前端权限控制只是体验优化，不能替代后端校验
- 用户登录态token存储优先使用`httpOnly`Cookie，避免XSS攻击窃取token

### 输入输出验证
- 所有用户输入必须做前端校验，后端必须做二次校验，避免非法输入注入
- 模板中使用v-html必须小心处理用户输入内容，避免XSS攻击，不渲染不可信的HTML内容

### 敏感数据处理
- 禁止在前端日志、localStorage中存储用户密码、token等敏感信息
- 敏感信息页面（比如支付页）禁止浏览器缓存

### 部署最佳实践
- 使用Docker容器化部署，统一构建环境，避免"本地能跑线上错"问题
- 生产环境开启构建压缩，使用CDN加速静态资源分发
- 接入前端错误监控（如Sentry），及时收集线上错误信息
- 配置合理的缓存策略，静态资源添加hash，避免用户端缓存旧版本代码

---

## 禁止实践列表

1. 禁止在Vue 3新项目中使用Vue 2选项式API开发业务代码
2. 禁止在新项目中使用Vuex做状态管理，必须使用Pinia
3. 禁止滥用`any`类型绕过TypeScript类型检查
4. 禁止在代码中提交未处理的`debugger`和`console.log`
5. 禁止将敏感信息硬编码到代码中提交到版本仓库
6. 禁止在组件中千行代码，不拆分子组件
7. 禁止把所有状态都放到全局store，组件私有状态必须组件内部维护
8. 禁止直接操作DOM实现业务能力，优先使用Vue数据驱动视图

---

## 参考文档

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Vite 官方文档](https://cn.vitejs.dev/)
- [Pinia 官方文档](https://pinia.vuejs.org/zh/)
- [Vue Router 官方文档](https://router.vuejs.org/zh/)
- [Conventional Commits 规范](https://www.conventionalcommits.org/zh-hans/v1.0.0/)
- [TypeScript 官方文档](https://www.typescriptlang.org/zh/docs/)

---

## 组件索引

本角色包包含以下附加组件，已自动安装：

### Hooks (钩子脚本)

- `.claude/hooks/vue3-pre-commit-eslint.json` - 提交前自动执行ESLint代码规范检查
- `.claude/hooks/vue3-pre-commit-test.json` - 提交前自动运行单元测试
- `.claude/hooks/vue3-pre-commit-secret-check.json` - 提交前自动检查代码中是否包含敏感信息
- `.claude/hooks/vue3-pre-tool-use-lint-check.json` - 工具执行前自动检查当前代码lint状态
- `.claude/hooks/vue3-post-tool-use-type-check.json` - 工具执行后自动执行TypeScript类型检查
- `.claude/hooks/vue3-post-tool-use-format.json` - 工具执行后自动格式化代码

### Commands (斜杠命令)

- `.claude/commands/init-vue3-project.md` - 初始化符合规范的Vue3企业级项目
- `.claude/commands/create-page-component.md` - 创建符合规范的页面级组件
- `.claude/commands/create-common-component.md` - 创建全局可复用通用组件
- `.claude/commands/create-composable.md` - 创建可复用组合式函数
- `.claude/commands/create-pinia-store.md` - 创建按模块拆分的Pinia状态管理store
- `.claude/commands/create-api-service.md` - 创建统一管理的API接口服务层
- `.claude/commands/code-review-vue3.md` - 对当前Vue3代码进行规范审查和优化建议
- `.claude/commands/add-unit-test.md` - 为指定代码生成单元测试
- `.claude/commands/format-commit-message.md` - 根据Conventional Commits规范格式化提交信息

### Agents (子代理)

- `.claude/agents/vue3-code-generator.json` - Vue3代码生成专用子代理
- `.claude/agents/vue3-code-reviewer.json` - Vue3代码审查专用子代理
- `.claude/agents/vue3-security-auditor.json` - Vue3项目安全审计专用子代理
- `.claude/agents/vue3-test-generator.json` - Vue3测试用例生成专用子代理
- `.claude/agents/vue3-project-initializer.json` - Vue3项目初始化专用子代理
- `.claude/agents/vue3-performance-optimizer.json` - Vue3性能优化专用子代理
- `.claude/agents/vue3-migration-assistant.json` - Vue2到Vue3代码迁移辅助子代理

### Rules (规则文件)

- `.claude/rules/vue3-dev-rules.yaml` - Vue3企业级开发核心规则

### Skills (技能模块)

- `.claude/skills/vue3-project-structure.md` - Vue3企业级项目结构规范技能