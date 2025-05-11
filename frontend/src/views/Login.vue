<template>
  <!-- 登录页面容器 -->
  <div class="login-container">
    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- Logo和标题容器 -->
      <div class="logo-container">
        <img src="/img/logo1.png" alt="Logo" class="logo">
        <h1 class="system-title">自习室预约系统</h1>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 用户名输入框 -->
        <div class="form-group">
          <div class="input-container">
            <label>用户名</label>
            <input
              v-model="username"
              type="text"
              required
              placeholder="请输入用户名"
              :disabled="loading"
            />
          </div>
        </div>
        
        <!-- 密码输入框 -->
        <div class="form-group">
          <div class="input-container">
            <label>密码</label>
            <input
              v-model="password"
              type="password"
              required
              placeholder="请输入密码"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- 记住我选项 -->
        <div class="remember-me">
          <label>
            <input type="checkbox" v-model="rememberMe">
            记住我
          </label>
        </div>

        <!-- 错误信息显示 -->
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <!-- 登录按钮 -->
        <button type="submit" :disabled="loading" class="login-button">
          <span v-if="loading">登录中...</span>
          <span v-else>登录</span>
        </button>

        <!-- 管理员登录按钮 -->
        <button type="button" class="admin-login-button" @click="goToAdminLogin">
          管理员登录
        </button>

        <!-- 额外链接 -->
        <div class="additional-links">
          <a href="#" @click.prevent="goToRegister" class="register-link">注册账号</a>
          <a href="#" @click.prevent="goToForgotPassword" class="forgot-password">忘记密码？</a>
        </div>

        <!-- 版权信息 -->
        <div class="copyright">
          © 2000-2024 自习室预约系统
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    const rememberMe = ref(false)

    const handleLogin = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await axios.post('/api/login/', {
          name: username.value,
          password: password.value,
          remember_me: rememberMe.value
        }, {
          withCredentials: true
        })

        if (response.data.success) {
          if (response.data.redirect_url) {
            window.location.href = response.data.redirect_url
          } else {
            window.location.href = '/'
          }
        } else {
          error.value = response.data.message || '登录失败，请检查账号和密码'
        }
      } catch (err: any) {
        console.error('Login error:', err)
        error.value = '用户登录失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    const goToAdminLogin = () => {
      window.location.href = 'http://localhost:8000/admin/login/'
    }

    const goToRegister = () => {
      router.push('/register')
    }

    const goToForgotPassword = () => {
      router.push('/forgot-password')
    }

    return {
      username,
      password,
      loading,
      error,
      rememberMe,
      handleLogin,
      goToAdminLogin,
      goToRegister,
      goToForgotPassword
    }
  }
})
</script>

<style lang="scss" scoped>
/* 登录页面容器样式 */
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100vw;
  padding: 20px;
  background-image: url('@/assets/images/666.png');
  background-size: 100% 100%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #f5f5f5;
  position: relative;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  overflow: hidden;

  @media (max-width: 768px) {
    background-size: cover;
  }
}

/* 登录卡片样式 */
.login-card {
  background: rgba(255, 255, 255, 0.7);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  width: 100%;
  max-width: 380px;
  position: relative;
  z-index: 1;
  animation: cardFloat 6s ease-in-out infinite;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.3);

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: -1;
    border-radius: 20px;
    background: linear-gradient(
      45deg,
      rgba(255, 255, 255, 0.1),
      rgba(255, 255, 255, 0.2)
    );
  }
}

/* Logo容器样式 */
.logo-container {
  text-align: center;
  margin-bottom: 20px;
  
  .logo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover; /* 修改回cover以填充满圆形 */
    box-shadow: 0 0 20px rgba(107, 115, 255, 0.2);
    border: 2px solid rgba(107, 115, 255, 0.3);
    padding: 0; /* 移除内边距使图片完全填充 */
    background: white;
    transition: transform 0.3s ease;
    
    &:hover {
      transform: scale(1.05);
    }
  }

  /* 系统标题样式 */
  .system-title {
    font-size: 20px;
    color: #333;
    margin: 10px 0;
    font-weight: 600;
    background: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
}

.login-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 500;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 16px;

  .input-container {
    label {
      display: block;
      color: #666;
      font-size: 14px;
      margin-bottom: 6px;
      font-weight: 500;
    }

    input {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #eee;
      border-radius: 8px;
      font-size: 14px;
      transition: all 0.3s ease;
      background: rgba(255, 255, 255, 0.9);

      &:focus {
        outline: none;
        border-color: #ff9a9e;
        box-shadow: 0 0 0 3px rgba(255, 154, 158, 0.1);
      }

      &::placeholder {
        color: #aaa;
      }
    }
  }
}

/* 记住我选项样式 */
.remember-me {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  
  label {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #666;
    font-size: 13px;
    cursor: pointer;

    input[type="checkbox"] {
      width: 14px;
      height: 14px;
      accent-color: #ff9a9e;
    }
  }
}

/* 登录按钮样式 */
.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 16px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
}

/* 管理员登录按钮样式 */
.admin-login-button {
  width: 100%;
  padding: 12px;
  background: transparent;
  color: #666;
  border: 2px solid rgba(255, 154, 158, 0.5);
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 16px;
  margin-top: 8px;

  &:hover:not(:disabled) {
    background: rgba(255, 154, 158, 0.1);
    border-color: #ff9a9e;
    color: #ff9a9e;
  }

  &:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
}

/* 额外链接样式 */
.additional-links {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  
  a {
    color: #ff9a9e;
    text-decoration: none;
    font-size: 13px;
    transition: color 0.3s ease;

    &:hover {
      color: #ff7a7e;
    }
  }
}

/* 错误信息样式 */
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: #fff5f5;
  color: #e53e3e;
  border-radius: 8px;
  font-size: 13px;
  border: 1px solid #fed7d7;
  margin-bottom: 16px;
}

/* 版权信息样式 */
.copyright {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 20px;
}

/* 登录卡片浮动动画 */
@keyframes cardFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* 响应式布局 */
@media (max-width: 480px) {
  .login-card {
    padding: 20px;
  }

  .system-title {
    font-size: 18px;
  }

  .logo {
    width: 70px;
    height: 70px;
  }

  .login-type-switch .switch-btn {
    padding: 8px 16px;
    font-size: 13px;
  }
}

.additional-links a {
  cursor: pointer;
}
</style> 