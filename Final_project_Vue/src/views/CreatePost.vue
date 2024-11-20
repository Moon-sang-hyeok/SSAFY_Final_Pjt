<template>
  <div>
    <h1>게시글 작성</h1>
    <form @submit.prevent="submitPost">
      <div>
        <label for="title">제목:</label>
        <input type="text" v-model="title" id="title" required />
      </div>

      <div>
        <label for="content">내용:</label>
        <textarea v-model="content" id="content" required></textarea>
      </div>

      <button type="submit">작성</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '../stores/auth';  // Pinia store import

export default {
  name: 'CreatePost',
  data() {
    return {
      title: '',
      content: '',
    };
  },
  methods: {
    async submitPost() {
      const authStore = useAuthStore(); // Pinia store에서 토큰을 가져옴
      const token = authStore.token; // 저장된 토큰을 가져옴

      if (!token) {
        alert('로그인 후 게시글을 작성할 수 있습니다.');
        this.$router.push('/login');  // 로그인 페이지로 리디렉션
        return;
      }

      // POST 요청 시 Authorization 헤더에 토큰을 포함
      try {
        const response = await axios.post(
          'http://localhost:8000/api/posts/create/', 
          {
            title: this.title,
            content: this.content,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`, // Bearer 방식으로 토큰을 전달
            }
          }
        );

        alert('게시글 작성 성공!');
        this.$router.push('/community');  // 게시글 작성 후 홈으로 리디렉션
      } catch (error) {
        console.error('게시글 작성에 실패했습니다.', error);
        alert('게시글 작성에 실패했습니다.');
      }
    },
  },
};
</script>

<style scoped>
/* 스타일 코드 */
h1 {
  text-align: center;
}

form {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 15px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #555;
}
</style>
