<template>
  <header class="header">
    <div class="user-menu">
      <el-dropdown trigger="click">
        <div class="user-info">
          <el-avatar :size="32" :src="userInfo.photo || '/default-avatar.png'" />
          <span class="username">{{ userInfo.name }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleChangePassword">
              <i class="el-icon-key"></i>
              修改密码
            </el-dropdown-item>
            <el-dropdown-item @click="handleChangeAvatar">
              <i class="el-icon-user"></i>
              更换头像
            </el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">
              <i class="el-icon-switch-button"></i>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userInfo = ref({
  name: '',
  photo: ''
})

// 获取用户信息
const getUserInfo = async () => {
  try {
    const response = await axios.get('http://localhost:8000/login/api/user/info/', {
      withCredentials: true
    })
    if (response.data.success) {
      userInfo.value = response.data.user
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    const response = await axios.post('http://localhost:8000/login/logout/', {}, {
      withCredentials: true,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    if (response.data.success) {
      ElMessage.success('退出登录成功')
      window.location.href = response.data.redirect_url
    }
  } catch (error) {
    console.error('退出登录失败:', error)
    ElMessage.error('退出登录失败，请重试')
  }
}

// 修改密码
const handleChangePassword = () => {
  // TODO: 实现修改密码功能
}

// 更换头像
const handleChangeAvatar = () => {
  // TODO: 实现更换头像功能
}

// 组件挂载时获取用户信息
getUserInfo()
</script>

<style scoped>
.header {
  height: 60px;
  padding: 0 20px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.user-menu {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 14px;
  color: #333;
}
</style> 