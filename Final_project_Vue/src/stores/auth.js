import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false, // 로그인 상태
    user: null, // 사용자 정보 (로그인 시 저장)
  }),

  actions: {
    login(user) {
      this.isLoggedIn = true;
      this.user = user; // 로그인한 사용자 정보
    },

    logout() {
      this.isLoggedIn = false;
      this.user = null; // 사용자 정보 초기화
    },
  },
});
