<template>
  <div class="product-detail">
    <h1>상품 상세 정보</h1>
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && !error && product" class="product-card">
      <h2 class="product-title">{{ product.fin_prdt_nm }}</h2>
      <ul class="product-info">
        <li><strong>기본 이자율:</strong> {{ product.intr_rate }}%</li>
        <li><strong>최고 우대 이자율:</strong> {{ product.intr_rate2 }}%</li>
        <li><strong>가입 방법:</strong> {{ product.join_way }}</li>
        <li><strong>우대 조건:</strong> {{ product.spcl_cnd }}</li>
        <li><strong>가입 대상:</strong> {{ product.join_member }}</li>
        <li><strong>저축 금리 유형명:</strong> {{ product.intr_rate_type_nm }}</li>
        <li>
          <strong>저축 한도:</strong>
          <span v-if="product.max_limit === null">없음</span>
          <span v-else>{{ formatNumber(product.max_limit) }}원</span>
        </li>
        <li><strong>저축 기간:</strong> {{ product.save_trm }} 개월</li>
      </ul>
      <p v-if="joinMessage" class="message">{{ joinMessage }}</p>
      <p v-else class="message"><div style="height: 21px;"><br> </div> </p>
      <div class="actions">
        <button @click="joinProduct" class="join-button">가입하기</button>
        <router-link :to="`/products-comparison`" class="back-button">뒤로가기</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useAuthStore } from '../stores/auth';

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  methods: {
    formatNumber(value) {
      if (value !== null) {
        return value.toLocaleString(); // 천 단위 쉼표 추가
      }
      return value;
    },
  },
  setup(props) {
    const product = ref(null);
    const loading = ref(false);
    const error = ref(null);
    const joinMessage = ref("");

    const fetchProductDetails = async () => {
      loading.value = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/products/api/savings-comparison/${props.id}/`
        );
        product.value = response.data;
      } catch (err) {
        error.value = "상품 정보를 가져올 수 없습니다.";
      } finally {
        loading.value = false;
      }
    };

    const joinProduct = async () => {
      try {
        const authStore = useAuthStore();
        const token = authStore.token;

        const response = await axios.post(
          `http://127.0.0.1:8000/products/api/savings/join/${props.id}/`,
          {},
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          }
        );
        joinMessage.value = response.data.message;
      } catch (err) {
        joinMessage.value =
          err.response?.data?.message || "상품 가입에 실패했습니다.";
      }
    };

    onMounted(() => {
      fetchProductDetails();
    });

    return {
      product,
      loading,
      error,
      joinMessage,
      joinProduct,
    };
  },
};
</script>

<style scoped>
.product-detail {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #34495e;
  text-align: center;
  margin-bottom: 20px;
}

.loading,
.error {
  text-align: center;
  color: #e74c3c;
  font-weight: bold;
}

.product-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.product-title {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.5rem;
  text-align: center;
}

.product-info {
  list-style: none;
  padding: 0;
}

.product-info li {
  margin: 10px 0;
  font-size: 1rem;
  color: #34495e;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.join-button,
.back-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  font-size: 1rem;
  cursor: pointer;
}

.join-button {
  background-color: #4CAF50;
  color: white;
  transition: background-color 0.3s ease;
}

.join-button:hover {
  background-color: #45a049;
  transform: scale(1.1);
}

.back-button {
  background-color: #C80F00;
  color: white;
  text-align: center;
}

.back-button:hover {
  background-color: #C80F00;
  transform: scale(1.1);
}

.message {
  margin-top: 20px;
  color: #16a085;
  text-align: center;
  font-weight: bold;
}
</style>
