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
  import { useAuthStore } from "@/stores/auth";  // Pinia store 가져오기
  
  export default {
    data() {
      return {
        posts: [], // 게시글 목록 데이터
      };
    },
    mounted() {
      this.fetchPosts();  // 컴포넌트가 마운트되면 게시글 목록을 가져옵니다.
    },
    methods: {
      // 게시글을 가져오는 메소드
      async fetchPosts() {
        const authStore = useAuthStore();  // Pinia store에서 인증 상태를 가져옵니다.
        const token = authStore.token;  // 저장된 토큰을 가져옵니다.
  
        console.log("토큰 확인: ", token);  // 디버깅용으로 토큰 확인
  
        if (!token) {
          alert("로그인 후 게시글을 조회할 수 있습니다.");
          return;  // 로그인하지 않으면 게시글을 가져오지 않습니다.
        }
  
        // 인증 토큰을 포함하여 게시글을 가져오는 API 호출
        fetch("http://localhost:8000/api/posts/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${token}`,  // 인증 토큰을 헤더에 추가
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("게시글 목록을 가져오는 데 실패했습니다.");
            }
            return response.json();  // JSON 형식으로 응답 처리
          })
          .then((data) => {
            this.posts = data;  // 받아온 게시글 목록을 저장
          })
          .catch((error) => {
            console.error(error);
            alert("게시글 목록을 가져오는 데 문제가 발생했습니다.");
          });
      },
      // 게시글 작성 페이지로 이동
      navigateToCreatePost() {
        this.$router.push("/create-post");
      },
    },
  };
  </script>
  
  <style scoped>
  /* 스타일 코드 */
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
  