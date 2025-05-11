"""
URL configuration for studyroom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path  # 修改：添加 re_path 导入
from django.views.static import serve  # 添加：导入serve视图函数
from index import views as index_views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('index.urls')),
    path('', include('login.urls')),
    path('bookings/', index_views.bookings, name='Bookings'),  # 修正：使用index.views中的bookings视图
    path('api/', include('index.api.urls')),  # 添加API路由
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加媒体文件的URL配置
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

