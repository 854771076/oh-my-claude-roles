---
name: Vue 3 核心模块开发规范
description: Vue 3 各核心模块（页面、组件、组合式函数、状态管理等）开发规范
triggers:
- ^.*vue3模块开发.*$
- ^.*vue3组件开发规范.*$
- ^.*pinia开发规范.*$
- ^.*vue3接口管理.*$
- ^.*vue3路由规范.*$
---

# Vue 3 核心模块开发规范

## 5.1 页面组件（views目录）

- 负责页面级布局组装，调用业务组件，不处理复杂业务逻辑，逻辑抽离到composables或service层
- 路由参数验证必须在页面进入时完成，非法参数直接跳转错误页

示例：
```vue
<script setup lang="ts">
// 只做组装，不写复杂业务逻辑
import { onBeforeRouteLeave } from 'vue-router'
import UserProfile from '../components/UserProfile.vue'
import UserOrderList from '../components/UserOrderList.vue'
import { useUserDetail } from '../hooks/useUserDetail'

const { userId, userInfo } = useUserDetail()
// 参数验证已经抽离到hook中
</script>

<template>
  <div class="user-detail-page">
    <UserProfile :user-info="userInfo" />
    <UserOrderList :user-id="userId" />
  </div>
</template>
```

## 5.2 通用组件（components目录）

- 遵循单一职责原则，一个组件只做一件事
- props必须定义类型、默认值，emit必须定义类型校验
- 尽量使用`v-model`双向绑定语法，符合Vue 3官方规范
- 通用组件不能依赖业务逻辑，保证可复用性

示例：
```vue
<script setup lang="ts">
import type { PropType, ExtractPropTypes } from 'vue'

const props = defineProps({
  modelValue: {
    type: String as PropType<string>,
    default: ''
  },
  placeholder: {
    type: String,
    default: '请输入'
  }
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
}>()

const handleInput = (e: Event) => {
  const value = (e.target as HTMLInputElement).value
  emit('update:modelValue', value)
}
</script>
```

## 5.3 组合式函数（composables目录）

- 抽离复用的状态逻辑，每个组合式函数只关注一个关注点
- 支持按需引入，返回清晰的响应式状态和方法，必须添加类型定义

示例：
```ts
// composables/usePagination.ts
import { ref, computed } from 'vue'

export interface PaginationOptions {
  defaultPageSize?: number
}

export function usePagination(options: PaginationOptions = {}) {
  const { defaultPageSize = 10 } = options
  const current = ref(1)
  const pageSize = ref(defaultPageSize)
  const total = ref(0)

  const offset = computed(() => (current.value - 1) * pageSize.value)

  const changePage = (page: number) => {
    current.value = page
  }

  const changePageSize = (size: number) => {
    pageSize.value = size
    current.value = 1
  }

  const reset = () => {
    current.value = 1
    total.value = 0
  }

  return {
    current,
    pageSize,
    total,
    offset,
    changePage,
    changePageSize,
    reset
  }
}
```

## 5.4 状态管理（store目录，Pinia）

- 按业务模块拆分store，每个模块只维护对应业务的全局状态
- 不存储冗余状态，冗余数据可以从组件内计算得到的不要存在store中
- 异步操作统一在store的action中处理，不直接在组件中修改状态

示例：
```ts
// store/modules/user.ts
import { defineStore } from 'pinia'
import type { IUserInfo } from '@/types/user'
import { getUserInfoApi } from '@/services/modules/user'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null as IUserInfo | null
  }),
  actions: {
    async fetchUserInfo(userId: number) {
      const res = await getUserInfoApi(userId)
      this.userInfo = res.data
      return res.data
    },
    clearUserInfo() {
      this.userInfo = null
    }
  }
})
```

## 5.5 接口层（services目录）

- 所有后端接口统一在services中管理，不允许在组件中直接写请求地址和请求配置
- 接口入参出参必须定义明确的TypeScript类型，统一处理接口错误，返回可处理的结果

示例：
```ts
// services/modules/user.ts
import request from '@/plugins/request'
import type { IUserInfo, GetUserInfoParams } from '@/types/user'

export const getUserInfoApi = (params: GetUserInfoParams): Promise<IUserInfo> => {
  return request.get('/api/user/info', { params })
}

export const updateUserInfoApi = (data: Partial<IUserInfo>): Promise<void> => {
  return request.post('/api/user/update', data)
}
```

## 5.6 路由（router目录）

- 按业务模块拆分路由配置，统一注册，大型项目支持路由懒加载优化首屏加载速度
- 路由守卫统一处理权限验证、登录状态校验，不分散到组件中处理

示例：
```ts
// router/modules/user.ts
export default [
  {
    path: '/user',
    name: 'User',
    component: () => import('@/layouts/BaseLayout.vue'),
    meta: {
      title: '用户管理',
      requiresAuth: true
    },
    children: [
      {
        path: 'list',
        name: 'UserList',
        component: () => import('@/views/user/UserList.vue'),
        meta: {
          title: '用户列表'
        }
      }
    ]
  }
]
```

---