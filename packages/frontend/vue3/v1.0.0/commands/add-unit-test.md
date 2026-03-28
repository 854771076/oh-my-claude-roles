<content>
---
name: 添加单元测试
description: 按照规范为Vue3项目核心逻辑添加单元测试
trigger: /vue3-add-test
---

## 执行步骤
1. 在对应目录创建测试文件，文件名格式为 `[被测文件名].test.ts`
2. 使用Vitest作为测试框架，遵循测试金字塔原则
3. 测试用例描述清晰表达测试场景
4. 只测试业务自定义逻辑，不测试Vue框架本身能力
5. 第三方依赖合理mock，核心业务不mock

## 测试模板
```typescript
import { describe, it, expect } from 'vitest'
import { usePagination } from '@/composables/usePagination'

describe('usePagination', () => {
  it('should initialize with correct first page', () => {
    const { currentPage, totalPages } = usePagination(100, 10)
    expect(currentPage.value).toBe(1)
    expect(totalPages.value).toBe(10)
  })

  it('should increment current page when call nextPage', () => {
    const { currentPage, nextPage } = usePagination(100, 10)
    nextPage()
    expect(currentPage.value).toBe(2)
  })
})
```

## 检查要点
- ✅ 测试文件命名符合规范，放在正确位置
- ✅ 测试用例描述清晰，覆盖正常/异常场景
- ✅ 核心业务逻辑覆盖率符合要求：核心业务≥80%，工具函数≥90%
- ✅ 只测试业务逻辑，不测试Vue原生能力
</content>

---