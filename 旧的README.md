# 📚 自习室预约系统

> 告别排队占座的烦恼，享受轻松便捷的学习时光！

## 项目总结 (当前状态)

本项目是一个自习室预约管理系统，目前正从传统的 Django 服务端渲染架构**过渡到前后端分离**的模式。

**当前实现的关键功能 (前后端分离部分):**

*   **用户认证**: 
    *   基于 Vue 的用户登录界面，通过 `/api/login/` 与后端交互。
    *   实现了密码哈希存储，并兼容旧有明文密码账户的首次登录及密码自动升级。
    *   基于 Vue 的用户注册界面，通过 `/api/register/` 实现新用户注册，密码自动哈希。
    *   用户登出功能。
*   **密码管理**: 
    *   实现了基于**邮箱验证码**的"忘记密码"流程。
    *   前端包含请求验证码和输入验证码/新密码的两阶段界面 (`ForgotPassword.vue`)。
    *   后端提供 API (`/api/password/reset/request/`, `/api/password/reset/with_code/`) 处理验证码生成、(模拟)发送和验证、密码重置。
*   **用户信息**: 提供 `/api/user/info/` API 获取当前登录用户信息。
*   **邮件发送**: 配置为开发模式，邮件(如密码重置验证码)将输出到 Django 服务器控制台，便于测试。(`README` 中包含切换到 SMTP 的说明)。
*   **跨域**: 已配置 CORS (`django-cors-headers`) 允许前端 (`localhost:8080` 或类似端口) 访问后端 API (`localhost:8000`)。

**原有 Django 功能**: 系统还包含原有的基于 Django 模板的自习室浏览、座位查看、预约、签到、后台管理等功能，这些功能与新的 Vue 前端尚未完全集成。

**技术栈 (当前混合状态):**

*   **后端**: Django, MySQL, Django REST framework (用于部分 API), `django-cors-headers`
*   **前端**: Vue 3, Vue Router, Axios

## ✨ 产品亮点

- 🚀 **一键预约**：随时随地，轻松预定心仪座位
- 🎯 **智能推荐**：基于个人偏好，推荐最适合的学习位置
- 🎵 **专注音乐**：精选学习音乐，打造专属学习氛围
- 📊 **数据可视**：直观展示学习数据，激励持续进步

## 🛠️ 快速开始

### 环境准备
- 💻 Windows 10 操作系统
- 🐍 Python 3.6+ 
- 📦 MySQL 5.7+
- 🔧 PyCharm（推荐）

### 测试账号
| 角色 | 账号 | 密码 |
|------|------|------|
| 普通用户 | user01/user02/user03 | 123 |
| 管理员 | admin | 123 |

## 🌟 核心功能

### 1. 👤 用户中心
- 便捷登录：手机号一键注册，即刻开启学习之旅
- 个性定制：自定义头像、昵称，打造专属学习档案
- 安全保障：多重加密，确保账号安全

### 2. 🏫 智能预约
- 实时动态：座位状态实时更新，避免空跑
- 智能匹配：基于学习偏好推荐最佳座位
- 便捷签到：扫码签到，轻松打卡
- 记录追踪：预约历史一目了然

### 3. 📝 学习助手
- ✅ 任务清单：智能规划每日学习计划
- 📈 数据统计：直观展示学习时长与进度
- ⏰ 贴心提醒：及时通知预约与签到
- 🎯 目标设定：制定并追踪学习目标

### 4. 🎵 专注空间
- 🎼 场景音乐：多种学习氛围音乐
- 💫 智能推荐：个性化音乐推送
- ❤️ 收藏夹：保存喜爱的学习音乐

## 🔧 部署指南

### 1. 基础环境配置
```bash
# 检查环境
python --version  # 确保 Python 3.6+
pip --version

# 安装 Django
pip install django

# 克隆项目
git clone [项目地址]
cd studyroom
```

