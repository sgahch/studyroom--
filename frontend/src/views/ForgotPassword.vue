<template>
  <!-- 忘记密码页面容器 -->
  <div class="forgot-password-container">
    <!-- 卡片 -->
    <div class="forgot-password-card">
      <!-- Logo和标题容器 -->
      <div class="logo-container">
        <img src="/img/logo1.png" alt="Logo" class="logo">
        <h1 class="system-title">{{ step === 1 ? '忘记密码' : '重置密码' }}</h1>
      </div>

      <!-- 表单 -->
      <form @submit.prevent="handleSubmit" class="forgot-password-form">
        <!-- 步骤 1: 输入邮箱 -->
        <div v-if="step === 1">
          <p class="instructions">请输入您的注册邮箱，我们将向该邮箱发送验证码。</p>
          <div class="form-group">
            <div class="input-container">
              <label>邮箱</label>
              <input
                v-model="email"
                type="email"
                required
                placeholder="请输入注册邮箱"
                :disabled="loading"
              />
            </div>
          </div>
        </div>

        <!-- 步骤 2: 输入验证码和新密码 -->
        <div v-if="step === 2">
          <p class="instructions">验证码已发送至 {{ email }}，请输入验证码和新密码。</p>
          <div class="form-group">
            <div class="input-container">
              <label>验证码</label>
              <input
                v-model="verificationCode"
                type="text"
                required
                placeholder="请输入 6 位验证码"
                :disabled="loading"
                maxlength="6"
                autocomplete="off"
              />
            </div>
          </div>
          <div class="form-group">
            <div class="input-container">
              <label>新密码</label>
              <input
                v-model="newPassword"
                type="password"
                required
                placeholder="请输入新密码"
                :disabled="loading"
                autocomplete="new-password"
              />
            </div>
          </div>
          <div class="form-group">
            <div class="input-container">
              <label>确认新密码</label>
              <input
                v-model="confirmPassword"
                type="password"
                required
                placeholder="请再次输入新密码"
                :disabled="loading"
                autocomplete="new-password"
              />
            </div>
          </div>
        </div>

        <!-- 通用信息显示 -->
        <div v-if="successMessage" class="success-message">
          <i class="fas fa-check-circle"></i>
          {{ successMessage }}
        </div>
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ error }}
        </div>

        <!-- 根据步骤显示不同按钮 -->
        <button type="submit" :disabled="loading || isResetComplete" class="submit-button">
          <span v-if="loading">{{ step === 1 ? '发送中...' : '设置中...' }}</span>
          <span v-else>{{ step === 1 ? '发送验证码' : '确认重置密码' }}</span>
        </button>

        <!-- 返回登录链接 -->
        <div class="additional-links">
          <a href="#" @click.prevent="goToLogin" class="login-link">返回登录</a>
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
  name: 'ForgotPasswordView',
  setup() {
    const router = useRouter()
    const step = ref(1) // 1: 输入邮箱, 2: 输入验证码和新密码
    const email = ref('')
    const verificationCode = ref('')
    const newPassword = ref('')
    const confirmPassword = ref('')
    const loading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const isResetComplete = ref(false) // 新增状态：标记重置是否完成

    // 请求发送验证码
    const requestCode = async () => {
      loading.value = true
      error.value = ''
      successMessage.value = ''

      try {
        const response = await axios.post('/api/password/reset/request/', {
          email: email.value
        }, { withCredentials: true })

        if (response.data.success) {
          successMessage.value = response.data.message || '验证码已发送至您的邮箱，请注意查收。'
          step.value = 2 // 进入下一步
        } else {
          error.value = response.data.message || '请求失败，请稍后重试'
        }
      } catch (err: any) {
        console.error('Request code error:', err)
        if (err.response && err.response.data && err.response.data.message) {
           error.value = err.response.data.message
        } else {
           error.value = '请求失败，请检查邮箱地址或稍后重试'
        }
      } finally {
        loading.value = false
      }
    }

    // 使用验证码重置密码
    const resetPasswordWithCode = async () => {
      if (newPassword.value !== confirmPassword.value) {
        error.value = '两次输入的密码不一致'
        return
      }
      if (!verificationCode.value || verificationCode.value.length !== 6) {
          error.value = '请输入 6 位验证码'
          return
      }

      loading.value = true
      error.value = ''
      successMessage.value = '' // 清除之前的成功消息

      try {
        const response = await axios.post('/api/password/reset/with_code/', {
          email: email.value, // 需要提交 email
          code: verificationCode.value,
          new_password: newPassword.value,
          confirm_password: confirmPassword.value
        })

        if (response.data.success) {
          successMessage.value = response.data.message || '密码重置成功！请使用新密码登录。'
          isResetComplete.value = true // 设置重置完成状态
          // 清空输入框，停留在成功页面
          verificationCode.value = ''
          newPassword.value = ''
          confirmPassword.value = ''
        } else {
          error.value = response.data.message || '密码重置失败'
          // 密码重置失败时不清空验证码和密码，方便用户修改
        }
      } catch (err: any) {
        console.error('Reset password with code error:', err)
        if (err.response && err.response.data && err.response.data.message) {
           error.value = err.response.data.message
        } else {
           error.value = '密码重置失败，验证码可能已失效或发生错误。'
        }
      } finally {
        loading.value = false
      }
    }

    // 根据当前步骤决定提交哪个方法
    const handleSubmit = () => {
      if (step.value === 1) {
        successMessage.value = '' // 清除可能残留的消息
        requestCode()
      } else {
        successMessage.value = '' // 清除可能残留的消息
        resetPasswordWithCode()
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    return {
      step,
      email,
      verificationCode,
      newPassword,
      confirmPassword,
      loading,
      error,
      successMessage,
      isResetComplete,
      handleSubmit,
      goToLogin
    }
  }
})
</script>

<style lang="scss" scoped>
/* 复用 Login.vue / Register.vue 的样式 */
.forgot-password-container {
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

.forgot-password-card {
  background: rgba(255, 255, 255, 0.7);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  width: 100%;
  max-width: 400px; /* 调整宽度 */
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

.instructions {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
  text-align: center;
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

    input[type="email"],
    input[type="text"],
    input[type="password"] {
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

.submit-button {
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
  margin-top: 8px; /* 加一点上边距 */

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
  text-align: center;
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

.success-message,
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 13px;
  border: 1px solid;
  margin-bottom: 16px;
}

.success-message {
  background: #f0fff4;
  color: #2f855a;
  border-color: #9ae6b4;
}

.error-message {
  background: #fff5f5;
  color: #e53e3e;
  border-color: #fed7d7;
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
  .forgot-password-card {
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