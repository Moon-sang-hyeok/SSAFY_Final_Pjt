import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue';
import SavingsComparison from '@/views/ProductsComparison.vue'; // 부모 뷰
import SavingsProductDetail from '@/components/SavingsProductDetail.vue'; // 상세 정보 뷰
import DepositsProductDetail from '@/components/DepositsProductDetail.vue'
import PostDetail from '@/views/PostDetail.vue';
import PostCreate from '../views/PostCreate.vue';
import PostEdit from '@/views/PostEdit.vue';
import Portfolio from '@/views/Portfolio.vue';
import Recommend from '@/views/Recommend.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/signup', component: Signup },
  { 
    path: '/products-comparison', 
    component: ProductsComparison // 부모 컴포넌트
  },
  { 
    path: '/savings-comparison/:id', 
    component: SavingsProductDetail, // 상세 정보 컴포넌트
    props: true, // id를 props로 전달
  },
  { 
    path: '/deposits-comparison/:id', 
    component: DepositsProductDetail, // 상세 정보 컴포넌트
    props: true, // id를 props로 전달
  },
  {
    path: '/posts/:id',  // :id는 게시글의 고유 ID
    name: 'post-detail',
    component: PostDetail,  // 게시글 상세보기 컴포넌트
    props: true,  // URL 파라미터를 props로 전달
  },
  {
    path: '/edit/:id',  // :id는 게시글의 고유 ID
    name: 'post-edit',
    component: PostEdit,  // 게시글 상세보기 컴포넌트
    props: true,  // URL 파라미터를 props로 전달
  },
  {
    path: '/create',
    name: 'create-post',
    component: PostCreate,  // 게시글 작성 페이지
  },
  {
    path: '/portfolio',
    component: Portfolio,  // 포트폴리오
  },
  {
    path: '/recommend',
    component: Recommend,  // 포트폴리오
  },
  
  
  
  // 다른 라우트들...
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
