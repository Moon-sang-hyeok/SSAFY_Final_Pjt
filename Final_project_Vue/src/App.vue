<template>
  <div id="app">
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/savings-comparison">예적금 상품 비교</router-link></li>
        <li><router-link to="/nearby-banks">주변 은행 검색</router-link></li>
        <li><router-link to="/recommend">금융 상품 추천</router-link></li>
        <li><router-link to="/exchange">환율 계산기</router-link></li>
      </ul>
    </nav>
    <!-- 로그인 및 회원가입/로그아웃 버튼 -->
    <div class="auth-buttons">
      <router-link v-if="!isLoggedIn" to="/login" class="auth-button">Login</router-link>
      <router-link v-if="!isLoggedIn" to="/signup" class="auth-button">Sign Up</router-link>
      <button v-if="isLoggedIn" @click="logout" class="auth-button">Logout</button>
    </div>
    <router-view></router-view>  <!-- 라우터 뷰로 각 페이지가 표시됩니다 -->
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
export default {
  name: 'App',
  computed: {
    // 로그인 상태를 Pinia store에서 가져옴
    isLoggedIn() {
      const authStore = useAuthStore();
      return authStore.isLoggedIn;
    },
  },
  methods: {
    logout() {
      const authStore = useAuthStore();
      authStore.logout(); // 로그아웃 처리
      this.$router.push('/'); // 로그아웃 후 홈으로 리디렉션
    },
  },
}
</script>

<style>
/* 네비게이션 바 스타일 */
nav {
  background-color: #333;
  color: white;
  padding: 10px;
}

nav ul {
  list-style: none;
  padding: 0;
  display: flex;
}

nav li {
  margin-right: 20px;
}

nav a {
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

/* 로그인 및 회원가입 버튼 스타일 */
.auth-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
}

.auth-button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #333;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}

.auth-button:hover {
  background-color: #555;
}
</style>
