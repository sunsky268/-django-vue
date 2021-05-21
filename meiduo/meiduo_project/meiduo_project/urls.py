"""meiduo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('search/', include('haystack.urls')),
    path('admin/', admin.site.urls),
    path('', include(('meiduo_project.apps.users.urls', 'users'), namespace='users')),  # 注册、登录
    path('', include(('meiduo_project.apps.contents.urls', 'contents'), namespace='contents')),  # 首页广告
    path('', include('meiduo_project.apps.verifications.urls')),  # 验证码模块
    path('', include('meiduo_project.apps.oauth.urls')),  # QQ登录子应用
    path('', include('meiduo_project.apps.areas.urls')),  # 省市区三级联动
    path('', include(('meiduo_project.apps.goods.urls', 'goods'), namespace='goods')),  # 商品列表页
    path('', include(('meiduo_project.apps.carts.urls', 'carts'), namespace='carts')),
    path('', include(('meiduo_project.apps.orders.urls', 'carts'), namespace='orders')),  # 订单
]
