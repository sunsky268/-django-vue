# celery入口
from celery import Celery
import os

# 为celery使用django配置文件进行设置-celery不同进程不能访问djano
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_project.settings.dev'
# 创建celery实例
celery_app = Celery('meiduo')

# 加载配置
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms', 'send_verify_email'])