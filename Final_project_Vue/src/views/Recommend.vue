<template>
  <div class="container">
    <h1>금융 상품 추천</h1>

    <!-- 필터 설정 (가입 목적, 저축 기간 등) -->
    <div class="filter">
      <label for="goal">가입 목적:</label>
      <select v-model="selectedGoal">
        <option value="">선택하세요</option>
        <option value="결혼 자금">결혼 자금</option>
        <option value="자녀 학비">자녀 학비</option>
        <option value="노후 자금">노후 자금</option>
        <option value="자택 마련">자택 마련</option>
      </select>
    </div>

    <div class="filter">
      <label for="duration">저축 기간:</label>
      <select v-model="selectedDuration">
        <option value="">선택하세요</option>
        <option value="0.5">6개월</option>
        <option value="1">1년</option>
        <option value="3">3년</option>
        <option value="5">5년</option>
        <option value="10">10년</option>
      </select>
    </div>

    <div class="filter">
      <label for="bank">은행:</label>
      <select v-model="selectedBank">
        <option value="">선택하세요</option>
        <option value="KB">KB국민은행</option>
        <option value="Shinhan">신한은행</option>
        <option value="Hana">하나은행</option>
        <option value="WOORI">우리은행</option>
        <option value="Citibank">씨티은행</option>
        <option value="KakaoBank">카카오뱅크</option>
        <option value="TossBank">토스뱅크</option>
        <option value="IBK">기업은행</option>
        <option value="Nonghyup">농협은행</option>
        <option value="StandardChartered">스탠다드차타드은행</option>
        <option value="KDB">산업은행</option>
        <option value="BUSANBank">부산은행</option>
        <option value="DaeguBank">대구은행</option>
        <option value="GwangjuBank">광주은행</option>
        <option value="JejuBank">제주은행</option>
      </select>
    </div>

    <div class="filter">
      <label for="minInterestRate">최소 이자율:</label>
      <input type="number" v-model="minInterestRate" />
    </div>

    <div class="filter">
      <label for="maxInterestRate">최대 이자율:</label>
      <input type="number" v-model="maxInterestRate" />
    </div>

    <!-- 검색 버튼 -->
    <div>
      <button @click="searchProducts">검색</button>
    </div>

    <div v-if="aiResponse" class="ai-response">
      <h3>AI 추천:</h3>
      <p v-html="aiResponse"></p>
      <button @click="addToPortfolio" :disabled="!isLoggedIn">포트폴리오에 저장</button>
    </div>

    <div v-if="portfolio.length > 0" class="portfolio">
      <h3>내 포트폴리오</h3>
      <ul>
        <li v-for="item in portfolio" :key="item.id">
          {{ item.product_name }} / {{ item.bank }} / {{ item.interest_rate }}%
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useAuthStore } from "@/stores/auth"