### 2. 虚拟环境配置
```bash
# 创建虚拟环境
python -m venv venv

# 激活环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库配置
1. 安装并启动 MySQL
2. 创建数据库并导入 `studyroom.sql`
3. 修改配置文件：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '你的数据库名',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 启动服务
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 📁 项目结构
```
studyroom/
├── 📂 index/      # 核心业务逻辑
├── 📂 login/      # 用户认证模块
├── 📂 static/     # 静态资源文件
├── 📂 media/      # 用户上传文件
├── 📂 studyroom/  # 项目配置
└── 📄 manage.py   # 管理脚本
```
studyroom/                      # 项目根目录
├── manage.py                   # Django项目管理脚本
├── README.md                   # 项目说明文档
├── add_music.py                # 添加背景音乐的脚本
├── venv/                       # Python虚拟环境
├── .idea/                      # IDE配置文件
├── .git/                       # Git版本控制
├── Mysql配置文件/               # MySQL数据库配置
├── static/                     # 静态文件目录
│   ├── bootstrap/              # Bootstrap框架文件
│   ├── css/                    # CSS样式文件
│   ├── img/                    # 图片资源
│   ├── js/                     # JavaScript脚本
│   └── music/                  # 背景音乐文件
├── media/                      # 用户上传的媒体文件
│   ├── Students/               # 学生相关文件
│   └── Room/                   # 自习室相关文件
├── studyroom/                  # 项目主配置目录
│   ├── __init__.py             # 初始化文件
│   ├── settings.py             # 项目设置文件
│   ├── urls.py                 # 主URL路由配置
│   ├── asgi.py                 # ASGI配置
│   └── wsgi.py                 # WSGI配置
├── login/                      # 登录应用
│   ├── __init__.py             # 初始化文件
│   ├── admin.py                # 后台管理配置
│   ├── apps.py                 # 应用配置
│   ├── models.py               # 数据模型定义
│   ├── SimpleMiddleware.py     # 中间件
│   ├── urls.py                 # URL路由配置
│   ├── views.py                # 视图函数
│   ├── migrations/             # 数据库迁移文件
│   └── templates/              # 模板文件
│       └── login/              # 登录相关模板
│           ├── login.html      # 登录页面
│           ├── register.html   # 注册页面
│           └── pswd_update.html # 密码更新页面
└── index/                      # 主页应用
    ├── __init__.py             # 初始化文件
    ├── admin.py                # 后台管理配置
    ├── apps.py                 # 应用配置
    ├── models.py               # 数据模型定义
    ├── urls.py                 # URL路由配置
    ├── utils.py                # 工具函数
    ├── views.py                # 视图函数
    ├── migrations/             # 数据库迁移文件
    └── templates/              # 模板文件
        └── index/              # 主页相关模板
            ├── base.html       # 基础模板
            ├── index.html      # 主页
            ├── modals.html     # 模态框
            ├── Bookings.html   # 预约页面
            ├── seat.html       # 座位页面
            ├── seat_id.html    # 座位详情页面
            ├── Recording.html  # 记录页面
            ├── sign_code.html  # 签到码页面
            ├── sign_url.html   # 签到URL页面
            ├── warn.html       # 警告页面
            ├── change_avatar.html # 修改头像页面
            └── change_password.html # 修改密码页面

## 📢 使用规范

1. ⏰ 请按时到达并完成签到
2. 🚫 预约时间结束后及时离开
3. 🧹 保持环境整洁
4. 🤫 保持安静，营造良好学习氛围

## 📞 联系我们

遇到问题？有建议想法？
- 📧 邮箱：hq1911779729@qq.com
- 💬 工作时间：周一至周五 9:00-18:00

## 📄 开源协议

本项目遵循 MIT 许可证开源。 

# 自习室预约系统改进计划

## 项目概述

这是一个基于Django的自习室预约管理系统，提供自习室预约、座位管理、签到等功能。本文档记录了系统的改进计划。

## 当前系统架构

- 后端框架：Django 4.0.3
- 数据库：MySQL
- 前端技术：Bootstrap + 原生JavaScript
- 认证方式：Session认证
- 模板引擎：Django Template

## 改进方向

### 1. 前后端分离架构改造

#### 1.1 后端 API 改造
- **引入 Django REST Framework**
  - 将现有视图改造为 RESTful API
  - 实现统一的 API 响应格式
  - 添加 API 版本控制

- **认证系统升级**
  - 实现 JWT 认证
  - 添加 OAuth2.0 支持
  - 完善权限控制系统

- **API 文档自动化**
  - 集成 Swagger/OpenAPI
  - 添加详细的 API 文档
  - 实现接口测试功能

#### 1.2 前端架构重构
- **Vue.js 框架引入**
  - 创建基于 Vue3 的前端项目
  - 使用 Composition API
  - 实现组件化架构

- **状态管理优化**
  - 引入 Pinia 状态管理
  - 实现数据持久化
  - 优化数据流转

- **路由系统重构**
  - 实现动态路由
  - 添加路由守卫
  - 优化导航体验

### 2. UI 现代化改造

#### 2.1 设计系统建立
- 引入 TailwindCSS
- 建立设计令牌系统
- 实现主题切换功能

#### 2.2 组件库升级
- 使用 Element Plus
- 自定义组件开发
- 实现响应式设计

#### 2.3 交互体验优化
- 添加页面过渡动画
- 实现骨架屏加载
- 优化表单交互

### 3. 性能优化方案

#### 3.1 缓存系统实现
- 引入 Redis 缓存
- 实现多级缓存策略
- 优化热点数据访问

#### 3.2 数据库优化
- 添加数据库索引
- 优化查询语句
- 实现数据分页

#### 3.3 前端性能优化
- 实现路由懒加载
- 优化资源加载
- 实现图片懒加载

#### 3.4 API 性能优化
- 实现请求合并
- 添加数据压缩
- 优化响应格式

### 4. 新功能扩展

#### 4.1 实时通知系统
- 集成 WebSocket
- 实现消息推送
- 添加系统通知

#### 4.2 数据分析功能
- 实现使用统计
- 添加数据可视化
- 生成分析报告

#### 4.3 预约系统增强
- 实现智能推荐
- 添加批量操作
- 优化预约流程

### 5. 开发流程优化

#### 5.1 自动化部署
- 配置 Docker 环境
- 实现 CI/CD 流程
- 自动化测试集成

#### 5.2 代码质量控制
- 添加代码规范
- 实现自动化测试
- 集成代码审查

#### 5.3 监控系统建设
- 实现日志收集
- 添加性能监控
- 错误追踪系统

## 实施计划

### 第一阶段：后端 API 改造

1. 环境准备
   - 安装 Django REST Framework
   - 配置 JWT 认证
   - 设置 CORS 支持

2. 数据模型优化
   - 重构现有模型
   - 添加序列化器
   - 优化模型关系

3. API 端点实现
   - 用户认证 API
   - 自习室管理 API
   - 预约系统 API
   - 签到系统 API
   - 待办事项 API
   - 背景音乐 API

4. 认证系统升级
   - 实现 JWT 认证
   - 添加权限控制
   - 实现刷新令牌

5. API 文档
   - 集成 Swagger
   - 编写 API 文档
   - 添加接口测试

## 技术栈升级

### 后端
- Django 4.0.3 -> Django 4.2+
- Django REST Framework
- JWT 认证
- Redis 缓存
- WebSocket (Channels)
- Celery 任务队列

### 前端
- Vue 3
- Element Plus
- TailwindCSS
- Pinia
- Vue Router
- Axios
- ECharts

### 开发工具
- Docker
- GitLab CI/CD
- Jest
- ESLint
- Prettier

## 预期成果

1. 提升系统性能和可扩展性
2. 改善用户体验
3. 增强系统功能
4. 提高代码质量
5. 优化开发流程

## 时间节点

1. 第一阶段（后端API改造）：2-3周
2. 第二阶段（前端重构）：3-4周
3. 第三阶段（性能优化）：2周
4. 第四阶段（新功能开发）：2-3周
5. 第五阶段（开发流程优化）：1-2周

总计预期时间：10-14周

## 风险评估

1. 数据迁移风险
2. 系统兼容性问题
3. 性能调优挑战
4. 开发周期延长
5. 用户适应新系统

## 应对策略

1. 完善的测试覆盖
2. 灰度发布策略
3. 用户培训计划
4. 回滚机制准备
5. 持续监控和反馈

## 维护计划

1. 定期代码审查
2. 性能监控和优化
3. 安全漏洞修复
4. 功能迭代更新
5. 用户反馈收集

## 贡献指南

1. 代码规范
2. 提交规范
3. 测试要求
4. 文档要求
5. 审查流程

# 自习室预约系统账号信息

## 管理员账号
1. 用户名：haige
   - 邮箱：169330@qq.com

2. 用户名：admin
   - 邮箱：23456@qq.com

3. 用户名：root
   - 邮箱：3209932364@qq.com

## 学生账号
1. 用户名：user01
   - 密码：123
   - 电话：19914378079
   - 邮箱：1693305172@qq.com

2. 用户名：user02
   - 密码：123
   - 电话：19914378079
   - 邮箱：1693305172@qq.com

3. 用户名：user03
   - 密码：123
   - 电话：19914378079
   - 邮箱：1693305172@qq.com

4. 用户名：李玉
   - 密码：admin
   - 电话：13154269458
   - 邮箱：3209932364@qq.com

5. 用户名：Ynchen
   - 密码：123456
   - 电话：1911779729
   - 邮箱：1911779729@qq.com

## 使用说明
1. 学生用户可以直接使用账号密码登录系统
2. 管理员账号需要通过后台管理界面登录
3. 建议使用学生账号进行测试，因为密码是明文存储的 

## 前后端分离改造进度

### 1. 已完成的工作

#### 1.1 前端架构搭建
- ✅ 创建基于 Vue3 的前端项目
- ✅ 引入 Element Plus UI 组件库
- ✅ 实现基础的路由配置
- ✅ 创建登录页面组件
- ✅ 实现用户登录界面
- ✅ 创建头部导航组件

#### 1.2 后端 API 改造
- ✅ 实现用户登录 API (`/login/api/login/`)
- ✅ 实现管理员登录 API (`/login/api/admin/login/`)
- ✅ 实现获取用户信息 API (`/login/api/user/info/`)
- ✅ 改造退出登录功能，支持前端重定向
- ✅ 添加跨域支持（CORS）
- ✅ 实现基于 Session 的认证

#### 1.3 数据交互
- ✅ 实现前后端的登录数据交互
- ✅ 实现用户会话管理
- ✅ 实现登录状态保持
- ✅ 实现退出登录功能

### 2. 进行中的工作

#### 2.1 前端开发
- ⏳ 完善路由守卫
- ⏳ 实现状态管理（Pinia）
- ⏳ 封装 axios 请求
- ⏳ 实现全局错误处理
- ⏳ 添加加载状态和过渡动画

#### 2.2 后端开发
- ⏳ 完善 RESTful API 设计
- ⏳ 实现统一的响应格式
- ⏳ 添加请求参数验证
- ⏳ 完善错误处理机制
- ⏳ 实现日志记录

### 3. 待开发功能

#### 3.1 用户功能模块
- 📝 个人信息修改
- 📝 头像上传
- 📝 密码修改
- 📝 自习室预约
- 📝 预约记录查询

#### 3.2 系统功能
- 📝 权限控制
- 📝 数据缓存
- 📝 实时通知
- 📝 系统监控

### 4. 技术栈更新

#### 4.1 前端技术栈
- Vue 3
- Vue Router
- Element Plus
- Axios
- Pinia (计划中)

#### 4.2 后端技术栈
- Django
- Django REST Framework
- MySQL
- Redis (计划中)

### 5. 下一步计划

1. 完善前端工程化配置
   - 配置开发环境
   - 添加代码规范
   - 设置构建脚本

2. 继续 API 改造
   - 设计剩余功能的 API
   - 添加 API 文档
   - 实现数据验证

3. 优化用户体验
   - 添加加载状态
   - 优化表单验证
   - 完善错误提示

4. 提升系统安全性
   - 完善认证机制
   - 添加请求限制
   - 实现数据加密

### 6. 已知问题

1. 前端开发环境配置未完成
   - 需要配置正确的开发脚本
   - 需要设置正确的构建命令

2. 路由配置待完善
   - 需要添加路由守卫
   - 需要处理未授权访问

3. 状态管理待实现
   - 需要引入 Pinia
   - 需要设计状态结构

4. API 安全性待加强
   - 需要添加请求频率限制
   - 需要完善错误处理

### 7. 后续优化方向

1. 性能优化
   - 添加数据缓存
   - 优化请求处理
   - 实现懒加载

2. 用户体验
   - 添加骨架屏
   - 优化加载状态
   - 完善错误提示

3. 代码质量
   - 添加自动化测试
   - 规范代码风格
   - 完善项目文档

4. 部署优化
   - 配置自动化部署
   - 添加监控系统
   - 优化服务器配置

## 配置

### 邮件发送 (用于密码重置)

*   **当前配置**: 使用 Django 的 `console.EmailBackend`。密码重置邮件的内容将直接打印到运行 Django 服务器的终端，并不会实际发送。这对于开发和测试很方便。
*   **后续配置 (实际发送邮件)**:
    1.  **选择邮件服务商**: 如 QQ 邮箱、163 邮箱、Gmail 或 SendGrid 等。
    2.  **开启 SMTP 服务并获取授权码/API Key**: 登录你的邮箱服务商，根据其文档开启 SMTP 并获取凭证。
    3.  **修改 `studyroom/settings.py`**: 
        *   注释掉 `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`。
        *   取消 SMTP 相关配置的注释，并填入你的实际信息：
            ```python
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.example.com' # 替换为你的 SMTP 服务器地址
            # EMAIL_PORT = 587 # 或 465
            # EMAIL_USE_TLS = True # 或 False, 根据端口
            # EMAIL_USE_SSL = False # 或 True, 根据端口
            # EMAIL_HOST_USER = 'your_email@example.com' # 替换为你的邮箱地址
            # EMAIL_HOST_PASSWORD = 'your_authorization_code_or_app_password' # 替换为你的授权码
            # DEFAULT_FROM_EMAIL = EMAIL_HOST_USER 
            ```
    4.  **修改 `login/views.py`**: 
        *   在 `api_password_reset_request` 函数中，找到被注释掉的 `send_mail(...)` 行。
        *   取消该行的注释。
    5.  **重启 Django 服务器**。

## 注意事项

*   确保前后端开发服务器都在运行。
*   CORS 配置已允许 `http://localhost:8080` 访问后端 API。 