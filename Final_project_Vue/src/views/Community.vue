<template>
  <div>
    <h1>커뮤니티 게시판</h1>
    <button @click="navigateToCreatePost">게시글 작성</button>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <router-link :to="'/posts/' + post.id">{{ post.title }}</router-link> - {{ post.author }}
      </li>
    </ul>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth';  // Pinia store import
import axios from 'axios';

export default {
  name: 'Community',
  data() {
    return {
      posts: [], // 게시글 목록을 저장할 변수
    };
  },
  methods: {
    async fetchPosts() {
      const authStore = useAuthStore(); // Pinia store에서 토큰을 가져옴
      const token = authStore.token; // 저장된 토큰을 가져옴
      console.log('헤더에 전달되는 토큰:', token);

      // 토큰이 없다면 로그인 페이지로 리디렉션
      if (!token) {
        alert('로그인 후 게시글을 조회할 수 있습니다.');
        this.$router.push('/login');  // 로그인 페이지로 리디렉션
        return;
      }

      // API 요청 시 Authorization 헤더에 토큰을 포함
      try {
        const response = await axios.get('http://localhost:8000/api/posts/', {
          headers: {
            Authorization: `Bearer ${token}`, // Bearer 방식으로 토큰을 전달
          },
        });
        console.log(response.status);  // 상태 코드 확인
        console.log(response.data); 

        this.posts = response.data; // 게시글 목록을 처리
      } catch (error) {
        console.error('게시글 목록을 가져오는 데 실패했습니다.', error);
        console.error(error.response.status);  // 오류 상태 코드 확인
        console.error(error.response.data); 
        alert('게시글 목록을 가져오는 데 실패했습니다.');
      }
    },
    navigateToCreatePost() {
      this.$router.push('/create-post'); // 게시글 작성 페이지로 이동
    },
  },
  mounted() {
    this.fetchPosts(); // 페이지가 로드될 때 게시글을 가져옴
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

a {
  text-decoration: none;
  color: #333;
}

a:hover {
  text-decoration: underline;
}

button {
  margin: 10px 0;
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
