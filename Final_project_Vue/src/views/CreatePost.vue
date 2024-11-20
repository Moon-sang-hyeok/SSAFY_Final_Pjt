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
        <button type="submit">게시글 작성</button>
      </form>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from "@/stores/auth";  // Pinia store import
  
  export default {
    data() {
      return {
        title: "",  // 제목
        content: "", // 내용
      };
    },
    methods: {
      submitPost() {
        const authStore = useAuthStore(); // Pinia store 가져오기
        const token = authStore.token; // 저장된 토큰 가져오기
  
        if (!token) {
          alert("로그인이 필요합니다.");
          return;
        }
  
        const postData = {
          title: this.title,
          content: this.content,
        };
  
        fetch("http://localhost:8000/api/posts/create/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,  // 토큰을 헤더에 추가
          },
          body: JSON.stringify(postData), // 게시글 데이터 전송
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("게시글 작성에 실패했습니다.");
            }
            return response.json();
          })
          .then((data) => {
            // 작성된 게시글 페이지로 이동
            this.$router.push(`/posts/${data.id}`);
          })
          .catch((error) => {
            console.error(error);
            alert("게시글 작성 중 오류가 발생했습니다.");
          });
      },
    },
  };
  </script>
  
  <style scoped>
  form {
    margin-top: 20px;
  }
  input, textarea {
    width: 100%;
    margin-bottom: 10px;
  }
  </style>
  