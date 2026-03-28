<content>
---
name: 创建通用组件
description: 创建可复用的全局通用组件，遵循Vue3组件开发规范
trigger: /vue3-create-component
---

## 执行步骤
1. 在 `src/components/common/` 目录创建文件，帕斯卡命名法
2. 使用 `<script setup lang="ts">` 语法
3. 定义props，必须添加类型声明和默认值
4. 定义emit，必须添加类型校验
5. 支持`v-model`双向绑定（如需）
6. 组件不依赖业务逻辑，保证通用性

## 代码模板
```vue
<script setup lang="ts">
interface IProps {
  /** 标题描述 */
  title: string
  /** 是否禁用 */
  disabled?: boolean
  /** 绑定值 */
  modelValue?: string
}

interface IEmits {
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
}

const props = withDefaults(defineProps<IProps>(), {
  disabled: false
})

const emit = defineEmits<IEmits>()
</script>
```

## 检查要点
- ✅ 遵循单一职责，一个组件只做一件事
- ✅ props/emit都有完整类型定义
- ✅ 支持v-model规范（需要双向绑定时）
- ✅ 组件不耦合具体业务逻辑，可全局复用
- ✅ 公共组件添加了清晰的功能注释
</content>

---