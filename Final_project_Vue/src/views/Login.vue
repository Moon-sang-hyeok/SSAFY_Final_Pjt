<template>
  <div class="login-page">
    <div class="login-container">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="username">아이디</label>
          <input type="text" v-model="username" id="username" placeholder="아이디를 입력하세요" required />
        </div>

        <div class="input-group">
          <label for="password">비밀번호</label>
          <input type="password" v-model="password" id="password" placeholder="비밀번호를 입력하세요" required />
        </div>

        <button type="submit" class="login-button">로그인</button>
      </form>
      <p class="forgot-password"><router-link to="/forgot-password">비밀번호를 잊으셨나요?</router-link></p>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth'; // store import

export default {
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const router = useRouter();
    const authStore = useAuthStore(); // store를 사용하여 상태 관리

    const handleLogin = async () => {
      try {
        const response = await axios.post('http://localhost:8000/accounts/api/login/', {
          username: username.value,
          password: password.value,
        });
        console.log('응답 받은 토큰:', response.data.token);

        if (response.data.token) {
          // 로그인 성공 후, store에 토큰 저장
          authStore.setAuthToken(response.data.token);

          // 로그인 후 사용자 ID를 저장 (예: 응답에서 user_id를 받아와서 저장)
          const userId = response.data.user_id;  // 서버에서 user_id 받아오기
          if (userId) {
            authStore.setUser(userId);  // Pinia store에 user_id 저장
          } else {
            alert('사용자 ID를 받을 수 없습니다.');
            return;
          }

          alert('로그인 성공');
          router.push('/');  // 로그인 후 이동할 페이지
        } else {
          alert('토큰을 받을 수 없습니다.');
        }
      } catch (error) {
        alert('아이디 또는 비밀번호가 잘못되었습니다.');
      }
    };

    return { username, password, handleLogin };
  },
};
</script>

<style scoped>
.login-page {
  background: linear-gradient(to bottom, white, #dfdfdf);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  color: #333;
  font-weight: 600;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: #f9f9f9;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  border-color: #4f5bfe;
  outline: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #1f76f8;
  color: white;
  font-size: 1.1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #394F78;
}

.forgot-password {
  text-align: center;
  margin-top: 15px;
}

.forgot-password a {
  text-decoration: none;
  color: #4facfe;
  font-weight: 500;
}

.forgot-password a:hover {
  text-decoration: underline;
}
</style>
