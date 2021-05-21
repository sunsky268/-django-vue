

def get_breadcrumb(category):
    # 获取面包屑导航
    breadrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': ''
    }
    if category.parent == None:  # 说明category是一级
        breadrumb['cat1'] = category
    elif category.subs.count() == 0:  # 说明category是三级
        cat2 = category.parent
        breadrumb['cat1'] = cat2.parent
        breadrumb['cat2'] = cat2
        breadrumb['cat3'] = category
    else:
        breadrumb['cat1'] = category.parent
        breadrumb['cat2'] = category
    return breadrumb