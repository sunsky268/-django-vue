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
from django.urls import path
from django.conf.urls import url
from . import views
# (?P<username>[a-zA-Z0-9_-]{5-20})
# reverse(user:register=='/statis/')
urlpatterns = [
    # 用户注册
    path('register/', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复
    path('usernames/<str:username>/count/', views.UsernameCountView.as_view()),
    # 用户登录
    path('login/', views.LoginView.as_view(), name='login'),
    # 用户退出
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    path('info/', views.UserInfoView.as_view(), name='info'),
    # 添加邮箱
    path('emails/', views.EmailView.as_view()),
    # 验证邮箱
    path('emails/verification/', views.VerifyEmailView.as_view()),
    # 用户收货地址
    path('addresses/', views.AddressView.as_view(), name='address'),
    # 新增用户地址
    path('addresses/create/', views.AddressCreateView.as_view()),
    # 新增用户地址
    url(r'addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 修改为默认地址
    url(r'addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 更新地址标题
    url(r'addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    # 用户浏览记录
    url(r'browse_histories/$', views.UserBrowseHistory.as_view()),
]