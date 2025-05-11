from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
import json
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
# 移除对已删除的 tokens 模块的导入
# from .tokens import student_token_generator
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
import random
import string
from datetime import datetime, timedelta, timezone as dt_timezone

from login.models import *


# Create your views here.
@csrf_exempt
def login(request):
    print(">>> Entering login view <<<") # 添加入口打印
    path_url = '/' # Default redirect URL
    msg = None     # Initialize error message

    if request.method == 'POST':
        # 尝试从 POST 表单获取数据
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 获取之前尝试访问的路径，作为登录后重定向的目标
        path_url = request.POST.get('path_url', '/') 

        if name and password: # Ensure name and password are provided
            try:
                user = Students.objects.get(name=name)
                # 使用 check_password 检查密码
                if check_password(password, user.password):
                    # 密码正确，设置 session
                    request.session['name'] = {"name": user.name, "photo": str(user.photo)}
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['photo'] = str(user.photo)

                    # 更新 last_login 时间戳
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    print(f"Login successful for {name} via standard login form.")
                    # 重定向到最初请求的路径，如果没有则重定向到首页
                    # 如果 path_url 为空或'/', 则重定向到 '/index/' 可能更合适
                    redirect_target = path_url if path_url and path_url != '/' else '/index/'
                    return HttpResponseRedirect(redirect_target)
                else:
                    # 密码错误
                    print(f"Password incorrect for {name} via standard login form.")
                    msg = "账号或密码错误！！"
            except Students.DoesNotExist:
                # 用户不存在
                print(f"User {name} not found via standard login form.")
                msg = "账号或密码错误！！"
            except Exception as e:
                # 其他可能的错误
                print(f"Error during login for {name}: {e}")
                msg = "登录过程中发生错误，请稍后重试。"
        else:
            msg = "请输入用户名和密码。"

        # 登录失败，重新渲染登录页面并显示错误信息
        return render(request, 'login/login.html', {"msg": msg, "path_url": path_url})

    else:
        # GET 请求，显示登录页面
        # 获取 'path' 参数，如果存在的话
        path_url = request.GET.get('path', '/')
        return render(request, 'login/login.html', {"path_url": path_url})


def reginter(request):
    if request.method == 'POST':
        name = request.POST['name']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
        photo = request.FILES.get('photo')
        try:
            stu = Students.objects.filter(is_active=True, name=name)
        except Exception as e:
            print(e)
        if stu:
            msg = '用户已存在！'
            return render(request, 'login/register.html', {"msg": msg})
        else:
            try:
                stu = Students.objects.create(
                    name=name,
                    password=password,
                    phone=phone,
                    email=email,
                    photo=photo
                )
            except Exception as e:
                print(e)
            msg = "注册成功！"
            return render(request, 'login/login.html', {"msg": msg})

    return render(request, 'login/register.html')


def pswd_update(request):
    if request.method == "POST":
        name = request.session['name']
        password_1 = request.POST["password_1"]
        password_2 = request.POST["password_1"]

        try:
            stu = Students.objects.get(name=name['name'])
        except Exception as e:
            print(e)
        if stu.password == password_1:
            stu.password = password_2
            stu.save()
            return HttpResponseRedirect("/login/")
        else:
            msg = "账号或密码错误！"
            return render(request, 'login/pswd_update.html', {"msg": msg})
    else:
        return render(request, 'login/pswd_update.html')


def logout(request):
    """退出登录视图"""
    # 清除所有会话数据
    if 'name' in request.session:
        del request.session['name']
    if 'is_login' in request.session:
        del request.session['is_login']
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'photo' in request.session:
        del request.session['photo']

    # 检查是否是 AJAX 请求
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'redirect_url': 'http://localhost:8080/login'  # 修改为8080端口
        })
    else:
        # 对于普通请求，直接重定向到Vue登录页面
        return HttpResponseRedirect('http://localhost:8080/login')


