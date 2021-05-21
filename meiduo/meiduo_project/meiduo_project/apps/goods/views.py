from django.shortcuts import render
from django.views import View
from django import http
from django.core.paginator import Paginator, EmptyPage  #分页器
import logging
from django.utils import timezone
from datetime import datetime

from meiduo_project.apps.goods.models import GoodsCategory, SKU, GoodsVisitCount
from meiduo_project.apps.goods.utils import get_breadcrumb
from meiduo_project.apps.contents.utils import get_categorier
from meiduo_project.utils.response_code import RETCODE
# Create your views here.

# 创建日志器
logger = logging.getLogger('django')


class DetailVisitView(View):
    """详情页分类商品访问量"""

    def post(self, request, category_id):
        """记录分类商品访问量"""
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('缺少必传参数')

        # 获取当天的日期
        t = timezone.localtime()
        # 获取当天的时间字符串
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        # 将当天时间字符串转事件对象datatime,为了跟data字段的类型匹配
        today_date = datetime.strptime(today_str, '%Y-%m-%d')

        try:
            # 查询今天该类别的商品的访问量，如果存在直接获取记录对应对象
            counts_data = category.goodsvisitcount_set.get(date=today_date)
        except GoodsVisitCount.DoesNotExist:
            # 如果该类别的商品在今天没有过访问记录，就新建一个访问记录
            counts_data = GoodsVisitCount()

        try:
            counts_data.category = category
            counts_data.count += 1
            counts_data.data = today_date
            counts_data.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('服务器异常')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})


class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categorier()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
            'sku': sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context)


class HotGoodsView(View):
    """热销排行"""
    def get(self, request, category_id):
        # 查询指定分页的sku信息，而且必须是上架状态，然后按销量由高到低排序，最后切片出前两个
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 将模型列表转字典列表，构造json数据
        hot_skus = []
        for sku in skus:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url  # 要取出全路径
            }
            hot_skus.append(sku_dict)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'hot_skus':hot_skus })


class ListView(View):
    """商品列表页"""
    def get(self, request, category_id, page_num):
        # 查询并渲染商品列表页

        # 校验参数category_id的范围
        try:
            # 三级类别
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNoExist:
            return http.HttpResponseForbidden('参数category_id,有误')

        # 查询商品分类
        categories = get_categorier()

        # 查询面包屑导航：一级>二级>三级
        breadrumb = get_breadcrumb(category)

        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')

        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'  # 防止用户传入非正常数据
            sort_field = 'create_time'
        print('三级对象：', category)

        # 分页和排序查询：category查询sku，一查多：一方的模型对象.多方关联字段.all/filter
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)

        # 创建分页器
        # paginator = Paginator('要分页的记录', '每页记录数')
        paginator = Paginator(skus, '5')
        try:
            # 获取用户当前要看的那一页（核心数据）
            page_skus = paginator.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        # 获取总页数：前端的分页插件需要使用
        total_page = paginator.num_pages

        # 构造上下文
        context = {
            'categories': categories,
            'breadrumb': breadrumb,
            'page_skus': page_skus,
            'total_page': total_page,
            'page_num': page_num,
            'sort': sort,
            'category_id': category_id,

        }
        return render(request, 'list.html', context)




"""
Unable to get repr for <class 'django.db.models.query.QuerySet'>: 无法读取数据，SKU模型字段default_image_url在生成数据库
时生成default_image，所有需要修改模型类字段为default_image
"""