# 邮箱绑定前判断是否登录，重写模块
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from meiduo_project.utils.response_code import RETCODE


class LoginRequireJsonMixin(LoginRequiredMixin):
    """自定义判断用户是否登录的扩展模块：返回json"""
    def handle_no_permission(self):
        """直接响应json数据"""
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})