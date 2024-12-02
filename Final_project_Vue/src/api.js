// api.js
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';  // Pinia store에서 auth 저장소를 가져옵니다.

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',  // API 서버의 기본 URL
});

// 요청 인터셉터를 사용하여 JWT 토큰을 자동으로 헤더에 추가합니다.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');  // Pinia store에서 저장된 JWT 토큰 가져오기

    // 토큰이 존재하면 Authorization 헤더에 토큰을 추가
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
