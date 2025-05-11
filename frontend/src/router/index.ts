import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LoginView from '../views/Login.vue'
import RegisterView from '../views/Register.vue'
import ForgotPasswordView from '../views/ForgotPassword.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPasswordView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      // 尝试获取用户信息来验证登录状态
      const response = await fetch('http://localhost:8000/api/user/info/', {
        credentials: 'include'
      })
      const data = await response.json()
      
      if (data.success) {
        next()
      } else {
        next('/login')
      }
    } catch (error) {
      console.error('验证登录状态失败:', error)
      next('/login')
    }
  } else {
    next()
  }
})

export default router 