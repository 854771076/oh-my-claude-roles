<content>
---
name: 创建页面组件
description: 按照规范创建符合Vue3企业级开发标准的页面级组件
trigger: /vue3-create-page
---

## 执行步骤
1. 在 `src/views/[业务模块]/` 目录下创建组件文件，使用帕斯卡命名法命名
2. 使用标准 `<script setup lang="ts">` 组合式API语法
3. 处理路由参数验证，非法参数跳转错误页
4. 只做页面布局组装，复杂业务逻辑抽离到composables或service层
5. 大型页面开启路由懒加载配置

## 代码模板
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
// 第三方库导入
// 空行分隔 → 全局导入
// 空行分隔 → 本地模块导入

const route = useRoute()
// 验证路由参数
const id = Number(route.params.id)
if (Number.isNaN(id)) {
  // 跳转404错误页
}

// 声明响应式状态，禁止滥用any
const isLoading = ref(false)

// 页面逻辑，抽离复用逻辑到composables
</script>

<template>
  <!-- 页面布局 -->
</template>
```

## 检查要点
- ✅ 强制使用 `<script setup>` 组合式API
- ✅ 文件名使用帕斯卡命名法
- ✅ 路由参数做了合法性校验
- ✅ 复杂逻辑已抽离，单文件代码不超过500行
- ✅ 所有变量/数据有明确类型定义，未滥用any
</content>

---