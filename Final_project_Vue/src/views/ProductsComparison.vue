<template>
  <div>
    <h1>예적금 상품 비교 페이지</h1>
    
    <!-- 버튼 영역 -->
    <div>
      <button @click="showDepositsProduct">예금 상품 보기</button>
      <button @click="showSavingsProduct">적금 상품 보기</button>
    </div>
    
    <!-- 조건부 컴포넌트 렌더링 -->
    <SavingsProduct v-if="currentComponent === 'savings'" />
    <DepositsProduct v-else-if="currentComponent === 'deposits'" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import SavingsProduct from "@/components/SavingsProduct.vue";
import DepositsProduct from "@/components/DepositsProduct.vue";

// 현재 보여줄 컴포넌트를 상태로 관리
const currentComponent = ref("savings"); // 기본은 예금 상품

// 이벤트 핸들러
function showSavingsProduct() {
  currentComponent.value = "savings";
}

function showDepositsProduct() {
  currentComponent.value = "deposits";
}
</script>

<style scoped>
/* 버튼 스타일 */
button {
  margin: 0.5em;
  padding: 0.5em 1em;
  font-size: 1em;
  cursor: pointer;
}

/* 선택한 버튼 강조 효과 */
button:focus {
  outline: none;
  background-color: #ddd;
  font-weight: bold;
}
</style>
