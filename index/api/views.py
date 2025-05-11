from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from login.models import Students
from ..models import TodoItem, BackgroundMusic
import json

def api_response(data=None, message="", status=200):
    """统一的API响应格式"""
    return JsonResponse({
        "status": status,
        "message": message,
        "data": data
    })

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """用户登录API"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = Students.objects.filter(name=username, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return api_response({
                "user": {
                    "id": user.id,
                    "username": user.name,
                    "avatar": user.photo.url if user.photo else None
                }
            }, "登录成功")
        return api_response(message="用户名或密码错误", status=400)
    except Exception as e:
        return api_response(message=str(e), status=500)

@require_http_methods(["GET"])
def get_seats(request):
    """获取座位列表API"""
    try:
        seats = Seat.objects.all()
        seats_data = [{
            "id": seat.id,
            "name": seat.name,
            "status": seat.status,
            "is_available": seat.is_available()
        } for seat in seats]
        return api_response(seats_data)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["POST"])
def book_seat(request, seat_id):
    """预订座位API"""
    try:
        seat = Seat.objects.get(id=seat_id)
        if not seat.is_available():
            return api_response(message="座位已被预订", status=400)
            
        user_id = request.session.get('user_id')
        booking = Booking.objects.create(
            user_id=user_id,
            seat=seat,
            status='active'
        )
        seat.status = 'booked'
        seat.save()
        
        return api_response({
            "booking_id": booking.id,
            "seat_id": seat.id
        }, "预订成功")
    except Seat.DoesNotExist:
        return api_response(message="座位不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["GET"])
def get_bookings(request):
    """获取用户的预订记录API"""
    try:
        user_id = request.session.get('user_id')
        bookings = Booking.objects.filter(user_id=user_id).select_related('seat')
        bookings_data = [{
            "id": booking.id,
            "seat_name": booking.seat.name,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for booking in bookings]
        return api_response(bookings_data)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["POST"])
def cancel_booking(request, booking_id):
    """取消预订API"""
    try:
        user_id = request.session.get('user_id')
        booking = Booking.objects.get(id=booking_id, user_id=user_id)
        if booking.status != 'active':
            return api_response(message="该预订已取消或已完成", status=400)
            
        booking.status = 'cancelled'
        booking.save()
        
        seat = booking.seat
        seat.status = 'available'
        seat.save()
        
        return api_response(message="取消预订成功")
    except Booking.DoesNotExist:
        return api_response(message="预订记录不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500)

@require_http_methods(["GET"])
def get_todos(request):
    """获取待办事项列表API"""
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return api_response(message="请先登录", status=401)
            
        todos = TodoItem.objects.filter(user_id=user_id)
        todos_data = [{
            "id": todo.id,
            "content": todo.content,
            "completed": todo.completed,
            "created_at": todo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for todo in todos]
        return api_response(todos_data)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["POST"])
def add_todo(request):
    """添加待办事项API"""
    try:
        data = json.loads(request.body)
        content = data.get('content')
        if not content:
            return api_response(message="内容不能为空", status=400)
            
        user_id = request.session.get('user_id')
        todo = TodoItem.objects.create(
            user_id=user_id,
            content=content
        )
        
        return api_response({
            "id": todo.id,
            "content": todo.content,
            "completed": todo.completed,
            "created_at": todo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }, "添加成功")
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["PUT"])
def update_todo(request, todo_id):
    """更新待办事项API"""
    try:
        data = json.loads(request.body)
        content = data.get('content')
        completed = data.get('completed')
        
        user_id = request.session.get('user_id')
        todo = TodoItem.objects.get(id=todo_id, user_id=user_id)
        
        if content is not None:
            todo.content = content
        if completed is not None:
            todo.completed = completed
            
        todo.save()
        
        return api_response({
            "id": todo.id,
            "content": todo.content,
            "completed": todo.completed,
            "created_at": todo.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }, "更新成功")
    except TodoItem.DoesNotExist:
        return api_response(message="待办事项不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_todo(request, todo_id):
    """删除待办事项API"""
    try:
        user_id = request.session.get('user_id')
        todo = TodoItem.objects.get(id=todo_id, user_id=user_id)
        todo.delete()
        return api_response(message="删除成功")
    except TodoItem.DoesNotExist:
        return api_response(message="待办事项不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["POST"])
def change_password(request):
    """修改密码API"""
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return api_response(message="密码不能为空", status=400)
            
        user_id = request.session.get('user_id')
        user = Students.objects.get(id=user_id)
        
        if user.password != old_password:
            return api_response(message="原密码错误", status=400)
            
        user.password = new_password
        user.save()
        
        return api_response(message="密码修改成功")
    except Students.DoesNotExist:
        return api_response(message="用户不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500)

@login_required
@require_http_methods(["POST"])
def change_avatar(request):
    """修改头像API"""
    try:
        if 'avatar' not in request.FILES:
            return api_response(message="请选择头像文件", status=400)
            
        avatar_file = request.FILES['avatar']
        user_id = request.session.get('user_id')
        user = Students.objects.get(id=user_id)
        
        user.photo = avatar_file
        user.save()
        
        return api_response({
            "avatar_url": user.photo.url
        }, "头像修改成功")
    except Students.DoesNotExist:
        return api_response(message="用户不存在", status=404)
    except Exception as e:
        return api_response(message=str(e), status=500) 