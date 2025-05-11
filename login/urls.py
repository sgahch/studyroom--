from django.urls import path, include

from login import views

urlpatterns = [
    path('', views.index, name="index"),  #
    path('login/', views.login, name="login"),  #
    path('register/', views.reginter, name="register"),  #
    path('pswd_update/', views.pswd_update, name="pswd_update"),  #
    path('logout/', views.logout, name="logout"),  #
    path('api/login/', views.api_login, name='api_login'),  # 添加 API 登录路由
    path('api/admin/login/', views.api_admin_login, name='api_admin_login'),  # 添加管理员 API 登录路由
    path('api/user/info/', views.user_info, name='user_info'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/password/reset/request/', views.api_password_reset_request, name='api_password_reset_request'),
    path('api/password/reset/with_code/', views.api_password_reset_with_code, name='api_password_reset_with_code'),
]
