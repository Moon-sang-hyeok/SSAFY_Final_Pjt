<template>
  <div class="signup-page">
    <h1>회원가입</h1>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="fullname">사용자 이름 : </label>
        <input type="text" v-model="fullname" id="fullname" required />
      </div>

      <div>
        <label for="username">아이디 : </label>
        <input type="text" v-model="username" id="username" required />
      </div>

      <div>
        <label for="password">비밀번호 : </label>
        <input type="password" v-model="password" id="password" required />
      </div>

      <div>
        <label for="password2">비밀번호 확인 : </label>
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
    const username = ref(''); // 아이디
    const fullname = ref(''); // 사용자이름
    const password = ref('');
    const password2 = ref('');
    const router = useRouter();
    const authStore = useAuthStore();

    const handleSubmit = async () => {
      if (password.value !== password2.value) {
        alert('비밀번호가 일치하지 않습니다.');
        return;
      }

      try {
        // 회원가입 API 호출
        const response = await axios.post('http://localhost:8000/accounts/api/register/', {
          username: username.value,  // 아이디
          fullname: fullname.value,          // 사용자이름
          password: password.value,
        });

        if (response.status === 201) {
          // 회원가입 성공 후, 로그인 API 호출
          const loginResponse = await axios.post('http://localhost:8000/accounts/api/token/', {
            username: username.value,  // 아이디로 로그인
            password: password.value,
          });

          // 로그인 성공 후 토큰 저장
          authStore.setAuthToken(loginResponse.data.access);

          alert('회원가입 성공');
          router.push('/login');  // 로그인 페이지로 이동
        }
      } catch (error) {
        console.error(error);
        alert('회원가입 실패');
      }
    };

    return { username, fullname, password, password2, handleSubmit };
  },
};
</script>

<style scoped>
.signup-page {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.signup-page h1 {
  text-align: center;
  margin-bottom: 20px;
}

.signup-page form {
  display: flex;
  flex-direction: column;
}

.signup-page label {
  margin: 10px 0 5px;
}

.signup-page input {
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.signup-page button {
  padding: 10px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.signup-page button:hover {
  background-color: #555;
}
</style>
