from collections import OrderedDict

from meiduo_project.apps.goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory


def get_categorier():
    # 查询商品频道和分类
    # 准备商品分类对应的字典
    categories = OrderedDict()
    # 查询所有的商品频道：37个一级类别
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    # 遍历所有频道
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的一级类别

        # 将cat1添加到channels
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别-查询二级和三级类别
        for cat2 in cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)
            # 将二级类别添加到一级类别的sub_cats
            categories[group_id]['sub_cats'].append(cat2)
    return categories