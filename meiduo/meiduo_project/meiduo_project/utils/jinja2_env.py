# 模板引擎环境配置工具文件

from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage   # 静态文件存储


def jinja2_environment(**options):
    """jinja2环境"""
    # 创建环境对象
    env = Environment(**options)

    # 自定义语法：{{ ststic(’静态文件相对路径‘) }}、{{ url('路由的命名空间') }}
    env.globals.update({
        'static': staticfiles_storage.url,  # 获取静态文件的前缀
        'url': reverse,  # 重定向/反向解析
    })

    # 返回环境对象
    return env
