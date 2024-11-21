import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory} from 'vue-router'







// 페이지 컴포넌트 임포트
import App from './App.vue'
import MainPage from './views/MainPage.vue'
import ExchangePage from './views/Exchange.vue'
import ProductsComparisonPage from './views/ProductsComparison.vue'
import NearbyBanksPage from './views/NearbyBanks.vue'
import RecommendPage from './views/Recommend.vue'
import CommunityPage from './views/Community.vue'
import ProfilePage from './views/Profile.vue'
import LoginPage from './views/Login.vue'
import SignupPage from './views/Signup.vue'
import MyPagePage from './views/MyPage.vue'
import CreatePostPage from './views/CreatePost.vue' 
import SavingsProductDetail from './components/SavingsProductDetail.vue'



// 라우터 설정
const routes =[
    { path: '/', component: MainPage},
    { path: '/exchange', component: ExchangePage},
    { path: '/products-comparison', component: ProductsComparisonPage},
    {
        path: '/savings-comparison/:id',
        component: SavingsProductDetail,
        props: true, // 라우트 매개변수를 컴포넌트로 전달
    },
    {
        path: '/deposits-comparison/:id',
        component: DepositsProductDetail,
        props: true, // 라우트 매개변수를 컴포넌트로 전달
    },
    { path: '/nearby-banks', component: NearbyBanksPage},
    { path: '/recommend', component: RecommendPage},
    { path: '/community', component: CommunityPage},
    { path: '/profile', component: ProfilePage},
    { path: '/login', component: LoginPage},
    { path: '/signup', component: SignupPage},
    { path: '/mypage', component: MyPagePage},
    { path: '/create-post', component: CreatePostPage },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)

import { useAuthStore } from './stores/auth'; // auth 스토어 가져오기
import DepositsProductDetail from './components/DepositsProductDetail.vue'
const pinia = createPinia();
app.use(pinia);
const authStore = useAuthStore();
authStore.initialize();  // 여기서 initialize를 호출하여 로컬 스토리지에서 토큰을 불러옵니다.

// app.use(createPinia())
app.use(router)

app.mount('#app')