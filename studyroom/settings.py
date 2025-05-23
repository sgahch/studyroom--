"""
Django settings for 图书馆座位预定管理系统 project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dsvds%4jzg1w9^k4k20+yd3zd5c07h(&6%ms+e1-8-ul^t!7ly'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'index',
    'login',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'studyroom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'studyroom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'studyroom',  # 数据库名称
        'USER': 'root',        # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': '127.0.0.1',  # 数据库主机地址
        'PORT': 3306,         # 数据库端口
        'ATOMIC_REQUEST': True,
        'OPTIONS': {
            "init_command": "SET default_storage_engine=INNODB",
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 允许上传的音频文件类型
ALLOWED_AUDIO_TYPES = [
    'audio/mpeg',  # MP3
    'audio/wav',   # WAV
    'audio/ogg',   # OGG
]

# 最大上传文件大小 (5MB)
MAX_UPLOAD_SIZE = 5 * 1024 * 1024

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLEUI_LOGO = '/static/img/logo.svg'

# simpleui 排序后台app导航栏
SIMPLEUI_DEFAULT_THEME = 'e-green.css'
SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['签到码', '自习室管理', '预约管理', '警告记录', '提示管理', '用户管理'],
    'dynamic': True,
    'menus': [{
        'name': '签到码',
        'models': [{
            'name': '签到码',
            'url': '/index/sign_code/'
        }
        ]
    }, {
        'name': '自习室管理',
        'models': [{
            'name': '自习室列表',
            'url': '/admin/login/rooms/'
        }
        ]
    }, {
        'name': '预约管理',
        'models': [{
            'name': '预约列表',
            'url': '/admin/login/bookings/'
        }]
    }, {
        'name': '提示管理',
        'models': [{
            'name': '提示列表',
            'url': '/admin/login/text/'
        }]
    }, {
        'name': '警告记录',
        'models': [{
            'name': '警告列表',
            'url': '/admin/login/integrals/'
        }]
    },
        {
            'name': '用户管理',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': '学生列表',
                    'url': '/admin/login/students/'
                },
                {
                    'name': '管理员列表',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                }]
        }]
}
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

# Email Configuration (Using QQ SMTP)
# --- Restore SMTP backend ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '1911779729@qq.com' # 更新为用户指定的 QQ 邮箱
EMAIL_HOST_PASSWORD = 'lbeemtllvcczedfi' # 假设这个授权码是属于 1911779729@qq.com 的
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER # 同步更新默认发件人

# --- Disable Console Backend ---
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'noreply@studyroom.local' # Console backend needs a default from address

# --- 注释掉 Console Backend ---
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'noreply@studyroom.local'

# --- Placeholder for other SMTP Configuration (See README.md) ---
# ... (保持不变)

# CORS设置
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vue开发服务器地址
    "http://localhost:8080",  # 添加前端开发服务器地址
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF设置
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",  # Vue开发服务器地址
]
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = True

# 开发环境可暂时允许所有跨域请求
CORS_ALLOW_ALL_ORIGINS = True

# Redirect to this URL after logout (both default admin and potentially custom views)
LOGOUT_REDIRECT_URL = 'http://localhost:8080/login'