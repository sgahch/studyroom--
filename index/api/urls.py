from django.urls import path
from . import views

urlpatterns = [
    # 用户相关
    path('login/', views.login, name='api_login'),
    path('change-password/', views.change_password, name='api_change_password'),
    path('change-avatar/', views.change_avatar, name='api_change_avatar'),
    
    # 座位相关
    path('seats/', views.get_seats, name='api_get_seats'),
    path('seats/<int:seat_id>/book/', views.book_seat, name='api_book_seat'),
    path('bookings/', views.get_bookings, name='api_get_bookings'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='api_cancel_booking'),
    
    # 待办事项相关
    path('todos/', views.get_todos, name='api_get_todos'),
    path('todos/add/', views.add_todo, name='api_add_todo'),
    path('todos/<int:todo_id>/update/', views.update_todo, name='api_update_todo'),
    path('todos/<int:todo_id>/delete/', views.delete_todo, name='api_delete_todo'),
] 