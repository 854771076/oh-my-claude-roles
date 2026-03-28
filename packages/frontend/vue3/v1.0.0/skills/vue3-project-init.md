---
name: Vue 3 项目初始化规范
description: Vue 3 企业级项目初始化的技术选型与基础配置规范
triggers:
- ^.*vue3项目初始化.*$
- ^.*创建vue3项目.*$
- ^.*vue3技术选型.*$
- ^.*vue3项目结构.*$
---

# Vue 3 企业级项目初始化规范

## 核心技术栈推荐

| Technology | Version Requirements | Core Positioning |
| ---------- | --------------------- | ---------------- |
| Vue | 3.2+ | 核心前端框架，默认使用组合式API |
| Vite | 4.x+ | 官方推荐构建工具 |
| TypeScript | 4.8+ | 强制全项目类型支持 |
| Vue Router | 4.x | 路由管理 |
| Pinia | 2.x | 官方状态管理，替代Vuex |
| Axios | 1.x | HTTP请求库 |
| Tailwind CSS / UnoCSS | 最新稳定版 | 原子化CSS方案 |
| Element Plus / Ant Design Vue | 最新稳定版 | 企业级UI组件库 |
| VeeValidate / Zod | 最新稳定版 | 类型安全表单验证 |
| Vitest | 最新稳定版 | 单元测试框架 |
| Cypress | 最新稳定版 | E2E测试框架 |
| ESLint + Prettier | 最新稳定版 | 代码规范检查与格式化 |

## 企业级项目目录结构

```
project-root/
├── public/                # 静态资源文件
├── src/
│   ├── assets/            # 项目需要处理的静态资源
│   ├── components/        # 全局可复用通用组件
│   │   └── common/        # 基础通用组件
│   ├── composables/       # 全局可复用组合式函数
│   ├── directives/        # 全局自定义指令
│   ├── plugins/           # 第三方插件初始化配置
│   ├── router/            # 路由配置
│   │   └── modules/       # 按业务模块拆分路由
│   ├── store/             # Pinia全局状态管理
│   │   └── modules/       # 按业务模块拆分状态
│   ├── services/          # 接口请求层
│   │   └── modules/       # 按业务模块拆分接口
│   ├── types/             # 全局TypeScript类型定义
│   ├── utils/             # 全局工具函数
│   ├── views/             # 页面级组件
│   │   └── [business-module]/ # 按业务模块分组页面
│   ├── constants/         # 全局常量定义
│   ├── hooks/             # 业务级自定义Hook
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口文件
├── tests/
│   ├── unit/              # 单元测试
│   └── e2e/               # 端到端测试
├── .env.development       # 开发环境变量
├── .env.production        # 生产环境变量
├── .eslintrc.js           # ESLint配置
├── .prettierrc.js         # Prettier配置
├── vite.config.ts         # Vite配置
├── tsconfig.json          # TypeScript配置
└── package.json           # 依赖配置
```

## 核心开发铁则

1. **优先组合式API**：所有新组件强制使用`<script setup>`，不推荐选项式API开发新业务
2. **类型安全强制**：全业务代码使用TypeScript，禁止`any`类型滥用
3. **框架原生优先，不造重复轮子**：优先使用Vue官方生态，成熟社区库解决需求
4. **组件化优先**：抽离可复用组件，禁止上千行重复逻辑在页面组件
5. **按需引入，减小包体积**：所有第三方依赖禁止全量引入
6. **可测试性设计**：业务逻辑抽离为纯函数/组合式函数，禁止逻辑UI强耦合
7. **可维护性优先**：语义化命名，目录结构清晰，复杂逻辑加文档
8. **异步不阻塞**：所有IO操作使用async/await，禁止同步阻塞调用

---