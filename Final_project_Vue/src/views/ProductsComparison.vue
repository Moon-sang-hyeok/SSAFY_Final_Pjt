<template>
  <div class="product-container">
    <h1 class="page-title">예적금 상품 비교 페이지</h1>

    <!-- 버튼 영역 -->
    <div class="button-container">
      <button 
        class="tab-button" 
        :class="{'active': currentComponent === 'deposits'}" 
        @click="showDepositsProduct">
        예금 상품 보기
      </button>
      <button 
        class="tab-button" 
        :class="{'active': currentComponent === 'savings'}" 
        @click="showSavingsProduct">
        적금 상품 보기
      </button>
    </div>

    <!-- 조건부 컴포넌트 렌더링 -->
    <div v-if="currentComponent === 'savings'">
      <SavingsProduct :products="savingsProducts" />
    </div>
    <div v-else-if="currentComponent === 'deposits'">
      <DepositsProduct :products="depositsProducts" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import SavingsProduct from "@/components/SavingsProduct.vue";
import DepositsProduct from "@/components/DepositsProduct.vue";

// 현재 보여줄 컴포넌트를 상태로 관리
const currentComponent = ref("deposits"); // 기본은 예금 상품

// 예적금 상품 리스트 예시
const savingsProducts = ref([
  { id: 1, name: "적금 상품 1", rate: 3.5, bank: "A은행", duration: 1 },
  { id: 2, name: "적금 상품 2", rate: 2.8, bank: "B은행", duration: 2 },
  // 상품 목록 추가
]);

const depositsProducts = ref([
  { id: 1, name: "예금 상품 1", rate: 3.0, bank: "C은행", duration: 1 },
  { id: 2, name: "예금 상품 2", rate: 2.5, bank: "D은행", duration: 2 },
  // 상품 목록 추가
]);

// 이벤트 핸들러
function showSavingsProduct() {
  currentComponent.value = "savings";
}

function showDepositsProduct() {
  currentComponent.value = "deposits";
}
</script>

<style scoped>
/* 전체 페이지 레이아웃 */
.product-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f3f4f6;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

/* 페이지 제목 */
.page-title {
  text-align: center;
  font-size: 2.2em;
  margin-bottom: 30px;
  color: #333;
}

/* 버튼 컨테이너 */
.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

/* 버튼 기본 스타일 */
.tab-button {
  padding: 12px 25px;
  font-size: 1.1em;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  background-color: white;
  color: #195DE7;
  transition: background-color 0.3s, transform 0.2s;
  width: 200px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  
}

/* 버튼 hover 효과 */
.tab-button:hover {
  background-color: #195DE7;
  color: white;
  transform: translateY(-2px);
  opacity: 0.7;
}

/* 버튼 선택 시 강조 효과 */
.tab-button.active {
  background-color: #195DE7;
  color: white;
  font-weight: bold;
}

/* 상품 목록 그리드 설정 */
.product-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3개의 열로 설정 */
  gap: 20px;
  margin-bottom: 30px;
}

/* 상품 카드 */
.product-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  overflow: hidden;
  height: 100%;
}

/* 상품 카드 hover 효과 */
.product-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* 상품 제목 스타일 */
.product-card .product-title {
  font-size: 1.6em;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

/* 상품 금리 및 우대 금리 표시 */
.product-rates {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.product-rate {
  font-size: 1.2em;
  color: #555;
}

.product-rate span {
  font-weight: bold;
  color: #007bff;
}

/* 상세보기 버튼 스타일 */
.view-details-button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s, transform 0.2s;
}

/* 버튼 hover 효과 */
.view-details-button:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

/* 페이지 네비게이션 스타일 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

.pagination button {
  padding: 10px 15px;
  font-size: 1.1em;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.pagination button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.pagination .active {
  background-color: #28a745;
  font-weight: bold;
}
</style>
