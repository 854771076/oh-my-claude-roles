---
name: Vue 3 测试规范
description: Vue 3 项目单元测试与E2E测试规范
triggers:
- ^.*vue3测试规范.*$
- ^.*vue3单元测试.*$
- ^.*vitest规范.*$
- ^.*cypress规范.*$
- ^.*vue3测试覆盖率.*$
---

# Vue 3 测试规范

## 核心测试原则

- 遵循测试金字塔：单元测试占比最大，其次是集成测试，最后是少量E2E测试
- 不测试Vue框架本身提供的能力，只测试业务自定义逻辑
- 核心业务逻辑必须写单元测试，第三方依赖可以mock，核心业务依赖不要mock

## 测试环境

- 单元测试使用Vitest，无需额外配置，兼容项目现有Vite配置
- E2E测试使用Cypress，本地开发可可视化调试，CI环境自动运行

## 测试命名规范

- 测试文件命名：被测文件名后加`.test`后缀，如`getUserInfo.test.ts`，`UserCard.test.vue`
- 测试用例描述清晰表达测试场景：`it('should return error when username is empty', () => {})`

## 覆盖率要求

- 核心业务模块单元测试覆盖率不低于80%
- 工具函数、通用组合式函数覆盖率不低于90%
- 页面组件核心交互流程需要覆盖E2E测试

## 单元测试示例

```ts
// composables/__tests__/usePagination.test.ts
import { usePagination } from '../usePagination'
import { describe, it, expect } from 'vitest'

describe('usePagination', () => {
  it('should initialize with default values correctly', () => {
    const { current, pageSize, total } = usePagination()
    expect(current.value).toBe(1)
    expect(pageSize.value).toBe(10)
    expect(total.value).toBe(0)
  })

  it('should change page correctly when call changePage', () => {
    const { current, changePage } = usePagination()
    changePage(5)
    expect(current.value).toBe(5)
  })

  it('should reset to first page when change page size', () => {
    const { current, pageSize, changePage, changePageSize } = usePagination()
    changePage(3)
    changePageSize(20)
    expect(pageSize.value).toBe(20)
    expect(current.value).toBe(1)
  })
})
```

---