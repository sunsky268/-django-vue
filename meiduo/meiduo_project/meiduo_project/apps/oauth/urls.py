from django.urls import path
from . import views


urlpatterns = [
    # 提供qq登陆扫码页面
    path('qq/login/', views.QQAuthURLView.as_view()),
    # 处理qq登陆回调
    path('oauth_callback/', views.QQAuthUserView.as_view()),
]