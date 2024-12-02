<template>
  <div>
    <!-- 은행 선택 드롭다운 -->
    <div class="bank-select">
      <label for="bank-select">은행 선택 : </label>
      <select id="bank-select" v-model="selectedBank" @change="goToPage(1)">
        <option value="">모든 은행</option>
        <option v-for="(bank, index) in banks" :key="index" :value="bank">{{ bank }}</option>
      </select>
    </div>

    <!-- 상품 목록 -->
    <div v-if="paginatedProducts.length">
      <h2>예금 상품</h2>
      <div class="product-list">
        <div class="product-card" v-for="(product, index) in paginatedProducts" :key="index">
          <div class="product-info">
            <h3>{{ product.fin_prdt_nm }}</h3>
            <p class="rate-info">
              기본 이자율: <span>{{ product.intr_rate }}%</span> | 최고 우대 이자율: <span>{{ product.intr_rate2 }}%</span> | 가입 기간: <span>{{ product.save_trm }}개월</span>
            </p>
            <router-link :to="`/savings-comparison/${product.id}`" class="button">상세보기</router-link>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button @click="goToPage(1)" :disabled="currentPage === 1">처음</button>
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">이전</button>

        <!-- 10개씩 끊어서 페이지 버튼 나누기 -->
        <span v-for="page in paginatedPageNumbers" :key="page">
          <button
            :class="{ active: page === currentPage }"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </span>

        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">다음</button>
        <button @click="goToPage(totalPages)" :disabled="currentPage === totalPages">끝</button>
      </div>
    </div>

    <div v-else>
      <p>상품이 없습니다. 은행을 선택해 보세요.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      products: [], // Django에서 반환된 데이터를 저장
      loading: false,
      banks: [], // 은행 목록을 저장
      selectedBank: "", // 선택된 은행
      currentPage: 1, // 현재 페이지 번호
      itemsPerPage: 9, // 한 페이지당 보여줄 항목 수
    };
  },
  computed: {
    totalPages() {
      // 필터링된 상품의 총 페이지 수 계산
      return Math.ceil(this.filterProductsByBank().length / this.itemsPerPage);
    },
    paginatedProducts() {
      // 현재 페이지에 해당하는 상품 목록 가져오기
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filterProductsByBank().slice(start, end);
    },
    paginatedPageNumbers() {
      // 현재 페이지를 기준으로 10개의 페이지 번호를 표시
      const pages = [];
      const totalPages = this.totalPages;
      let startPage = Math.floor((this.currentPage - 1) / 10) * 10 + 1; // 10개씩 나누어 시작 페이지 계산

      // 최대 10개 페이지 표시
      for (let i = 0; i < 10 && startPage <= totalPages; i++) {
        pages.push(startPage++);
      }
      return pages;
    },
  },
  methods: {
    async fetchProducts() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/products/api/savings-comparison/");
        this.products = response.data; // 데이터를 products 배열에 저장

        // kor_co_nm을 기준으로 은행 목록 추출 (중복 제거)
        this.banks = [...new Set(response.data.map((product) => product.kor_co_nm))];
      } catch (error) {
        console.error("Error fetching products:", error);
        alert("Failed to fetch products.");
      } finally {
        this.loading = false;
      }
    },
    filterProductsByBank() {
      // 선택된 은행에 맞는 상품만 필터링
      if (this.selectedBank) {
        return this.products.filter((product) => product.kor_co_nm === this.selectedBank);
      }
      return this.products;
    },
    goToPage(pageNumber) {
      // 페이지 이동
      if (pageNumber >= 1 && pageNumber <= this.totalPages) {
        this.currentPage = pageNumber;
      }
    },
  },
  mounted() {
    this.fetchProducts();
  },
};
</script>

<style scoped>
/* 은행 선택 드롭다운 */
.bank-select {
  margin-bottom: 20px;
  font-size: 1.1rem;
  color: #444;
}

select {
  padding: 8px 15px;
  border-radius: 5px;
  font-size: 1rem;
  margin-top: 10px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

/* 상품 목록 스타일 */
.product-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.product-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 250px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.product-info h3 {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 10px 0;
  color: #333;
}

.product-info p {
  font-size: 0.95rem;
  color: #555;
  margin: 10px 0;
}

.product-info .rate-info span {
  color: #4CAF50;
  font-weight: bold;
}

.product-info .button {
  display: inline-block;
  background-color: #4CAF50;
  color: white;
  padding: 10px;
  border-radius: 5px;
  text-decoration: none;
  margin-top: 15px;
  transition: background-color 0.3s ease;
}

.product-info .button:hover {
  background-color: #45a049;
}

/* 페이지네이션 스타일 */
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f4f4f9; /* 연한 배경 색상 */
  padding: 10px;
  border-radius: 10px; /* 둥근 모서리 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
  transition: background-color 0.3s ease; /* 배경 색상 전환 효과 */
}

/* 페이지네이션 버튼 스타일 */
.pagination button {
  padding: 8px 16px;
  margin: 0 5px;
  background-color: #007bff; /* 기본 파란색 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.pagination button.active {
  font-weight: bold;
  background-color: #0056b3; /* 선택된 버튼 색상 */
}

/* 비활성화된 버튼 스타일 */
.pagination button:disabled {
  background-color: #f4f4f9;
  cursor: not-allowed;
  color : #f4f4f9
}

/* 버튼 호버 효과 */
.pagination button:hover:not(:disabled) {
  background-color: #0056b3;
  transform: scale(1.1); /* 호버 시 버튼 크기 확대 */
}

/* 버튼에 마우스를 올렸을 때 배경색 변화
.pagination:hover {
  background-color: #e0e0e0; /* 페이지네이션 배경 색상 */
 

</style>
