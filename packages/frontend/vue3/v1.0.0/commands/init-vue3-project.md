---
name: 初始化Vue3项目
description: 根据企业级规范初始化一个标准Vue3项目，生成推荐目录结构和基础配置
trigger: /vue3-init
---

## 执行步骤
1. 推荐使用 `npm create vite@latest` 初始化项目，选择 Vue + TypeScript 模板
2. 按照文档中提供的**企业级项目目录结构**创建所有标准目录
3. 安装推荐生产级依赖：
   - Vue Router 4.x、Pinia 2.x、Axios 1.x
   - 选择UI组件库（Element Plus / Ant Design Vue）
   - 选择原子化CSS方案（Tailwind CSS / UnoCSS）
   - 配置ESLint + Prettier
4. 初始化基础配置文件：
   - 拆分多环境环境变量文件 `.env.development` 和 `.env.production`
   - 配置 `vite.config.ts` 开启路径别名、按需引入优化
   - 配置 `tsconfig.json` 开启严格类型检查
5. 生成根入口 `main.ts` 和 `App.vue` 基础模板

## 检查要点
- ✅ 目录结构严格匹配文档规范，按业务模块拆分路由、store、services
- ✅ 已经开启TypeScript严格模式，禁用隐式any
- ✅ 基础依赖版本符合文档要求
- ✅ 敏感信息预留环境变量注入位置，未硬编码

---