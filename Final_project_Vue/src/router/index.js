import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Community from '../views/Community.vue'  // 커뮤니티 페이지
import CreatePost from '../views/CreatePost.vue'  // 게시글 작성 페이지
import PostDetail from '../views/PostDetail.vue'  // 게시글 상세 페이지


const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { path: '/community', component: Community }, // 커뮤니티 페이지
  { path: '/create-post', component: CreatePost }, // 게시글 작성 페이지
  { path: '/posts/:id', component: PostDetail, props: true }, // 게시글 상세 페이지
  // 다른 라우트들...
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
