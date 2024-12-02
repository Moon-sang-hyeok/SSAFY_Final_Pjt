<template>
  <div class="signup-page">
    <h1>회원가입</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="fullname">사용자 이름</label>
        <input type="text" v-model="fullname" id="fullname" required />
      </div>

      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" v-model="username" id="username" required />
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input type="email" v-model="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" v-model="password2" id="password2" required />
      </div>

      <button type="submit">회원가입</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';

export default {
  name: 'Signup',
  setup() {
    const username = ref('');
    const fullname = ref('');
    const password = ref('');
    const password2 = ref('');
    const email = ref('');
    const router = useRouter();
    const authStore = useAuthStore();

    const handleSubmit = async () => {
      if (password.value !== password2.value) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/accounts/api/register/', {
          username: username.value,
          fullname: fullname.value,
          password: password.value,
          email: email.value,
        });

        if (response.status === 201) {
          const loginResponse = await axios.post('http://localhost:8000/accounts/api/token/', {
            username: username.value,
            password: password.value,
          });

          authStore.setAuthToken(loginResponse.data.access);

          alert('회원가입 성공');
          router.push('/login');
        }
      } catch (error) {
        console.error(error);
        alert('회원가입 실패');
      }
    };

    return { username, fullname, password, password2, email, handleSubmit };
  },
};
</script>

<style scoped>
.signup-page {
  max-width: 450px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.signup-page h1 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 32px;
  color: #333;
  font-weight: 700;
}

.signup-page form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #555;
  margin-bottom: 6px;
}

.signup-page input {
  width: 100%;
  padding: 12px 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-sizing: border-box;
  background-color: #fff;
  transition: border-color 0.3s ease;
}

.signup-page input:focus {
  border-color: #4e73df;
  outline: none;
  box-shadow: 0 0 8px rgba(78, 115, 223, 0.3);
}

.signup-page button {
  padding: 12px;
  background-color: #4e73df;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.signup-page button:hover {
  background-color: #3557a5;
}

.signup-page button:focus {
  outline: none;
}

.signup-page input,
.signup-page button {
  font-family: 'Helvetica Neue', sans-serif;
}

</style>
