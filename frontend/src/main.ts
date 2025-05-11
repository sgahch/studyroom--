import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:8000'  // Django服务器地址
axios.defaults.withCredentials = true  // 允许跨域携带cookie

const app = createApp(App)
app.use(router)
app.mount('#app') 