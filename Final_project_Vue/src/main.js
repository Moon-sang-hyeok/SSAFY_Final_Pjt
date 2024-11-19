import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory} from 'vue-router'







// 페이지 컴포넌트 임포트
import App from './App.vue'
import MainPage from './views/MainPage.vue'
import ExchangePage from './views/Exchange.vue'
import SavingsComparisonPage from './views/SavingsComparison.vue'
import NearbyBanksPage from './views/NearbyBanks.vue'
import RecommendPage from './views/Recommend.vue'
import CommunityPage from './views/Community.vue'
import ProfilePage from './views/Profile.vue'
import LoginPage from './views/Login.vue'
import SignupPage from './views/Signup.vue'



// 라우터 설정
const routes =[
    { path: '/', component: MainPage},
    { path: '/exchange', component: ExchangePage},
    { path: '/savings-comparison', component: SavingsComparisonPage},
    { path: '/nearby-banks', component: NearbyBanksPage},
    { path: '/recommend', component: RecommendPage},
    { path: '/community', component: CommunityPage},
    { path: '/profile', component: ProfilePage},
    { path: '/login', component: LoginPage},
    { path: '/signup', component: SignupPage},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
app.use(createPinia())
app.use(router)

app.mount('#app')