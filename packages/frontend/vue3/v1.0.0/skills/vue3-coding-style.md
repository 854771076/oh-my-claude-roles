---
name: Vue 3 代码书写规范
description: Vue 3 项目代码书写命名、注释、格式规范
triggers:
- ^.*vue3代码规范.*$
- ^.*vue3命名规范.*$
- ^.*vue3书写规范.*$
- ^.*vue3风格指南.*$
---

# Vue 3 代码书写规范

## 命名规范

| 类型 | 规范 | 示例 |
| ---- | ---- | ---- |
| 组件文件 | 帕斯卡命名法 | `UserCard.vue` |
| 工具/类型/常量文件 | 小驼峰 | `userUtils.ts` |
| 页面文件 | 帕斯卡命名法 | `UserDetail.vue` |
| 变量 | 小驼峰 | `const userName = ref('')` |
| 常量 | 全大写下划线分割 | `const MAX_PAGE_SIZE = 20` |
| 函数/方法 | 小驼峰，动词开头 | `getUserInfo`, `handleSubmit` |
| 组件 | 帕斯卡命名法，多个单词 | `UserProfile` 而非 `up` |
| 接口 | 前缀`I`，帕斯卡 | `interface IUserInfo {}` |
| 类型 | 帕斯卡 | `type UserStatus = 'active' | 'inactive'` |

## 注释规范

- 公共组件、工具函数、组合式函数必须添加功能说明、入参出参说明
- 复杂业务逻辑必须添加行内注释说明设计意图
- 不要注释显而易见的代码
- 文件头部不需要添加创建者、创建时间冗余注释，由Git管理版本
- TODO注释格式：`// TODO: 处理分页逻辑错误 @zhangsan`

## 格式化规则

- 缩进使用2个空格，不使用Tab
- 单文件代码行数不超过500行，超过必须拆分
- 导入顺序：第三方库导入 → 全局工具/类型导入 → 本地组件/模块导入，组之间空一行分隔
- 字符串优先使用单引号，JSX/模板属性使用双引号

示例：
```ts
// 第三方库导入
import { ref, computed } from 'vue'
import { useStore } from 'pinia'

// 全局工具/类型导入
import type { IUserInfo } from '@/types/user'
import { formatDate } from '@/utils/date'

// 本地组件/模块导入
import UserCard from './components/UserCard.vue'
import { useUserStore } from '@/store/modules/user'
```

## 禁止行为

- 禁止在代码中写死生产环境接口地址，所有环境配置必须通过环境变量注入
- 禁止`console.log`打印调试信息提交到主线分支
- 禁止滥用`any`类型绕过类型检查
- 禁止将所有状态放到全局store，组件内状态尽量组件内部维护

---