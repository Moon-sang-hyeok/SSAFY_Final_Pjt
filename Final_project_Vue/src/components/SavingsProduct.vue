<script>
import axios from "axios";

export default {
  data() {
    return {
      products: [], // Django에서 반환된 데이터를 저장
      loading: false,
      banks: [], // 은행 목록을 저장
      selectedBank: "", // 선택된 은행
      currentPage: 1, // 현재 페이지 번호
      itemsPerPage: 10, // 한 페이지당 보여줄 항목 수
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
  },
  methods: {
    async fetchProducts() {
      this.loading = true;
      try {
        const response = await axios.get("http://127.0.0.1:8000/products/api/savings-comparison/");
        console.log("API Response:", response.data);
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

<template>
  <div>
    <!-- 은행 선택 드롭다운 -->
    <div>
      <label for="bank-select">은행 선택:</label>
      <select id="bank-select" v-model="selectedBank" @change="goToPage(1)">
        <option value="">모든 은행</option>
        <option v-for="(bank, index) in banks" :key="index" :value="bank">{{ bank }}</option>
      </select>
    </div>

    <!-- 상품 목록 -->
    <!-- <button @click="fetchProducts" :disabled="loading">
      {{ loading ? "가져오는중..." : "적금 상품 가져오기" }}
    </button> -->
    <div v-if="paginatedProducts.length">
      <h2>적금 상품</h2>
      <ul>
        <li v-for="(product, index) in paginatedProducts" :key="index">
          <div>
            <h3>{{ product.fin_prdt_nm }}
                <router-link :to="`/savings-comparison/${product.id}`" class='button'>상세보기</router-link>
            </h3>
            <p>기본 이자율: {{ product.intr_rate }}% | 최고 우대 이자율: {{ product.intr_rate2 }}% | 가입 기간: {{ product.save_trm }}개월 |</p>
            <hr>    
            
          </div>
        </li>
      </ul>

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">이전</button>
        <span v-for="page in totalPages" :key="page">
          <button
            :class="{ active: page === currentPage }"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </span>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">다음</button>
      </div>
    </div>
    <div v-else>
      <p>상품이 없습니다. 은행을 선택해 보세요.</p>
    </div>
  </div>
</template>

<style scoped>
select {
  margin-bottom: 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 15px;
}
.pagination {
  margin-top: 20px;
}
button.active {
  font-weight: bold;
  color: white;
  background-color: black;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px 0;
}

.pagination-button {
  font-size: 20px; /* 버튼의 글자 크기 */
  padding: 15px 25px; /* 버튼의 크기 조정 */
  margin: 0 10px; /* 버튼 간격 */
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.pagination-info {
  font-size: 18px; /* 현재 페이지 정보의 크기 */
  margin: 0 10px;
}
</style>