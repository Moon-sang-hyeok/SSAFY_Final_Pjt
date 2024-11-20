import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('auth_token') || '',  // 로컬스토리지에서 token 가져오기
    refreshToken: localStorage.getItem('refresh_token') || '', // refreshToken 상태 추가
    user: null,  // 사용자 정보를 저장할 변수
  }),

  actions: {
    setAuthToken(token) {
      this.token = token;
      localStorage.setItem('auth_token', token);  // 토큰을 로컬스토리지에 저장
    },
    removeToken() {
      this.token = '';  // 빈 문자열로 초기화
      localStorage.removeItem('auth_token');  // 로컬 스토리지에서 토큰을 삭제
    },
    setRefreshToken(refreshToken) {
      this.refreshToken = refreshToken;
      localStorage.setItem('refresh_token', refreshToken);  // refreshToken을 로컬스토리지에 저장
    },
    
    setUser(user) {
      this.user = user;
    },
    logout() {
      this.token = '';  // 토큰을 빈 문자열로 초기화
      this.refreshToken = '';  // refreshToken도 빈 문자열로 초기화
      this.user = null;  // 사용자 정보 초기화
      localStorage.removeItem('auth_token');  // 로컬스토리지에서 token 제거
      localStorage.removeItem('refresh_token');  // 로컬스토리지에서 refreshToken 제거
    },

    // 로그인 상태 확인
    initialize() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        this.token = token;  // 로컬스토리지에서 token 가져오기
      }
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        this.refreshToken = refreshToken;  // 로컬스토리지에서 refreshToken 가져오기
      }
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.token,  // 토큰이 있으면 인증된 상태로 반환
    getUser: (state) => state.user,  // 사용자 정보 반환
  },
});
