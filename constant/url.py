

class Url:
    """
    定义url地址
    """
    # 登录
    login = '/login'
    # 首页
    index = '/'
    # 注册
    register = '/register'
    # 注销
    logout = '/logout'
    # 文章列表
    article_list = '/article/list'
    # 文章详情
    article_detail = '/article/detail/{}'
    # 文章添加
    article_add = '/article/add'
    # 文章编辑
    article_edit = '/article/edit/{}'
    # 文章删除
    article_delete = '/article/delete/{}'
    # 文章排序
    article_sort = '/article/sort'
    # 文章分类
    article_category = '/article/category'
    # 文章分类添加
    article_category_add = '/article/category/add'
    # 文章分类编辑
    article_category_edit = '/article/category/edit/{}'
    # 文章分类删除
    article_category_delete = '/article/category/delete/{}'
    # 文章分类排序
    article_category_sort = '/article/category/sort'