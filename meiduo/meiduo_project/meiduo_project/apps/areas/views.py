from django.shortcuts import render
from django.views import View
from django import http
import logging
from django.core.cache import cache

from meiduo_project.apps.areas.models import Area
from meiduo_project.utils.response_code import RETCODE

# Create your views here.

logger = logging.getLogger('django')


class AreasView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            # 获取并判断是否存在缓存
            province_list = cache.get('province_list')
            if not province_list:
                # 提供省份数据
                try:
                    # 查询省份数据
                    # Area.object.filter(属性名—__条件表达式=值)
                    province_model_list = Area.objects.filter(parent__isnull=True)

                    # 序列化省级数据；需要将模型列表转化为字典列表
                    province_list = []
                    for province_model in province_model_list:
                        province_list.append({'id': province_model.id, 'name': province_model.name})
                    # 缓存省份字典列表数据,默认存储到名为default的redis数据表中
                    cache.set('province_list', province_list, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})
            # 响应省份数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})

        else:
            # 判断是否有缓存
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                # 提供市或区数据
                try:
                    parent_model = Area.objects.get(id=area_id)  # 查询市或区的父级
                    # sub_models_list = parent_model.area_set.all()
                    sub_model_list = parent_model.subs.all()

                    # 序列化市或区数据， 将子级模型列表转成字典列表
                    sub_list = []
                    for sub_model in sub_model_list:
                        sub_list.append({'id': sub_model.id, 'name': sub_model.name})

                    # 构造子级json数据
                    sub_data = {
                        'id': parent_model.id,  # 父级pk
                        'name': parent_model.name,  # 父级name
                        'subs': sub_list  # 父级的子集
                    }
                    # 缓存市或区县
                    cache.set('sub_area_' + area_id, sub_data, 3600)
                except Exception as e:
                    logger.error(e)
                    return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})

            # 响应市或区数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})