<template>
  <div class="login-page">
    <h1>로그인</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="name">아이디 : </label>
        <input type="text" v-model="username" id="name" required />
      </div>

      <div>
        <label for="password">비밀번호 : </label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';  // store import

export default {
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const authStore = useAuthStore();  // store를 사용하여 상태 관리
    
    const login = async () => {
      // 로그인 API 호출 후 받은 토큰
      const response = await axios.post('/api/login', { username, password });
      const token = response.data.token;

      // Pinia store에 토큰 저장
      authStore.setToken(token);
    };
    console.log(authStore.token);  
    const handleLogin = async () => {
      try {
        // 로그인 API 호출
        const response = await axios.post('http://localhost:8000/accounts/api/token/', {
          username: username.value,
          password: password.value,
        });

        // 로그인 성공 후 토큰 저장 (access 및 refresh 토큰 모두 저장 가능)
        authStore.setAuthToken(response.data.access);
        authStore.setRefreshToken(response.data.refresh);  // refresh 토큰 저장

        console.log("로그인 성공, 저장된 토큰:", authStore.token);  // 디버깅용으로 토큰 확인
        alert('로그인 성공');
        router.push('/');  // 로그인 후 이동할 페이지
      } catch (error) {
        // 오류 처리
        if (error.response) {
          // 서버에서 응답을 받았지만 에러가 발생한 경우
          alert(error.response.data.detail || '아이디 또는 비밀번호가 잘못되었습니다.');
        } else {
          // 서버 연결 자체가 안 될 경우
          alert('서버와 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
        }
      }
    };

    return { username, password, handleLogin, login, };
  },
};
</script>

<style scoped>
.login-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.login-page h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-page form {
  display: flex;
  flex-direction: column;
}

.login-page label {
  margin: 10px 0 5px;
}

.login-page input {
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-page button {
  padding: 10px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-page button:hover {
  background-color: #555;
}
</style>
