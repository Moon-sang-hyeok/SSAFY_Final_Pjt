import { defineStore } from 'pinia';
import { jwtDecode} from 'jwt-decode'; // JWT 검증 라이브러리 추가

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
  }),

  actions: {
    setAuthToken(token) {
      this.token = token;
      localStorage.setItem('auth_token', token);
    },

    setUser(userId) {
      this.user = userId;
      localStorage.setItem('user_id', userId);
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user_id');
    },

    initialize() {
      const token = localStorage.getItem('auth_token');
      const userId = localStorage.getItem('user_id');
      if (token && this.isTokenValid(token)) {
        this.token = token;
        this.user = userId ? Number(userId) : null;
      } else {
        this.logout(); // 토큰이 유효하지 않으면 로그아웃 처리
      }
    },

    isTokenValid(token) {
      try {
        const decoded = jwtDecode(token);
        return decoded.exp > Date.now() / 1000;
      } catch (error) {
        return false;
      }
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.token && state.user !== null,
    currentUser: (state) => state.user,
  },
});
