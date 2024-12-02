<template>
  <div id="app">
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/products-comparison">예적금 상품 비교</router-link></li>
        <li><router-link to="/nearby-banks">주변 은행 검색</router-link></li>
        <li><router-link to="/recommend">금융 상품 추천</router-link></li>
        <li><router-link to="/exchange">환율 계산기</router-link></li>
        <li><router-link to="/community">커뮤니티</router-link></li>
      </ul>

      <div class="auth-buttons">
        <!-- 로그인 버튼 -->
        <button 
          v-if="!isLoggedIn" 
          @click="navigateTo('/login')" 
          class="auth-button">
          Login
        </button>

        <!-- 회원가입 버튼 -->
        <button 
          v-if="!isLoggedIn" 
          @click="navigateTo('/signup')" 
          class="auth-button">
          Sign Up
        </button>

        <!-- 로그아웃과 마이 페이지 버튼 -->
        <button 
          v-if="isLoggedIn" 
          @click="logout" 
          class="auth-button">
          Logout
        </button>

        <button 
          v-if="isLoggedIn" 
          @click="navigateTo('/mypage')" 
          class="auth-button">
          My Page
        </button>
      </div>
    </nav>

    <router-view></router-view>
  </div>

  <footer class="footer">
  <div class="footer-info">
    <p>개인정보처리방침 | 신용정보활용체제 | 전자민원 | 사고신고 | 싸피지킴이 | 보호금융상품등록부</p>
    <p>상품공시실 | 영업점안내 | 상담신청 | 웹접근성이용안내 | 위치기반서비스약관</p>
    <p>고객센터 1588-1234 평일 09:00~18:00 (은행휴무일 제외) © SSOKBO BANK. All rights reserved.</p>
  </div>
  <div class="footer-links">
    <p>싸피 홈페이지 | 싸피 페이스북 | 싸피 인스타그램 | 싸피 유튜브</p>
  </div>
  <div class="footer-certifications">
    <p>프로젝트 진행 기간 2024.11.18 ~ 2024.11.26</p>
    <p>이전 수상내역 보기 | 다음 수상내역 보기 | 글로벌패밀리</p>
  </div>
</footer>
</template>

<script>
import { useAuthStore } from './stores/auth';
import { computed, onMounted, watchEffect } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const isLoggedIn = computed(() => authStore.isAuthenticated);

    onMounted(() => {
      authStore.initialize();
    });

    watchEffect(() => {
      if (authStore.isAuthenticated) {
        console.log("로그인 상태: ", authStore.isAuthenticated);
      } else {
        console.log("로그아웃 상태");
      }
    });

    const logout = () => {
      authStore.logout();
      router.push('/');
    };

    const navigateTo = (path) => {
      router.push(path);
    };

    return {
      isLoggedIn,
      logout,
      navigateTo, // 버튼으로 페이지 이동 처리
    };
  },
};
</script>

<style>
/* 네비게이션 바 스타일 */
nav {
  background-color: #195DE7;
  color: white;
  padding: 5px; /* 네비게이션 바의 두께를 얇게 */
  position: fixed;
  top: 10px;
  left: 10px;
  width: calc(100% - 20px);
  z-index: 1000;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
  background-color: white; /* 배경색을 흰색으로 변경 */
  color: #195DE7; /* 글자 색을 네비게이션 바와 같은 색으로 */
  padding: 20px 8px; /* hover 시 네비게이션 바 두께와 동일하게 설정 */
  font-size: 18px;
  font-weight: 700;
  border-radius: 5px; /* 모서리 둥글게 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 약간의 그림자 효과 추가 */
  position: relative; /* 네비게이션 바 위로 올라오도록 설정 */
  z-index: 1100;
  /* text-decoration: underline; 밑줄 추가 */
}

#app {
  padding-top: 25px; /* 네비게이션 바 높이에 맞게 여백 조정 */
}

.auth-buttons {
  position: absolute;
  top: 15px; /* 위치 조정 */
  right: 20px;
}

.auth-button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #195DE7;
  color: white;
  text-decoration: none;
  border: 2px solid #195DE7;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.auth-button:hover {
  background-color: white;
  color: #195DE7;
  border-color: white;
}

/* 푸터 스타일 */
.footer {
  display: flex;
  flex-direction: column; /* 세로로 나열 */
  justify-content: space-between; /* 각 항목 간 공간을 최대화 */
  align-items: flex-start; /* 왼쪽 정렬 */
  padding: 20px;
  width: 100%;
  background-color: #f1f1f1; /* 배경색 */
}

.footer-info,
.footer-links,
.footer-certifications {
  width: 100%; /* 각 항목을 전체 너비에 맞춤 */
  margin-bottom: 10px; /* 항목 간 간격 */
}

.footer-info p,
.footer-links p,
.footer-certifications p {
  font-size: 14px;
  color: #333;
  margin: 5px 0;
  word-break: break-word; /* 긴 문장이 잘리거나 겹치지 않도록 처리 */
}

.footer-links p {
  text-align: center; /* 가운데 정렬 */
}

.footer-certifications p {
  text-align: right; /* 오른쪽 정렬 */
}

</style>