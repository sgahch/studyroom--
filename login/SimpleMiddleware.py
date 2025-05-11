import re
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def is_ajax(self, request):
        return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def __call__(self, request):
        path = request.path
        
        # 允许不登录就可以访问的路径
        open_urls = ['/login/', '/login/register/', '/admin/login/', '/admin/logout/', '/captchaHostQuery']
        
        # 如果用户未登录
        if 'name' not in request.session:
            # 如果是 AJAX 请求，返回 JSON 响应
            if self.is_ajax(request):
                return JsonResponse({'status': 'error', 'message': '请先登录'}, status=401)
            # 如果是需要登录的页面，重定向到登录页面
            elif path not in open_urls:
                sign_code = request.GET.get('sign_code', '')
                return redirect(f'/login/?path={request.path_info}?sign_code={str(sign_code)}')
                
        response = self.get_response(request)
        return response
