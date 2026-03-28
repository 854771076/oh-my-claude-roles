---
name: 创建规范React组件
description: 根据规范创建符合要求的React组件文件
trigger: /create-component
---

# 创建规范React组件

根据规范创建Next.js项目中的React组件，执行以下步骤：

1. **判断组件类型**
   - 默认优先设计为服务端组件，仅当需要交互时才使用客户端组件
   - 仅以下场景添加`'use client'`声明：使用React Hooks、浏览器API、事件监听、Zustand状态管理

2. **文件命名与路径**
   - 组件文件使用PascalCase命名，后缀为`.tsx`
   - 公共组件放在`components/`目录，业务组件对应业务模块目录

3. **类型定义规范**
   - 组件Props使用PascalCase命名，禁止加`I`前缀
   - 所有props必须显式定义类型，优先使用type定义
   - 复杂props必须添加注释说明用途

4. **遵循开发规则**
   - 表单必须使用React Hook Form + Zod校验
   - 客户端数据请求必须使用TanStack Query
   - 客户端全局状态必须使用Zustand
   - 复杂组件必须配套编写单元测试，测试文件名为`[ComponentName].test.tsx`

## 检查要点
- ✅ 文件命名符合PascalCase.tsx规则
- ✅ 仅必要组件添加`'use client'`，客户端组件已最小化
- ✅ Props类型定义规范，无any类型，未使用I前缀
- ✅ 技术栈选择符合规范要求
- ✅ 已创建对应测试文件（核心组件）

---