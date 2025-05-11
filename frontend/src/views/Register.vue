<template>
  <!-- 注册页面容器 -->
  <div class="register-container">
    <!-- 注册卡片 -->
    <div class="register-card">
      <!-- Logo和标题容器 -->
      <div class="logo-container">
        <!-- 你可以用回 Login 页面的 logo，或者用 Django 页面的 H logo -->
        <img src="/img/logo1.png" alt="Logo" class="logo">
        <h1 class="system-title">用户注册</h1>
      </div>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="register-form">
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

        <!-- 用户图片上传 -->
        <div class="form-group">
          <div class="input-container">
            <label>用户图片</label>
            <!-- 基础文件上传样式，可以后续美化 -->
            <input
              type="file"
              @change="handleFileChange"
              accept="image/*"
              :disabled="loading"
              class="file-input"
            />
          </div>
        </div>

        <!-- 手机号输入框 -->
        <div class="form-group">
          <div class="input-container">
            <label>手机号</label>
            <input
              v-model="phone"
              type="tel"
              required
              placeholder="请输入手机号"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- 邮箱输入框 -->
        <div class="form-group">
          <div class="input-container">
            <label>邮箱</label>
            <input
              v-model="email"
              type="email"
              required
              placeholder="请输入邮箱"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- 错误信息显示 -->
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <!-- 注册按钮 -->
        <button type="submit" :disabled="loading" class="register-button">
          <span v-if="loading">注册中...</span>
          <span v-else>注册</span>
        </button>

        <!-- 返回登录链接 -->
        <div class="additional-links">
          <a href="#" @click.prevent="goToLogin" class="login-link">已有账号？返回登录</a>
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
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const photo = ref<File | null>(null) // 用于存储文件对象
    const phone = ref('')
    const email = ref('')
    const loading = ref(false)
    const error = ref('')

    const handleFileChange = (event: Event) => {
      const target = event.target as HTMLInputElement
      if (target.files && target.files[0]) {
        photo.value = target.files[0]
      } else {
        photo.value = null
      }
    }

    const handleRegister = async () => {
      if (!photo.value) {
        error.value = '请选择用户图片'
        return
      }

      loading.value = true
      error.value = ''

      // 使用 FormData 来发送包含文件的表单数据
      const formData = new FormData()
      formData.append('name', username.value)
      formData.append('password', password.value)
      formData.append('phone', phone.value)
      formData.append('email', email.value)
      formData.append('photo', photo.value) // 添加文件对象

      try {
        // 假设后端注册 API 端点是 /api/register/
        // 注意：后端需要能处理 multipart/form-data
        const response = await axios.post('/api/register/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data' // 必须设置
          },
          withCredentials: true // 如果需要 cookie 认证
        })

        if (response.data.success) {
          // 注册成功，可以提示用户并跳转到登录页
          alert('注册成功！请登录。') // 简单提示
          router.push('/login') // 跳转到登录页
        } else {
          error.value = response.data.message || '注册失败，请检查输入信息'
        }
      } catch (err: any) {
        console.error('Register error:', err)
        if (err.response && err.response.data && err.response.data.message) {
           error.value = err.response.data.message
        } else {
           error.value = '注册失败，请稍后重试'
        }
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      username,
      password,
      phone,
      email,
      loading,
      error,
      handleFileChange,
      handleRegister,
      goToLogin
    }
  }
})
</script>

<style lang="scss" scoped>
/* 复用 Login.vue 的大部分样式 */
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  width: 100vw;
  padding: 20px;
  background-image: url('@/assets/images/666.png'); /* 与登录页背景一致 */
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

.register-card {
  background: rgba(255, 255, 255, 0.7);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  width: 100%;
  max-width: 420px; /* 可以比登录略宽一点以容纳更多字段 */
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

.logo-container {
  text-align: center;
  margin-bottom: 20px;

  .logo {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 0 20px rgba(107, 115, 255, 0.2);
    border: 2px solid rgba(107, 115, 255, 0.3);
    padding: 0;
    background: white;
    transition: transform 0.3s ease;

    &:hover {
      transform: scale(1.05);
    }
  }

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

    input[type="text"],
    input[type="password"],
    input[type="tel"],
    input[type="email"] {
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

    .file-input {
      /* 简单样式，可以进一步美化 */
       display: block;
       width: 100%;
       padding: 8px 12px;
       font-size: 14px;
       color: #666;
       background-color: rgba(255, 255, 255, 0.9);
       border: 1px solid #eee;
       border-radius: 8px;
       cursor: pointer;
    }
  }
}

.register-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); /* 与登录按钮颜色一致 */
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

.additional-links {
  text-align: center; /* 居中显示返回登录链接 */
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

.copyright {
  text-align: center;
  color: #999;
  font-size: 12px;
  margin-top: 20px;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@media (max-width: 480px) {
  .register-card {
    padding: 20px;
  }
  .system-title {
    font-size: 18px;
  }
  .logo {
    width: 70px;
    height: 70px;
  }
}

</style> 