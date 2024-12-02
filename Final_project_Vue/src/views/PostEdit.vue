<template>
  <div class="post-form">
    <div class="form-container">
      <h1>게시글 수정</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">제목</label>
          <input id="title" v-model="post.title" placeholder="제목을 입력하세요" required />
        </div>
        <div class="form-group">
          <label for="content">내용</label>
          <textarea id="content" v-model="post.content" placeholder="내용을 입력하세요" required></textarea>
        </div>
        <div class="form-actions">
          <button type="submit" class="submit-btn">수정하기</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from "../api";

export default {
  data() {
    return {
      post: {
        title: "",
        content: "",
      },
      postId: this.$route.params.id, // URL에서 게시글 ID 받기
    };
  },
  methods: {
    async fetchPost() {
      try {
        const response = await api.get(`posts/${this.postId}/`);
        this.post = response.data;
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    },
    async handleSubmit() {
      try {
        await api.put(`posts/${this.postId}/`, this.post);
        this.$router.push(`/post/${this.postId}`); // 수정 후 상세 페이지로 리디렉션
      } catch (error) {
        console.error("Error submitting post:", error);
      }
    },
  },
  created() {
    this.fetchPost(); // 컴포넌트가 생성되면 해당 게시글 정보 로드
  },
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.post-form {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9f9f9;
  padding: 20px;
}

/* 폼 컨테이너 */
.form-container {
  width: 100%;
  max-width: 500px;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
h1 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

/* 폼 그룹 */
.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 14px;
  margin-bottom: 5px;
  color: #666;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

input:focus,
textarea:focus {
  border-color: #0066cc;
}

/* 텍스트박스 높이 */
textarea {
  min-height: 150px;
  resize: vertical;
}

/* 버튼 스타일 */
.form-actions {
  display: flex;
  justify-content: center;
}

.submit-btn {
  padding: 12px 20px;
  background-color: #0066cc;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #004d99;
}

/* 반응형 처리 */
@media (max-width: 768px) {
  .form-container {
    padding: 20px;
  }

  h1 {
    font-size: 20px;
  }

  input,
  textarea {
    font-size: 14px;
  }
}
</style>
