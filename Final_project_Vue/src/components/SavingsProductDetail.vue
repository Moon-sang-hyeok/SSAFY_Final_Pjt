<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const product = ref(null);
    const loading = ref(false);
    const error = ref(null);

    console.log("Product ID:", props.id);

    const fetchProductDetails = async () => {
      loading.value = true;
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/products/api/savings-comparison/${props.id}/`
        );
        console.log("Product Details:", response.data);
        product.value = response.data;
      } catch (err) {
        console.error("Error fetching product details:", err);
        error.value = "상품 정보를 가져올 수 없습니다.";
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      console.log("Fetching product details for ID:", props.id);
      fetchProductDetails();
    });

    return {
      product,
      loading,
      error,
    };
  },
};
</script>

<template>
  <div>
    <h1>상품 상세 페이지</h1>
    <div v-if="loading">로딩 중...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="!loading && !error && product">
      <h2>{{ product.fin_prdt_nm }}</h2>
      <p>기본 이자율: {{ product.intr_rate }}%</p>
      <p>최고 우대 이자율: {{ product.intr_rate2 }}%</p>
      <p>가입 방법: {{ product.join_way }}</p>
      <p>우대 조건: {{ product.spcl_cnd }}</p>
      <p>가입 대상: {{ product.join_member }}</p>
      <p>저축 금리 유형명: {{ product.intr_rate_type_nm }}</p>
      <p>적립 유형명: {{ product.rsrv_type_nm }}</p>
      <p>저축 기간: {{ product.save_trm }}</p>
      <router-link :to="`/products-comparison`">뒤로가기</router-link>
    </div>
  </div>
</template>

<style scoped>
h1 {
  color: #2c3e50;
}
</style>
