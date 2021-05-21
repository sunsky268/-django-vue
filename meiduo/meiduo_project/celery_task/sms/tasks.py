# 定义任务
from celery_task.main import celery_app


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    # send_ret = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)
    send_ret = 'test'
    print('注册用户输入的手机号是：', mobile)
    return send_ret
