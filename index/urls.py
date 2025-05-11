from django.urls import path
from . import views
from .views import MusicListView, MusicDetailView

urlpatterns = [
    path('', views.index, name="index"),  # 首页
    path('bookings/', views.bookings, name="bookings"),  # 选择预约自习室
    path('seat/<int:id>', views.seat, name="seat"),  # 预约座位
    path('recording/', views.recording, name="recording"),  # 预约记录
    path('warn/', views.warn, name="warn"),  # 警告记录
    path('sign/', views.sign_url, name="sign_url"),  # 签到页面
    path('sign_code/', views.sign_code, name="sign_code"), # 添加签到码页面
    path('logout/', views.logout, name="logout"),  # 退出登录
    path('todos/', views.get_todos, name='get_todos'),
    path('todos/add/', views.add_todo, name='add_todo'),
    path('todos/<int:todo_id>/update/', views.update_todo, name='update_todo'),
    path('todos/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('api/music/', MusicListView.as_view(), name='music_list'),
    path('api/music/<int:music_id>/', MusicDetailView.as_view(), name='music_detail'),
]
