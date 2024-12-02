<template>
  <div v-if="post" class="post-detail">
    <div class="post-container">
      <!-- 게시글 메타 정보 -->
      <router-link to="/community" class="back-link">
        <img src="@/assets/back.svg" alt="목록" class="back-image" />
      </router-link>
      <div class="post-meta">
        
        <!-- 게시글 메타 정보 -->
      <div class="post-meta">
        <p class="meta-item">
          <span class="meta-label">작성자:</span>
          <span>{{ post.author }}</span>
        </p>
      </div>
      <div class="post-meta">
          <p class="meta-item">
          <span class="meta-label">작성일:</span>
          <span>{{ formattedDate }}</span>
        </p>
      </div>
    </div>
      <h1 class="post-title">제목 : {{ post.title }}</h1>
      <p class="post-content">{{ post.content }}</p>
      <br>
      <br>

      <!-- 수정/삭제 버튼 -->
      <div v-if="isLoggedIn && post.author_id === currentUser" class="post-actions">
        <router-link :to="'/edit/' + post.id" class="edit-btn">게시글 수정</router-link>
        <button @click="deletePost(post.id)" class="delete-btn">게시글 삭제</button>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments">
        <h3>댓글</h3>
        <div v-for="comment in post.comments" :key="comment.id" class="comment">
          <div v-if="editingComment && editingComment.id === comment.id" class="edit-comment">
            <textarea v-model="editingComment.content"></textarea>
            <button @click="updateComment(comment.id)" class="save-btn">댓글 수정</button>
            <button @click="cancelEdit" class="cancel-btn">취소</button>
          </div>
          <div v-else>
            <p class="comment-content">{{ comment.content }}</p>
            <div class="comment-meta">
              <span>작성자: {{ comment.author }}</span>
            </div>
            <div v-if="isLoggedIn && comment.author_id === currentUser" class="comment-actions">
              <button @click="editComment(comment)" class="edit-btn">수정</button>
              <button @click="deleteComment(comment.id)" class="delete-btn">삭제</button>
            </div>
          </div>
        </div>

        <!-- 댓글 작성 -->
        <div v-if="isLoggedIn" class="add-comment">
          <textarea v-model="newComment" placeholder="댓글을 작성해주세요"></textarea>
          <button @click="addComment" class="add-btn">댓글 추가</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import api from "../api";
import { useAuthStore } from "../stores/auth"; // Pinia store import
import dayjs from "dayjs"; // dayjs import

export default {
  props: ["id"],
  data() {
    return {
      post: null,
      newComment: "",
      isLoggedIn: false,
      currentUser: null,
      editingComment: null,
    };
  },
  computed: {
    formattedDate() {
      return this.post ? dayjs(this.post.created_at).format("YYYY년 MM월 DD일 HH:mm") : "";
    },
  },
  methods: {
    async fetchPost() {
      try {
        const response = await api.get(`posts/${this.id}/`);
        this.post = response.data;
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    },
    async deletePost(postId) {
      try {
        await api.delete(`posts/${postId}/`);
        this.$router.push("/community");
      } catch (error) {
        console.error("Error deleting post:", error);
      }
    },
    async deleteComment(commentId) {
      try {
        await api.delete(`comments/${commentId}/`);
        this.fetchPost();
      } catch (error) {
        console.error("Error deleting comment:", error);
      }
    },
    async addComment() {
      try {
        const commentData = { content: this.newComment, post: this.id };
        await api.post("comments/", commentData);
        this.newComment = "";
        this.fetchPost();
      } catch (error) {
        console.error("Error adding comment:", error);
      }
    },
    editComment(comment) {
      this.editingComment = { ...comment };
    },
    async updateComment(commentId) {
      try {
        await api.put(`comments/${commentId}/`, { content: this.editingComment.content });
        this.fetchPost();
        this.editingComment = null;
      } catch (error) {
        console.error("Error updating comment:", error);
      }
    },
    cancelEdit() {
      this.editingComment = null;
    },
  },
  created() {
    const authStore = useAuthStore();
    this.isLoggedIn = !!localStorage.getItem("auth_token");
    this.currentUser = authStore.user;
    this.fetchPost();
  },
};
</script>

<style scoped>
.back-link {
  display: inline-block;
  text-decoration: none;
  margin-bottom: 15px;
}

.back-image {
  width: 60px; /* 이미지 크기 조정 */
  height: auto;
}

/* 전체 컨테이너 */
.post-detail {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #f9f9f9;
}

.post-container {
  max-width: 800px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
}

/* 게시글 메타 정보 */
.post-meta {
  display: flex;
  justify-content: space-between;  /* 양쪽 끝에 배치 */
  font-size: 14px;
  color: #777;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  justify-content: space-between;  /* 양쪽 끝에 배치 */
  width: 100%;
}

.meta-label {
  font-weight: bold;
  color: #333;
}

/* 게시글 스타일 */
.post-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.post-content {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.6;
}

.post-meta p {
  font-size: 14px;
  color: #777;
  margin: 5px 0;
}

.post-meta span {
  font-weight: bold;
  color: #333;
}

/* 버튼 스타일 */
.post-actions,
.comment-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn,
.add-btn,
.save-btn,
.cancel-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.edit-btn {
  background-color: #0066cc;
  color: #fff;
}

.delete-btn {
  background-color: #ff4d4d;
  color: #fff;
}

.add-btn,
.save-btn {
  background-color: #28a745;
  color: #fff;
}

.cancel-btn {
  background-color: #6c757d;
  color: #fff;
}

.edit-btn:hover,
.delete-btn:hover,
.add-btn:hover,
.save-btn:hover,
.cancel-btn:hover {
  opacity: 0.8;
}

/* 댓글 섹션 */
.comments {
  margin-top: 30px;
}

.comment {
  padding: 15px;
  margin-bottom: 10px;
  background: #f1f1f1;
  border-radius: 5px;
}

.comment-content {
  font-size: 14px;
  color: #444;
}

.add-comment textarea {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.add-comment .add-btn {
  margin-top: 10px;
}
</style>
