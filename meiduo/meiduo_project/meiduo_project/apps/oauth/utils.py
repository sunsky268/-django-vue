from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData

from . import constants


def check_access_token(access_token_openid):
    """反解、反序列access_token_openid"""
    # 创建序列化器对象：序列化和反序列化的对象的参数必须是一模一样
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.ACCESS_TOKEN_EXPIRES)

    # 反序列化openid密文
    try:
        data = serializer.load(access_token_openid)
    except BadData:  # openid密文过期
        return None
    else:
        # 返回openid明文
        return data.get('openid')


def generate_eccess_token(openid):
    """
    签名openid
    :param openid: 用户的openid
    :return: access_token
    """
    # serializer = Serializer(秘钥, 有效期秒)
    serializer = Serializer(settings.SECRET_KEY, expires_in=constants.ACCESS_TOKEN_EXPIRES)
    # serializer.dumps(数据), 返回bytes类型
    data = {'openid': openid}
    token = serializer.dumps(data)
    return token.decode()