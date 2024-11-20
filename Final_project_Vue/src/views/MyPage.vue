<template>
    <div>
      <h1>내 페이지</h1>
  
      <div>
        <h2>기본 정보</h2>
        <p>이름: {{ userInfo.first_name }} {{ userInfo.last_name }}</p>
        <p>이메일: {{ userInfo.email }}</p>
        <button @click="editUserInfo">정보 수정</button>
      </div>
  
      <div v-if="editing">
        <h3>정보 수정</h3>
        <form @submit.prevent="saveUserInfo">
          <label>이름:
            <input type="text" v-model="newUserInfo.first_name" />
            <input type="text" v-model="newUserInfo.last_name" />
          </label>
          <br />
          <label>이메일:
            <input type="email" v-model="newUserInfo.email" />
          </label>
          <br />
          <button type="submit">저장</button>
        </form>
      </div>
  
      <div>
        <h2>가입한 금융 상품</h2>
        <ul>
          <li v-for="product in financialProducts" :key="product.id">
            {{ product.name }} - 금리: {{ product.interest_rate }}% - 가입일: {{ product.joined_date }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from "@/stores/auth";  // Pinia store import
  
  export default {
    data() {
      return {
        userInfo: {},  // 사용자 정보 저장
        financialProducts: [],  // 금융 상품 목록 저장
        chartData: [],  // 차트 데이터 (필요 시 추가)
        editing: false,  // 정보 수정 여부
        newUserInfo: {  // 수정할 사용자 정보
          first_name: '',
          last_name: '',
          email: '',
        },
      };
    },
    mounted() {
      this.fetchUserInfo();  // 사용자 정보 조회
      this.fetchFinancialProducts();  // 금융 상품 목록 조회
    },
    methods: {
  // 사용자 정보 조회
  async fetchUserInfo() {
    const authStore = useAuthStore();  // Pinia store에서 token을 가져옵니다
    const token = authStore.token;  // token을 가져옴
    if (!token) {
      console.error("토큰이 없습니다. 로그인 상태를 확인해주세요.");
      return;
    }

    console.log("Authorization 토큰:", token);  // 콘솔에 토큰 확인

    try {
      const response = await fetch("http://localhost:8000/user-profile/profile/", {
        method: "GET",
        headers: {
          "Authorization": `Token ${token}`,  // Pinia store에서 가져온 token을 헤더에 포함
        },
      });
      if (response.ok) {
        this.userInfo = await response.json();  // 사용자 정보 저장
      } else {
        console.error("사용자 정보 가져오기 실패");
      }
    } catch (error) {
      console.error("사용자 정보 오류:", error);
    }
  },

  // 금융 상품 목록 조회
  async fetchFinancialProducts() {
    const authStore = useAuthStore();  // Pinia store에서 token을 가져옵니다
    const token = authStore.token;  // token을 가져옴
    if (!token) {
      console.error("토큰이 없습니다. 로그인 상태를 확인해주세요.");
      return;
    }

    console.log("Authorization 토큰:", token);  // 콘솔에 토큰 확인

    try {
      const response = await fetch("http://localhost:8000/user-profile/financial-products/", {
        method: "GET",
        headers: {
          "Authorization": `Token ${token}`,  // Pinia store에서 가져온 token을 헤더에 포함
        },
      });
      if (response.ok) {
        this.financialProducts = await response.json();  // 금융 상품 목록 저장
      } else {
        console.error("금융 상품 목록 가져오기 실패");
      }
    } catch (error) {
      console.error("금융 상품 오류:", error);
    }
  },


      // 정보 수정 모드로 전환
      editUserInfo() {
        this.editing = true;
        this.newUserInfo = { ...this.userInfo };  // 기존 정보로 수정 폼 채우기
      },
  
      // 사용자 정보 저장
      async saveUserInfo() {
        const authStore = useAuthStore();  // Pinia store를 사용하여 token을 가져옵니다
        const token = authStore.token;  // token을 가져옴
        if (!token) {
          console.error("토큰이 없습니다. 로그인 상태를 확인해주세요.");
          return;
        }
  
        try {
          const response = await fetch("http://localhost:8000/user-profile/profile/update/", {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Token ${token}`,  // Pinia store에서 가져온 토큰을 헤더에 포함
            },
            body: JSON.stringify(this.newUserInfo),  // 수정된 사용자 정보
          });
          if (response.ok) {
            this.userInfo = { ...this.newUserInfo };  // 새 정보로 업데이트
            this.editing = false;  // 수정 모드 종료
          } else {
            console.error("사용자 정보 수정 실패");
          }
        } catch (error) {
          console.error("정보 수정 오류:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 스타일 코드 */
  </style>
  