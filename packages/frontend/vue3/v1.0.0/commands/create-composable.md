<content>
---
name: 创建组合式函数
description: 创建可复用的状态逻辑组合式函数，遵循类型安全规范
trigger: /vue3-create-composable
---

## 执行步骤
1. 在 `src/composables/` 目录创建文件，小驼峰命名，前缀一般用use（如`usePagination.ts`）
2. 编写函数，只关注一个关注点，抽离复用状态逻辑
3. 为入参和返回值添加明确的TypeScript类型定义
4. 返回响应式状态和操作方法，支持按需引入

## 代码模板
```typescript
import { ref, computed } from 'vue'

/**
 * 分页逻辑复用组合式函数
 * @param total 总条数
 * @param pageSize 每页大小
 */
export function usePagination(total: number, pageSize: number = 10) {
  const currentPage = ref(1)
  const totalPages = computed(() => Math.ceil(total / pageSize))

  function nextPage() {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  function prevPage() {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  return {
    currentPage,
    totalPages,
    nextPage,
    prevPage
  }
}
```

## 检查要点
- ✅ 命名符合 `useXXX` 规范，文件放在composables目录
- ✅ 每个组合式函数只关注一个关注点
- ✅ 入参出参都有完整类型定义，未使用any
- ✅ 返回响应式状态，可在组件中正常使用
</content>

---