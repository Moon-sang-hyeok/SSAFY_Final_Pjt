<template>
  <div class="community-container">
    <h1 class="page-title">게시글 목록</h1>

    <!-- 게시글 목록 -->
    <div v-if="posts.length" class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2 class="post-title">
          <router-link :to="'/post/' + post.id" class="post-link">{{ post.title }}</router-link>
        </h2>
        <p class="post-meta">
          작성자: <span class="author-name">{{ post.author }}</span>
        </p>

        <!-- 관리자가 작성한 게시글만 수정, 삭제 가능 -->
        <div v-if="isLoggedIn && post.author === currentUser" class="post-actions">
          <router-link :to="'/edit/' + post.id" class="action-btn edit-btn">수정</router-link>
          <button @click="deletePost(post.id)" class="action-btn delete-btn">삭제</button>
        </div>
      </div>
    </div>

    <!-- 새 게시글 작성 버튼 -->
    <button v-if="isLoggedIn" @click="createPost" class="create-post-btn">새 게시글 작성</button>

    <!-- 게시글이 없을 경우 메시지 -->
    <div v-else class="no-posts-message">
      <p>게시글이 없습니다. 새 게시글을 작성해보세요!</p>
    </div>
  </div>
</template>

<script>
import api from '../api';
import { useAuthStore } from '../stores/auth';  // Pinia store 임포트

export default {
  data() {
    return {
      posts: [],  // 게시글 목록
      currentUser: null,  // 현재 사용자 정보
    };
  },
  computed: {
    // Pinia store를 컴포넌트에서 사용
    isLoggedIn() {
      const authStore = useAuthStore();
      return authStore.isAuthenticated;  // 인증된 상태인지 확인
    },
  },
  methods: {
    // 게시글 가져오기
    async fetchPosts() {
      try {
        const response = await api.get('http://localhost:8000/api/posts/');
        this.posts = response.data;
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    },

    // 로그인 상태 확인
    async checkLoginStatus() {
      try {
        const authStore = useAuthStore();  // Pinia store 접근
        const token = authStore.token;
        
        if (!token) {
          this.isLoggedIn = false;
          return;  // 토큰이 없다면 로그인되지 않은 상태로 처리
        }

        // JWT 토큰을 Authorization 헤더에 포함시켜 요청
        const response = await api.get('http://localhost:8000/accounts/status/', {
          headers: {
            'Authorization': `Bearer ${token}`,  // Bearer 토큰 방식
          }
        });

        if (response.data.is_logged_in) {
          this.currentUser = response.data.user.username;  // 로그인한 사용자 정보
        }
      } catch (error) {
        console.error('Error checking login status:', error);
        this.isLoggedIn = false;  // 로그인 오류가 있으면 상태를 false로 설정
      }
    },

    // 게시글 삭제
    async deletePost(postId) {
      try {
        await api.delete(`posts/${postId}/`);
        this.fetchPosts();  // 삭제 후 게시글 목록 새로 고침
      } catch (error) {
        console.error('Error deleting post:', error);
      }
    },

    // 새 게시글 작성 페이지로 이동
    createPost() {
      this.$router.push('/create');  // 새 게시글 작성 페이지로 이동
    },
  },
  created() {
    this.fetchPosts();
    this.checkLoginStatus();  // 페이지가 로드될 때 로그인 상태 확인
  },
};
</script>

<style scoped>
/* 전체 컨테이너 */
.community-container {
  max-width: 950px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
  font-family: 'Noto Sans', sans-serif;
}

/* 페이지 제목 */
.page-title {
  font-size: 2.2rem;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-bottom: 40px;
}

/* 게시글 목록 */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

/* 게시글 카드 */
.post-card {
  background-color: #f7f8f9;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

/* 게시글 제목 */
.post-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 12px;
}

.post-link {
  text-decoration: none;
  color: inherit;
  font-weight: 600;
}

.post-link:hover {
  color: #007bff;
}

/* 작성자 정보 */
.post-meta {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 10px;
}

.author-name {
  font-weight: 500;
}

/* 게시글 관리 버튼 */
.post-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  font-size: 1rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: center;
}

/* 삭제 버튼 */
.delete-btn {
  background-color: #ff4d4f;
  color: white;
  border: none;
}

.delete-btn:hover {
  background-color: #e12f36;
}

/* 수정 버튼 */
.edit-btn {
  background-color: #f0a500;
  color: white;
  border: none;
}

.edit-btn:hover {
  background-color: #d88c00;
}

/* 새 게시글 작성 버튼 */
.create-post-btn {
  background-color: #2f5cb5;
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 1.1rem;
  width: 100%;
  margin-top: 35px;
  cursor: pointer;
  transition: background-color 0.3s;
  border: none;
}

.create-post-btn:hover {
  background-color: #1c4782;
}

/* 게시글이 없을 때 메시지 */
.no-posts-message {
  text-align: center;
  font-size: 1.3rem;
  color: #999;
  margin-top: 50px;
}
</style>
