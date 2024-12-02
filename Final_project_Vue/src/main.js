import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory} from 'vue-router'







// 페이지 컴포넌트 임포트
import App from './App.vue'
import MainPage from './views/MainPage.vue'
import ExchangePage from './views/Exchange.vue'
import SavingsComparisonPage from './views/ProductsComparison.vue'
import NearbyBanksPage from './views/NearbyBanks.vue'
import RecommendPage from './views/Recommend.vue'
import CommunityPage from './views/Community.vue'
import LoginPage from './views/Login.vue'
import SignupPage from './views/Signup.vue'
import MyPagePage from './views/MyPage.vue'
import SavingsProductDetail from './components/SavingsProductDetail.vue'
import DepositsProductDetail from './components/DepositsProductDetail.vue'
import PostCreate from './views/PostCreate.vue'
import PostDetail from './views/PostDetail.vue'
import PostEdit from './views/PostEdit.vue'
import Portfolio from './views/Portfolio.vue'
// 라우터 설정
const routes =[
    { path: '/', component: MainPage},
    { path: '/exchange', component: ExchangePage},
    { path: '/products-comparison', component: SavingsComparisonPage},
    { path: '/nearby-banks', component: NearbyBanksPage},
    { path: '/recommend', component: RecommendPage},
    { path: '/community', component: CommunityPage},
    { path: '/login', component: LoginPage},
    { path: '/signup', component: SignupPage},
    { path: '/mypage', component: MyPagePage},
    { path: '/create', component: PostCreate},
    { path: '/post/:id', component: PostDetail,props: true,},
    { path: '/edit/:id', component: PostEdit,props: true,},
    { path: '/portfolio', component: Portfolio},
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
    
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
app.use(createPinia())
app.use(router)

app.mount('#app')