from django.shortcuts import render
from django.views import View
from collections import OrderedDict   # 有序字典

from meiduo_project.apps.goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory
from meiduo_project.apps.contents.models import ContentCategory
from meiduo_project.apps.contents.utils import get_categorier
# Create your views here.


class IndexView(View):
    # 首页广告
    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categorier()

        # 广告数据
        # 广告类别
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)


"""
注意：1、storage服务安装在ubuntu系统中，通过ubuntu绑定的域名访问storage里存储的图片需要在本机的“hosts”文件中添加ip绑定域名才能正常访问
2、ubuntu防火墙需开放端口8888
3、storage服务是否正常启动
"""

