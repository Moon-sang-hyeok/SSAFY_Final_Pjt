<!-- PostDetail.vue -->
<template>
    <div>
      <h1>{{ post.title }}</h1>
      <p><strong>작성자:</strong> {{ post.author }}</p>
      <p><strong>작성일:</strong> {{ post.created_at }}</p>
      <p>{{ post.content }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        post: {}, // 게시글 상세 데이터
      };
    },
    mounted() {
      const postId = this.$route.params.id; // URL에서 게시글 ID를 가져옴
      this.fetchPost(postId); // 해당 게시글 ID로 게시글 정보 불러오기
    },
    methods: {
      // 게시글 상세 정보를 가져오는 함수
      fetchPost(postId) {
        fetch(`http://localhost:8000/api/posts/${postId}/`)
          .then((response) => response.json())
          .then((data) => {
            this.post = data; // 가져온 게시글 정보를 post에 저장
          });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 스타일은 필요에 맞게 추가 */
  h1 {
    margin-bottom: 20px;
  }
  </style>
  