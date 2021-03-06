# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     context_processors.py  
   Description :  
   Author :       Afa
   date：          2017/4/14
-------------------------------------------------
   Change Activity:
                   2017/4/14: 
-------------------------------------------------
"""
__author__ = 'Afa'

import importlib
from blog.models import Category, Article, Tag, Comment, Links


def sidebar(request):
    category_list = Category.objects.all()
    # 所有类型

    blog_top = Article.objects.all().values("id", "title", "view").order_by('-view')[0:6]
    # 文章排行

    tag_list = Tag.objects.all()
    # 标签

    comment = Comment.objects.all().order_by('-create_time')[0:6]
    # 评论

    # importlib.reload(blogroll)
    # 友链
    _links = Links.get_links()

    return {
        'category_list': category_list,
        'blog_top': blog_top,
        'tag_list': tag_list,
        'comment_list': comment,
        'links': _links

    }


if __name__ == '__main__':
    pass
