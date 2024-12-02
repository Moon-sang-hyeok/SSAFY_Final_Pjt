<template>
  <div class="post-form">
    <h1>{{ isEdit ? '게시글 수정' : '새 게시글 작성' }}</h1>
    <form @submit.prevent="handleSubmit">
      <input v-model="post.title" placeholder="제목" required />
      <textarea v-model="post.content" class='custom-textarea' placeholder="- 욕설 및 비하 게시물은 제재 대상입니다." required></textarea>
      <button type="submit">{{ isEdit ? '수정' : '작성' }}</button>
    </form>
  </div>
</template>

<script>
import api from '../api';  // 수정된 api.js 파일을 import 합니다.
import { ref } from 'vue';

export default {
  data() {
    return {
      post: {
        title: '',
        content: '',
      },
      isEdit: false,
      postId: null,
    };
  },
  methods: {
    async handleSubmit() {
      try {
        if (this.isEdit) {
          // 게시글 수정
          await api.put(`posts/${this.postId}/`, this.post);
        } else {
          // 새 게시글 작성
          await api.post('posts/', this.post);
        }
        this.$router.push('/community');  // 게시글 작성 후 홈으로 리디렉션
      } catch (error) {
        if (error.response) {
          // 서버가 응답을 반환한 경우
          console.error('게시글 제출 중 서버 오류:', error.response.data);
        } else {
          // 서버가 응답을 반환하지 않은 경우
          console.error('게시글 제출 중 오류 발생:', error.message);
        }
      }
    },
    async fetchPost() {
      if (this.isEdit) {
        try {
          const response = await api.get(`posts/${this.postId}/`);
          this.post = response.data;
        } catch (error) {
          console.error('Error fetching post:', error);
        }
      }
    },
  },
  created() {
    this.isEdit = this.$route.params.id != null;
    if (this.isEdit) {
      this.postId = this.$route.params.id;
      this.fetchPost();
    }
  },
};
</script>

<style scoped>
.custom-textarea {
  font-size: 16px; /* 글자 크기 설정 */
  color: #333; /* 글자 색상 설정 */
  padding: 12px;
  margin-bottom: 20px;
  font-size: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  transition: border 0.3s ease;
}

.custom-textarea::placeholder {
  color: #aaa; /* placeholder 텍스트 색상 설정 */
  font-size: 12px; /* placeholder 텍스트 크기 설정 */
}

.custom-textarea:focus {
  border-color: #007bff;
  outline: none;
}
.post-form {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

input, textarea {
  margin-bottom: 20px;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #fff;
  transition: border 0.3s ease;
}

input:focus, textarea:focus {
  border-color: #007bff;
  outline: none;
}

textarea {
  resize: vertical;
  min-height: 120px;
}

button {
  padding: 12px;
  font-size: 16px;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

button:focus {
  outline: none;
}

@media (max-width: 600px) {
  .post-form {
    padding: 20px;
  }

  input, textarea, button {
    font-size: 14px;
  }
}
</style>
