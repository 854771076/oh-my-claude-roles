<content>
---
name: 定义API接口服务
description: 统一管理后端API接口，添加类型定义和错误处理
trigger: /vue3-create-api
---

## 执行步骤
1. 在 `src/services/modules/` 目录按业务模块创建接口文件
2. 为每个接口的入参和出参定义明确的TypeScript类型
3. 统一封装axios请求，统一处理错误
4. 组件中只调用service导出的接口方法，不直接写axios请求

## 代码模板
```typescript
import request from '@/utils/request'
import type { IUserInfo, ILoginParams, ILoginResult } from '@/types/user'

/** 登录接口 */
export async function login(params: ILoginParams): Promise<ILoginResult> {
  try {
    return await request.post('/auth/login', params)
  } catch (error) {
    // 统一错误处理
    return Promise.reject(error)
  }
}

/** 获取用户信息 */
export async function getUserInfo(): Promise<IUserInfo> {
  return await request.get('/user/info')
}
```

## 检查要点
- ✅ 所有接口统一管理，不在组件中直接写请求地址
- ✅ 入参出参都有明确类型，禁止使用any
- ✅ 统一处理接口错误，返回可处理结果
- ✅ 按业务模块拆分，接口清晰分类
</content>

---