def index(request):
    try:
        text = Text.objects.filter(is_active=True).order_by('time')
    except Exception as e:
        print(e)
    bookings_url = reverse('Bookings')  # 确保这里使用了正确的名称
    return render(request, 'index/index.html', {'bookings_url': bookings_url})


def admin_login(request):
    """管理员登录视图"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, is_staff=True)
            if user.check_password(password):
                request.session['admin_name'] = {"name": user.username}
                request.session['is_admin'] = True
                return HttpResponseRedirect('/admin/')
            else:
                msg = "密码错误！"
                return render(request, 'login/admin_login.html', {"msg": msg})
        except Exception as e:
            print(e)
            msg = "账号不存在或不是管理员！"
            return render(request, 'login/admin_login.html', {"msg": msg})
    return render(request, 'login/admin_login.html')


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            print("Received login request with headers:", request.headers)
            data = json.loads(request.body)
            print("Received data:", data)
            
            name = data.get('name')
            password = data.get('password') # 用户输入的明文密码
            print(f"Attempting login for user: {name}")
            
            try:
                user = Students.objects.get(name=name)
                print(f"Found user: {user.name}, checking password")
                
                login_successful = False
                password_needs_upgrade = False

                # 1. 尝试使用 check_password (适用于哈希密码)
                if check_password(password, user.password):
                    login_successful = True
                    print("Password check successful (hashed)")
                else:
                    # 2. 如果 check_password 失败，尝试明文比较 (兼容老账户)
                    #    注意：这里假设老密码不包含 Django 哈希算法前缀 (如 pbkdf2_sha256$)
                    #    如果老密码可能包含 '$'，这个判断需要更健壮
                    if '$' not in user.password and user.password == password:
                        login_successful = True
                        password_needs_upgrade = True # 标记需要升级密码
                        print("Password check successful (plaintext) - upgrading hash.")
                    else:
                        print("Password incorrect")

                # 如果登录成功 (无论是哈希还是明文)
                if login_successful:
                    # 如果是明文密码登录，立即升级为哈希
                    if password_needs_upgrade:
                        user.password = make_password(password)
                        # 在保存密码的同时更新 last_login，减少一次 save()
                        user.last_login = timezone.now()
                        user.save(update_fields=['password', 'last_login'])
                        print(f"Password for user {user.name} upgraded to hash.")
                        print(f"Updated last_login for user {user.name}")
                    else:
                        # 如果密码已经是哈希，只更新 last_login
                        user.last_login = timezone.now()
                        user.save(update_fields=['last_login'])
                        print(f"Updated last_login for user {user.name}")
                    
                    # 设置session
                    request.session['name'] = {"name": user.name, "photo": str(user.photo)}
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['photo'] = str(user.photo)
                    
                    response_data = {
                        'success': True,
                        'user': {
                            'id': user.id,
                            'username': user.name,
                            'photo': str(user.photo)
                        },
                        'redirect_url': 'http://localhost:8000/index/'  # 或者根据需要重定向到前端页面
                    }
                    print(f"Login successful, sending response: {response_data}")
                    return JsonResponse(response_data)
                else:
                    # 如果两种方式都验证失败
                    return JsonResponse({
                        'success': False,
                        'message': '用户名或密码错误' 
                    }, status=401)
                    
            except Students.DoesNotExist:
                print(f"User not found: {name}")
                return JsonResponse({
                    'success': False,
                    'message': '用户名或密码错误' 
                }, status=401)
                
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data: {e}")
            return JsonResponse({
                'success': False,
                'message': '无效的请求数据'
            }, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=500)
            
    return JsonResponse({
        'success': False,
        'message': '不支持的请求方法'
    }, status=405)


@csrf_exempt
def user_info(request):
    """获取当前登录用户信息"""
    if request.method == 'GET':
        if 'user_id' in request.session:
            try:
                user = Students.objects.get(id=request.session['user_id'])
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.name,
                        'photo': str(user.photo)
                    }
                })
            except Students.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': '用户不存在'
                }, status=404)
        return JsonResponse({
            'success': False,
            'message': '未登录'
        }, status=401)
    return JsonResponse({
        'success': False,
        'message': '不支持的请求方法'
    }, status=405)


@csrf_exempt
def api_admin_login(request):
    """管理员登录API"""
    if request.method == 'POST':
        try:
            print("Received admin login request with headers:", request.headers)
            data = json.loads(request.body)
            print("Received data:", data)
            
            username = data.get('name')
            password = data.get('password')
            print(f"Attempting admin login for user: {username}")
            
            try:
                user = User.objects.get(username=username, is_staff=True)
                if user.check_password(password):
                    print("Admin password correct, setting session")
                    request.session['admin_name'] = {"name": user.username}
                    request.session['is_admin'] = True
                    
                    response_data = {
                        'success': True,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                        },
                        'redirect_url': 'http://localhost:8000/admin/'
                    }
                    print(f"Admin login successful, sending response: {response_data}")
                    return JsonResponse(response_data)
                else:
                    print("Admin password incorrect")
                    return JsonResponse({
                        'success': False,
                        'message': '密码错误'
                    }, status=401)
            except User.DoesNotExist:
                print(f"Admin user not found: {username}")
                return JsonResponse({
                    'success': False,
                    'message': '账号不存在或不是管理员'
                }, status=401)
                
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data: {e}")
            return JsonResponse({
                'success': False,
                'message': '无效的请求数据'
            }, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=500)
            
    return JsonResponse({
        'success': False,
        'message': '不支持的请求方法'
    }, status=405)


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        # 从 POST 数据中获取字段
        name = request.POST.get('name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        photo = request.FILES.get('photo') # 从 FILES 中获取图片

        # 简单的验证
        if not all([name, password, phone, email, photo]):
            return JsonResponse({'success': False, 'message': '所有字段都是必填的'}, status=400)

        # 检查用户名是否已存在
        if Students.objects.filter(name=name).exists():
            return JsonResponse({'success': False, 'message': '用户名已存在'}, status=400)

        # 检查邮箱是否已存在
        if Students.objects.filter(email=email).exists():
             return JsonResponse({'success': False, 'message': '邮箱已被注册'}, status=400)

        try:
            # 哈希密码
            hashed_password = make_password(password)
            stu = Students.objects.create(
                name=name,
                password=hashed_password, # 存储哈希后的密码
                phone=phone,
                email=email,
                photo=photo,
                is_active=True # 默认激活
            )
            return JsonResponse({'success': True, 'message': '注册成功'})
        except Exception as e:
            print(f"Error creating student: {e}") # 记录错误日志
            return JsonResponse({'success': False, 'message': '注册过程中发生错误，请稍后重试'}, status=500)

    else:
        return JsonResponse({'success': False, 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt
def api_password_reset_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求格式'}, status=400)

        if not email:
            return JsonResponse({'success': False, 'message': '邮箱不能为空'}, status=400)

        user = Students.objects.filter(email=email, is_active=True).first()

        if user:
            # 生成 6 位数字验证码
            code = ''.join(random.choices(string.digits, k=6))
            # 设置验证码过期时间（例如 10 分钟后）
            expiry_time = datetime.now(dt_timezone.utc) + timedelta(minutes=10)

            # 将验证码和过期时间存储在 session 中 (与邮箱关联)
            request.session['reset_code'] = code
            request.session['reset_code_email'] = email
            request.session['reset_code_expiry'] = expiry_time.isoformat() # Store as string
            print(f"Stored reset code for {email}: {code}, expires: {expiry_time.isoformat()}")


            # 邮件内容
            subject = '您的密码重置验证码 - 自习室预约系统'
            message = f"""
