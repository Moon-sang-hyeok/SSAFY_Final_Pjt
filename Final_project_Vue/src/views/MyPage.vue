<template>
  <div class="my-page">
    <h1>내 페이지</h1>

    <!-- 기본 정보 -->
    <div class="user-info">
      <h2>기본 정보</h2>
      <p>이름: {{ userInfo.full_name }}</p>
      <p>이메일: {{ userInfo.email }}</p>
      <button @click="editUserInfo">정보 수정</button>
    </div>

    <!-- 정보 수정 폼 -->
    <div v-if="editing">
      <h3>정보 수정</h3>
      <form @submit.prevent="saveUserInfo">
        <label>이름:
          <input type="text" v-model="newUserInfo.full_name" />
        </label>
        <br />
        <label>이메일:
          <input type="email" v-model="newUserInfo.email" />
        </label>
        <br />
        <button type="submit">저장</button>
      </form>
    </div>

    <!-- 금융 상품 리스트 -->
    <div class="financial-products">
      <!-- 예금 상품 테이블 -->
      <div v-if="financialProducts.some(product => product.type === 'Deposit Product')">
        <h2>가입한 예금 상품</h2>
        <table class="styled-table">
          <thead>
            <tr>
              <th>상품명</th>
              <th>금리 (%)</th>
              <th>우대 금리 (%)</th>
              <th>해지</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in financialProducts.filter(product => product.type === 'Deposit Product')" :key="product.id">
              <td>{{ product.fin_prdt_nm }}</td>
              <td>{{ product.intr_rate }}%</td>
              <td>{{ product.intr_rate2 }}%</td>
              <td>
                <button class="cancel-btn" @click="cancelProduct(product.id)">해지하기</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 적금 상품 테이블 -->
      <div v-if="financialProducts.some(product => product.type === 'Saving Product')">
        <h2>가입한 적금 상품</h2>
        <table class="styled-table">
          <thead>
            <tr>
              <th>상품명</th>
              <th>금리 (%)</th>
              <th>우대 금리 (%)</th>
              <th>해지</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in financialProducts.filter(product => product.type === 'Saving Product')" :key="product.id">
              <td>{{ product.fin_prdt_nm }}</td>
              <td>{{ product.intr_rate }}%</td>
              <td>{{ product.intr_rate2 }}%</td>
              <td>
                <button class="cancel-btn" @click="cancelProduct(product.id)">해지하기</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 금리 차트 -->
    <div>
      <h2>금리 차트</h2>
      <canvas id="interest-rate-chart"></canvas>
    </div>

    <!-- 포트폴리오로 이동 버튼 -->
    <div class="portfolio-button">
      <router-link to="/portfolio">
        <button>포트폴리오로 이동</button>
      </router-link>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import Chart from "chart.js/auto"; // 차트 라이브러리

export default {
  data() {
    return {
      userInfo: {},
      financialProducts: [],
      editing: false,
      newUserInfo: {
        full_name: "",
        email: "",
      },
      chart: null, // 차트를 저장
    };
  },
  mounted() {
    this.fetchUserInfo(); // 사용자 정보 조회
    this.fetchFinancialProducts(); // 금융 상품 목록 조회
  },
  methods: {
    async fetchUserInfo() {
      const authStore = useAuthStore();
      const token = authStore.token;
      if (!token) return;

      try {
        const response = await axios.get("http://localhost:8000/user-profile/profile/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.userInfo = response.data;

        // 새로운 사용자 정보에 초기 데이터 설정
        this.newUserInfo.full_name = this.userInfo.full_name;
        this.newUserInfo.email = this.userInfo.email;
      } catch (error) {
        console.error("사용자 정보 가져오기 실패", error);
      }
    },
    editUserInfo() {
      // 정보 수정 폼 활성화
      this.editing = true;
    },
    async saveUserInfo() {
  const authStore = useAuthStore();
  const token = authStore.token;
  if (!token) return;

  try {
    const response = await axios.patch(
      "http://localhost:8000/user-profile/profile/update/",
      this.newUserInfo,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    alert("정보가 성공적으로 수정되었습니다.");

    // 수정 완료 후 전체 페이지 새로고침
    window.location.reload();
  } catch (error) {
    console.error("사용자 정보 수정 실패", error);
    alert("정보 수정 중 오류가 발생했습니다.");
  }
},
    async fetchFinancialProducts() {
      const authStore = useAuthStore();
      const token = authStore.token;
      if (!token) return;

      try {
        const response = await axios.get("http://localhost:8000/accounts/financial-products/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.financialProducts = [
          ...response.data.savings.map(product => ({
            ...product,
            type: "Saving Product",
          })),
          ...response.data.deposits.map(product => ({
            ...product,
            type: "Deposit Product",
          })),
        ];
        this.prepareChartData();
      } catch (error) {
        console.error("금융 상품 목록 가져오기 실패", error);
      }
    },
    async cancelProduct(productId) {
      const authStore = useAuthStore();
      const token = authStore.token;
      if (!token) return;

      try {
        // 상품 해지 API 호출
        const response = await axios.delete(`http://localhost:8000/accounts/financial-products/${productId}/cancel/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        // 성공적으로 해지된 상품을 테이블에서 제거
        this.financialProducts = this.financialProducts.filter(product => product.id !== productId);

        // 차트 데이터 갱신
        this.prepareChartData();

        alert("상품 해지 완료");
      } catch (error) {
        console.error("상품 해지 실패", error);
      }
    },
    prepareChartData() {
      const labels = this.financialProducts.map(product => product.fin_prdt_nm);
      const intrRates = this.financialProducts.map(product => product.intr_rate);
      const intrRate2s = this.financialProducts.map(product => product.intr_rate2);

      if (this.chart) this.chart.destroy(); // 기존 차트가 있으면 삭제
      const ctx = document.getElementById("interest-rate-chart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "기본 금리",
              data: intrRates,
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
            {
              label: "우대 금리",
              data: intrRate2s,
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: { title: { display: true, text: "상품명" } },
            y: { beginAtZero: true, title: { display: true, text: "금리 (%)" } },
          },
          plugins: {
            legend: { position: "top" },
            tooltip: {
              callbacks: {
                label: tooltipItem => `${tooltipItem.dataset.label}: ${tooltipItem.raw}%`,
              },
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.my-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.my-page h1 {
  text-align: center;
  margin-bottom: 20px;
}

.my-page h2 {
  margin-top: 20px;
  text-align: center;
}

.my-page .user-info {
  margin-bottom: 20px;
}

.my-page form {
  display: flex;
  flex-direction: column;
}

.my-page form label {
  margin: 10px 0 5px;
}

.my-page input {
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.my-page button {
  padding: 10px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.my-page button:hover {
  background-color: #555;
}

/* 스타일링된 테이블 */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 16px;
  text-align: left;
}

.styled-table th,
.styled-table td {
  padding: 12px;
  border: 1px solid #ddd;
}

.styled-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.cancel-btn {
  background-color: #ff4444;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #d33d3d;
}

/* 차트 스타일 */
canvas {
  margin: 20px 0;
  display: block;
  width: 100%;
}

.portfolio-button {
  text-align: center;
  margin-top: 30px;
}

.portfolio-button button {
  padding: 10px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.portfolio-button button:hover {
  background-color: #004d99;
}
</style>
