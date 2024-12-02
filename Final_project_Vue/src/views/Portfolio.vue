<template>
  <div class="portfolio-container">
    <h1>내 포트폴리오</h1>

    <div v-if="portfolio.length > 0">
      <ul>
        <li v-for="item in portfolio" :key="item.id">
          {{ item.product_name }} ({{ item.bank }} / {{ item.interest_rate }}%) 
          <button @click="removeFromPortfolio(item.id)">삭제</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>저장된 포트폴리오가 없습니다.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      portfolio: [],
    };
  },
  methods: {
    async loadPortfolio() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/portfolio/portfolio/list/", {
          headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
        });
        console.log("Portfolio data:", response.data); // 여기서 반환된 데이터 확인
        this.portfolio = response.data;
      } catch (error) {
        console.error("포트폴리오 불러오기 실패:", error);
      }
    },

    async removeFromPortfolio(id) {
      try {
        // id가 제대로 전달되는지 확인
        console.log("Deleting portfolio with id:", id);
        if (!id) {
          console.error("Invalid id:", id);
          return;
        }

        // 포트폴리오 항목의 id로 삭제 요청
        await axios.delete(`http://127.0.0.1:8000/portfolio/portfolio/list/${id}/`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("auth_token")}` },
        });
        
        // 로컬 데이터에서 삭제된 항목 제거
        this.portfolio = this.portfolio.filter((item) => item.id !== id);
      } catch (error) {
        console.error("포트폴리오 삭제 실패:", error);
      }
    },
  },
  mounted() {
    this.loadPortfolio();
  },
};
</script>


<style scoped>
.portfolio-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}
button {
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #ff5252;
}
</style>
