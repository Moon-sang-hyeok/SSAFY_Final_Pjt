<template>
  <div id="app">
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/savings-comparison">예적금 상품 비교</router-link></li>
        <li><router-link to="/nearby-banks">주변 은행 검색</router-link></li>
        <li><router-link to="/recommend">금융 상품 추천</router-link></li>
        <li><router-link to="/exchange">환율 계산기</router-link></li>
        <li><router-link to="/community">커뮤니티</router-link></li>
      </ul>
    </nav>

    <!-- 로그인 및 회원가입/로그아웃 버튼 -->
    <div class="auth-buttons">
      <!-- 로그인과 회원가입 버튼 -->
      <router-link v-if="!isLoggedIn" to="/login" class="auth-button">Login</router-link>
      <router-link v-if="!isLoggedIn" to="/signup" class="auth-button">Sign Up</router-link>

      <!-- 로그아웃과 마이 페이지 버튼 -->
      <button v-if="isLoggedIn" @click="logout" class="auth-button">Logout</button>
      <router-link v-if="isLoggedIn" to="/mypage" class="auth-button">My Page</router-link>
    </div>

    <router-view></router-view>  <!-- 라우터 뷰로 각 페이지가 표시됩니다 -->
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import { computed, onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();  // Pinia store를 가져옵니다
    const router = useRouter();  // useRouter를 통해 router 인스턴스를 가져옵니다
    const isLoggedIn = computed(() => authStore.isAuthenticated); // 로그인 상태를 계산

    // 페이지가 로드되었을 때, token 값을 로드하여 상태를 초기화
    onMounted(() => {
      authStore.initialize();  // Pinia store에서 상태를 초기화
    });

    // watchEffect로 로그인 상태 변화 감지
    watchEffect(() => {
      if (authStore.isAuthenticated) {
        console.log("로그인 상태: ", authStore.isAuthenticated);
      } else {
        console.log("로그아웃 상태");
      }
    });

    const logout = () => {
      authStore.logout();  // Pinia store에서 로그아웃 처리
      router.push('/');  // 로그아웃 후 홈으로 리디렉션
    };

    return {
      isLoggedIn,  // 로그인 상태를 UI에서 사용
      logout,
    }
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
