import { defineStore } from 'pinia';


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || null,  // 로컬스토리지에서 token 가져오기
    user: null,
  }),

  actions: {
    setAuthToken(token) {
      this.token = token;
      localStorage.setItem('auth_token', token);  // 토큰을 로컬스토리지에 저장
    },

    setUser(user) {
      this.user = user;
    },

    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('auth_token');  // 로그아웃 시 로컬스토리지에서 token 제거
    },

    // 로그인 상태 확인
    initialize() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        this.token = token;  // 로컬스토리지에서 token 가져오기
      }
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.token,  // 토큰이 있으면 인증된 상태로 반환
  },
});
