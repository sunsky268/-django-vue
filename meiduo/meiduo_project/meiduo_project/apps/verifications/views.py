from django.shortcuts import render
from django.views import View
import random, logging
from django_redis import get_redis_connection
from django import http
from . import constants

from meiduo_project.utils.response_code import RETCODE
from meiduo_project.apps.verifications.libs.yuntongxun.ccp_sms import CCP
from meiduo_project.apps.verifications.libs.captcha.captcha import captcha
from celery_task.sms.tasks import send_sms_code


# Create your views here.
# 日志器创建
logger = logging.getLogger('django')


class SMSCodeView(View):
    """ 短信验证码 """
    def get(self, request, mobile):
        # 接收参数
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        # 校验参数
        if not all([image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')

        # 提取图形验证码
        redis_conn = get_redis_connection('verify')
        image_code_server = redis_conn.get('image_%s' % uuid)

        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已失效'})
        # 删除图形验证码
        redis_conn.delete('image_%s' % uuid)
        # 对比图形验证码,需要先将byte转换为字符串再比较
        image_code_server = image_code_server.decode()

        if image_code_client.lower() != image_code_server.lower():  # 转换为小写，再比较
            print('请求验证码：', image_code_client)
            print('服务端保存验证码：', image_code_server)
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入的图形验证码有误'})

        # 生成短信验证码：随机6位数字000007
        sms_code = '%06d' % random.randint(0, 999999)
        # 保存短信验证码
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
        # 使用celery发送短信验证码
        send_sms_code.delay(mobile, sms_code)

        # 创建redis管道
        pl = redis_conn.pipeline()
        # 将命令添加到队列中
        # 保存短信验证码
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 执行
        pl.execute()
        print('短信验证码是:', sms_code)

        logger.info(sms_code)
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '发送短信成功'})


class ImageCodeView(View):
    # 图形验证
    def get(self, request, uuid):
        # param uuid: 通用唯一识别码，用于唯一标识该图形验证码属于那个用户，由浏览器页面自动生成
        # 接受和校验参数
        # 实现主体业务逻辑：生成、保存、响应图形验证码
        text, image = captcha.generate_captcha()
        # 保存图形验证码
        redis_conn = get_redis_connection('verify')
        # redis_conn.setex('key', 'expires过期时间', 'value')
        redis_conn.setex('image_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        return http.HttpResponse(image, content_type='image/jpg')