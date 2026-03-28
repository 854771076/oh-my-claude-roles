---
name: vue3-project-structure
description: Vue 3 企业级项目目录结构规范，定义标准的项目分层与目录组织方式
triggers:
- pattern: vue3.*(目录|结构|project structure|folder)
- pattern: (组织|安排)vue3.*项目结构
- pattern: init vue3.*project
---

# Vue 3 企业级项目目录结构规范

## 标准目录结构
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

## 目录职责说明

| 目录 | 职责说明 |
|------|----------|
| `public` | 存放不需要Vite处理的静态资源，直接复制到输出目录 |
| `src/assets` | 存放需要Vite处理的静态资源，会被打包处理 |
| `src/components` | 存放全局可复用的通用组件，按类型分类存放 |
| `src/composables` | 存放跨组件复用的无业务逻辑的组合式函数 |
| `src/hooks` | 存放业务相关的可复用Hook，和composables分层 |
| `src/directives` | 存放全局自定义指令 |
| `src/plugins` | 第三方插件的初始化配置代码 |
| `src/router` | 路由配置，按业务模块拆分，便于维护 |
| `src/store` | Pinia全局状态管理，按业务模块拆分 |
| `src/services` | 后端接口统一管理，所有API请求都放这里 |
| `src/types` | 全局通用的TypeScript类型定义 |
| `src/utils` | 通用工具函数，无业务依赖 |
| `src/views` | 页面级组件，按业务模块分组 |
| `src/constants` | 全局常量定义 |
| `tests` | 所有测试用例，分单元测试和E2E测试 |

## 最佳实践
1. **按业务分层**：每个层级职责清晰，不要越界
2. **按模块拆分**：大型项目按业务模块拆分配置和代码，便于多人协作
3. **统一管理接口**：所有后端API都放在services层，方便维护和修改
4. **抽离复用逻辑**：可复用的状态逻辑抽离到composables，不要写在组件内