export default {
  data() {
    return {
      selectedGoal: "",
      selectedDuration: "",
      selectedBank: "",
      minInterestRate: 0,
      maxInterestRate: 5,
      recommendedProducts: { savings: [], deposits: [] },
      aiResponse: "안녕하세요! 원하는 금융 상품을 추천받기 위해 선택사항을 고르세요.",
      portfolio: [], // 포트폴리오 저장
    };
  },
  computed: {
    auth() {
      return useAuthStore();
    },
    // 로그인 여부 확인
    isLoggedIn() {
      return this.auth.isAuthenticated;
    },

    // 현재 사용자 ID
    currentUser() {
      return this.auth.currentUser;
    },
  },
  methods: {
    async searchProducts() {
      // 모든 선택 항목이 입력되었는지 확인
      if (this.selectedGoal && this.selectedDuration && this.selectedBank) {
        try {
          const params = {
            duration: this.selectedDuration,
            bank: this.selectedBank,
            minInterestRate: this.minInterestRate,
            maxInterestRate: this.maxInterestRate,
          };

          const prompt = `금융상품 데이터 총합에서 가입목적은 '${this.selectedGoal}', 저축기간은 '${this.selectedDuration}'년, 은행은 '${this.selectedBank}', 최소 이자율은 ${this.minInterestRate}%, 최대 이자율이 ${this.maxInterestRate}% 설정한 금융 상품을 추천해 주세요. 추천 설명을 조금 자세히 해주세요. 그리고 그 추천하는 은행의 공식 홈페이지도 주세요, 마지막에는 '추천하는 상품명 : "상품명"'으로 말해주세요 띄어쓰기도 안틀리게`;

          const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
          if (!apiKey) {
            throw new Error("API 키가 정의되지 않았습니다.");
          }

          const openAiResponse = await axios.post(
            "https://api.openai.com/v1/chat/completions",
            {
              model: "gpt-3.5-turbo",
              messages: [
                {
                  role: "user",
                  content: prompt,
                },
              ],
              max_tokens: 300,
              temperature: 0.7,
            },
            {
              headers: {
                Authorization: `Bearer ${apiKey}`,
                "Content-Type": "application/json",
              },
            }
          );

          // AI 응답에 링크 추가
          this.aiResponse = openAiResponse.data.choices[0].message.content.trim();

          // 링크에 <a> 태그를 포함하여 직접 클릭할 수 있도록 처리
          const bankHomepageRegex = /(https?:\/\/[^\s]+)/g;
          this.aiResponse = this.aiResponse.replace(bankHomepageRegex, `<a href="$&" target="_blank">$&</a>`);

          // 금융 상품 추천 API 호출
          const response = await axios.get("http://127.0.0.1:8000/products/api/products/", {
            params: params,
          });

          const { savings, deposits } = response.data;
          this.recommendedProducts.savings = savings || [];
          this.recommendedProducts.deposits = deposits || [];
        } catch (error) {
          console.error("상품을 가져오는 데 실패했습니다.", error);
        }
      } else {
        this.aiResponse = "모든 선택 항목을 입력한 후 검색을 눌러주세요.";
      }
    },

    async addToPortfolio() {
      if (!this.isLoggedIn) {
        // 로그인되지 않은 경우 경고창 표시
        alert("로그인 후 이용해 주세요.");
        return;
      }
      const userId = localStorage.getItem('user_id')
      const recommendedProduct = {
        user: parseInt(userId, 10),
        product_name: this.extractProductName(this.aiResponse),
        bank: this.selectedBank,
        interest_rate: `${this.minInterestRate}-${this.maxInterestRate}`,
        
      };

      // 포트폴리오에 추가
      try {
        const authStore = useAuthStore();  // Pinia store 접근
        const token = authStore.token;
        console.log("전송 데이터:", recommendedProduct);
        console.log("전송 데이터:", JSON.stringify(recommendedProduct, null, 2));
        await axios.post(
          `http://127.0.0.1:8000/portfolio/portfolio/`,
          
          recommendedProduct,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        // 로컬에서 포트폴리오 업데이트
        this.portfolio.push(recommendedProduct);
      } catch (error) {
        console.error("포트폴리오 저장에 실패했습니다.", error);
      }
    },

    async loadPortfolio() {
      if (this.isLoggedIn && this.currentUser) {
        try {
          const authStore = useAuthStore();
          const token = authStore.token;
          
          const response = await axios.get(
            `http://127.0.0.1:8000/portfolio/portfolio/list/`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          this.portfolio = response.data.portfolio || [];
        } catch (error) {
          console.error("포트폴리오 로딩에 실패했습니다.", error);
        }
      }
    },
    
    extractProductName(response) {
      const regex = /추천하는 상품명 : "([^"]+)|추천하는 상품명: "([^"]+)"|추천하는 상품명: ([^ ]+)|추천하는 상품명 : ([^ ]+)|추천하는 상품명 : '([^']+)|추천하는 상품명: '([^']+)/;
      const match = response.match(regex);
      if (match) {
        return match[1] || match[2] || match[3] || match[4] || match[5] || match[6];
      } else {
        return "알 수 없는 상품";
      }
    },

  mounted() {
    this.loadPortfolio(); // 포트폴리오가 있다면 로드
  },
}
}
</script>

<style scoped>
/* 기존 스타일 코드 그대로 사용 */
.container {
  width: 80%;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 2rem;
  color: #4a90e2;
  margin-bottom: 20px;
}

h3 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 10px;
}

.filter {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

label {
  font-size: 1rem;
  color: #555;
  margin-bottom: 5px;
}

select, input {
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease;
}

select:focus, input:focus {
  border-color: #4a90e2;
  outline: none;
}

.ai-response {
  margin-top: 20px;
  padding: 15px;
  background-color: #e9f7fe;
  border-left: 5px solid #4a90e2;
  border-radius: 5px;
  font-size: 1rem;
  color: #333;
  line-height: 1.6;
}

.ai-response h3 {
  font-weight: bold;
}

button {
  padding: 12px 20px;
  font-size: 1rem;
  color: white;
  background-color: #4a90e2;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #357ab7;
}

.portfolio {
  margin-top: 30px;
  padding: 10px;
  background-color: #f1f1f1;
  border-radius: 5px;
}

.portfolio h3 {
  font-size: 1.5rem;
  color: #333;
}

.portfolio ul {
  list-style-type: none;
  padding: 0;
}

.portfolio li {
  font-size: 1rem;
  color: #333;
  margin-bottom: 5px;
}

.login-message {
  color: red;
  font-size: 1rem;
  margin-top: 10px;
}
</style>
