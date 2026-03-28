<content>
---
name: 创建Pinia状态模块
description: 按照规范创建Pinia全局状态管理模块
trigger: /vue3-create-store
---

## 执行步骤
1. 在 `src/store/modules/` 目录创建文件，按业务模块拆分
2. 使用Pinia setup组合式语法定义store
3. 只存储当前业务模块需要的全局状态，不存储冗余数据
4. 异步操作统一放在action中处理，不直接在组件修改状态

## 代码模板
```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { IUserInfo } from '@/types/user'

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<IUserInfo | null>(null)

  const isLogin = computed(() => userInfo.value !== null)

  async function fetchUserInfo() {
    // 异步逻辑在这里处理
  }

  function clearUserInfo() {
    userInfo.value = null
  }

  return {
    userInfo,
    isLogin,
    fetchUserInfo,
    clearUserInfo
  }
})
```

## 检查要点
- ✅ 按业务模块拆分，每个store只对应一个业务领域
- ✅ 使用setup组合式语法，而非选项式语法
- ✅ 不存储可通过计算得到的冗余状态
- ✅ 异步操作都在action中处理
- ✅ 状态有明确的TypeScript类型定义
</content>

---