
# from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    # 商品列表页
    url(r'carts/$', views.CartsView.as_view(), name='info'),
    url(r'carts/selection/$', views.CartsSelectAllView.as_view()),
    url(r'carts/simple/$', views.CartsSimpleView.as_view(), name='simple'),
]