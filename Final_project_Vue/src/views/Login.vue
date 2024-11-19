<!-- src/views/Login.vue -->
<template>
    <div class="login-page">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="email">이메일</label>
          <input type="email" v-model="email" id="email" required />
        </div>
  
        <div>
          <label for="password">비밀번호</label>
          <input type="password" v-model="password" id="password" required />
        </div>
  
        <button type="submit">로그인</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '../stores/auth';
  
  export default {
    name: 'Login',
    setup() {
      const email = ref('');
      const password = ref('');
      const router = useRouter();
      const authStore = useAuthStore();
  
      const handleLogin = async () => {
        // API 호출로 로그인 처리 (예시)
        try {
          // 실제 로그인 API 호출을 여기에 추가합니다.
          const user = { email: email.value, password: password.value };
          authStore.login(user);  // 로그인 후 상태 관리
  
          alert('로그인 성공');
          router.push('/');  // 로그인 후 홈 페이지로 이동
        } catch (error) {
          alert('로그인 실패');
        }
      };
  
      return { email, password, handleLogin };
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
  