您好 {user.name},

您正在请求重置密码。您的验证码是：

{code}

此验证码将在 10 分钟后过期。如果您没有请求重置密码，请忽略此邮件。

感谢！
自习室预约系统团队
            """
            from_email = settings.DEFAULT_FROM_EMAIL

            try:
                # 发送邮件 (当前配置为输出到控制台)
                send_mail(subject, message, from_email, [email])
                print(f"发送密码重置验证码邮件给 {email}，验证码: {code}")
                return JsonResponse({'success': True, 'message': '验证码已发送至您的邮箱，请注意查收。'})
            except Exception as e:
                print(f"Error sending reset code email: {e}")
                # 清除 session 中的无效数据
                if 'reset_code' in request.session: del request.session['reset_code']
                if 'reset_code_email' in request.session: del request.session['reset_code_email']
                if 'reset_code_expiry' in request.session: del request.session['reset_code_expiry']
                return JsonResponse({'success': False, 'message': '发送验证码邮件时出错，请稍后重试'}, status=500)
        else:
            # 即使邮箱不存在，也返回看似成功的消息，防止信息泄露
            print(f"密码重置请求，邮箱不存在或用户未激活: {email}")
            return JsonResponse({'success': True, 'message': '如果您的邮箱已注册，验证码已发送。'}) # 调整措辞

    else:
        return JsonResponse({'success': False, 'message': '仅支持 POST 请求'}, status=405)


@csrf_exempt
def api_password_reset_with_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email') # 需要前端也把 email 传过来
            code = data.get('code')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if not all([email, code, new_password, confirm_password]):
                return JsonResponse({'success': False, 'message': '缺少必要参数'}, status=400)

            if new_password != confirm_password:
                return JsonResponse({'success': False, 'message': '两次输入的密码不一致'}, status=400)

            # --- 验证 Session 中的验证码 ---
            stored_code = request.session.get('reset_code')
            stored_email = request.session.get('reset_code_email')
            stored_expiry_str = request.session.get('reset_code_expiry')

            print(f"Verifying code: Input Email={email}, Stored Email={stored_email}, Input Code={code}, Stored Code={stored_code}, Expiry={stored_expiry_str}")

            if not stored_code or not stored_email or not stored_expiry_str:
                return JsonResponse({'success': False, 'message': '验证码会话不存在，请重新请求'}, status=400)

            if email != stored_email:
                 return JsonResponse({'success': False, 'message': '邮箱与请求验证码时的邮箱不符'}, status=400)

            if code != stored_code:
                 return JsonResponse({'success': False, 'message': '验证码错误'}, status=400)

            # 检查验证码是否过期
            try:
                expiry_time = datetime.fromisoformat(stored_expiry_str)
                if datetime.now(dt_timezone.utc) > expiry_time:
                    # 清除过期的 session 数据
                    del request.session['reset_code']
                    del request.session['reset_code_email']
                    del request.session['reset_code_expiry']
                    return JsonResponse({'success': False, 'message': '验证码已过期，请重新请求'}, status=400)
            except ValueError:
                 # 清除格式错误的 session 数据
                 if 'reset_code_expiry' in request.session: del request.session['reset_code_expiry']
                 return JsonResponse({'success': False, 'message': '验证码有效期格式错误'}, status=500)


            # --- 验证通过，查找用户并重置密码 ---
            try:
                user = Students.objects.get(email=email, is_active=True) # 再次确认用户
            except Students.DoesNotExist:
                 return JsonResponse({'success': False, 'message': '用户不存在或未激活'}, status=404)

            try:
                user.password = make_password(new_password)
                user.save(update_fields=['password'])
                print(f"Password reset successful for user {user.name} via code.")

                # 密码重置成功后，清除 session 中的验证码信息
                del request.session['reset_code']
                del request.session['reset_code_email']
                del request.session['reset_code_expiry']

                return JsonResponse({'success': True, 'message': '密码重置成功！请使用新密码登录。'})
            except Exception as e:
                print(f"Error saving new password after code verification: {e}")
                return JsonResponse({'success': False, 'message': '保存新密码时出错'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求格式'}, status=400)
        except Exception as e:
            print(f"Unexpected error in password reset with code: {e}")
            return JsonResponse({'success': False, 'message': '处理密码重置时发生错误'}, status=500)

    else:
        return JsonResponse({'success': False, 'message': '仅支持 POST 请求'}, status=405)
