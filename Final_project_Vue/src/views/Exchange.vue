<template>
    <div>
        <h2>환율 계산기</h2>
        <Exchange />
    </div>
</template>

<script>
import { defineAsyncComponent } from 'vue'
export default {
  name: 'ExchangePage',
  setup() {
    // 동적으로 컴포넌트를 로드
    const Exchange = defineAsyncComponent(() => import('../views/Exchange.vue'))

    return {
      Exchange
    }
  }
}
</script>

<style lang="scss" scoped>

</style>