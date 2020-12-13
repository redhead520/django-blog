# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     models.py
   Description :
   Author :       Afa
   date：          2016/11/18
-------------------------------------------------
   Change Activity:
                   2016/11/18:
-------------------------------------------------
"""
from django.core.cache import cache
from django.utils.timezone import now
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from mdeditor.fields import MDTextField
import logging
logger = logging.getLogger(__name__)

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField('标签名称', max_length=30)

    def __str__(self):
        return self.tag_name
    
    class Meta:  # 按时间降序
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')  # 博客标题
    category = models.ForeignKey('Category', verbose_name='文章类型', on_delete=models.CASCADE)
    date_time = models.DateField(auto_now_add=True, verbose_name='日期')  # 博客日期
    content = MDTextField(blank=True, null=True, verbose_name='正文')  # 文章正文
    digest = models.TextField(blank=True, null=True, verbose_name='摘要')  # 文章摘要
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    view = models.BigIntegerField(default=0, verbose_name='阅读数')  # 阅读数
    comment = models.BigIntegerField(default=0, verbose_name='评论数')  # 评论数
    picture = models.CharField(max_length=200, verbose_name='图片地址')  # 标题图片地址
    tag = models.ManyToManyField(Tag, verbose_name='标签')  # 标签

    def __str__(self):
        return self.title

    def sourceUrl(self):
        source_url = settings.HOST + '/blog/detail/{id}'.format(id=self.pk)
        return source_url  # 给网易云跟帖使用

    def viewed(self):
        """
        增加阅读数
        :return:
        """
        self.view += 1
        self.save(update_fields=['view'])

    def commenced(self):
        """
        增加评论数
        :return:
        """
        self.comment += 1
        self.save(update_fields=['comment'])

    class Meta:  # 按时间降序
        ordering = ['-date_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField('文章类型', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "文章类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    title = models.CharField("标题", max_length=100)
    source_id = models.CharField('文章id或source名称', max_length=25)
    create_time = models.DateTimeField('评论时间', auto_now=True)
    user_name = models.CharField('评论用户', max_length=25)
    url = models.CharField('链接', max_length=100)
    comment = models.CharField('评论内容', max_length=500)
    

class Links(models.Model):
    """友情链接"""

    name = models.CharField('链接名称', max_length=30, unique=True)
    link = models.URLField('链接地址')
    sequence = models.IntegerField('排序', unique=True)
    description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_links()

    @classmethod
    def get_links(cls):
        value = cache.get('get_blog_links')
        if value:
            return value
        value = Links.objects.filter(is_enable=True).order_by("sequence")
        logger.info('set cache get_blog_links')
        cache.set('get_blog_links', value)
        return value

    def refresh_links(self):
        cache.delete('get_blog_links')
        return self.get_links()


class Carousels(models.Model):
    """首页轮播图"""
    name = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='carousels/', default='default/mygirl.jpg', blank=False, null=False)
    link = models.CharField('跳转地址', max_length=200)
    sequence = models.IntegerField('排序', unique=True)
    is_enable = models.BooleanField('是否启用', default=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_carousels()

    @classmethod
    def get_carousels(cls):
        value = cache.get('get_blog_carousels')
        if value:
            return value
        value = Carousels.objects.filter(is_enable=True).order_by("sequence")
        logger.info('set cache get_blog_carousels')
        cache.set('get_blog_carousels', value)
        return value

    def refresh_carousels(self):
        cache.delete('get_blog_carousels')
        return self.get_carousels()


class BlogSettings(models.Model):
    '''站点设置 '''
    name = models.CharField("网站名称", max_length=200, null=False, blank=False, default='字节阁')
    title = models.CharField("网站标题", max_length=200, null=False, blank=False, default='字节阁 - 黄少的博客')
    description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    seo_description = models.TextField("网站SEO描述", max_length=1000, null=False, blank=False, default='')
    keywords = models.TextField("关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_length = models.IntegerField("文章摘要长度", default=300)
    sidebar_article_count = models.IntegerField("侧边栏文章数目", default=10)
    sidebar_comment_count = models.IntegerField("侧边栏评论数目", default=5)
    show_google_adsense = models.BooleanField('是否显示谷歌广告', default=False)
    google_adsense_codes = models.TextField('广告内容', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    show_carousels = models.BooleanField('是否显示轮播图', default=True)
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=True, blank=True, default='')
    copy_right = models.CharField('版权申明', max_length=2000, null=True, blank=True, default='2020-2022 字节阁-黄少')
    beiancode = models.CharField('ICP备案号', max_length=2000, null=True, blank=True, default='')
    show_gongan_code = models.BooleanField('是否显示公安备案号', default=False, null=True)
    gongan_beiancode = models.CharField('公安备案号', max_length=2000, null=True, blank=True, default='')
    resource_path = models.CharField("静态文件保存地址", max_length=300, null=True, default='/var/www/resource/')
    multi_messages = models.TextField("滚动消息", max_length=1000, null=True, blank=True, default='')
    github_url = models.URLField("GitHub地址", max_length=1000, null=True, blank=True, default='https://github.com/redhead520')
    download_url = models.URLField("下载地址", max_length=1000, null=True, blank=True, default='https://github.com/redhead520')
    changyan_code = models.TextField("畅言评论代码", max_length=2000, null=True, blank=True, default="""
<script type="text/javascript">
(function(){
var appid = 'cyv9d1zOD';
var conf = 'prod_65d69aa1e9903b59a3753409fde50f27';
var width = window.innerWidth || document.documentElement.clientWidth;
if (width < 960) {
var head = document.getElementsByTagName('head')[0]||document.head||document.documentElement;
var script = document.createElement('script');
script.type = 'text/javascript';
script.charset = 'utf-8';
script.id = 'changyan_mobile_js';
script.src = 'https://cy-cdn.kuaizhan.com/upload/mobile/wap-js/changyan_mobile.js?client_id=' + appid + '&conf=' + conf;
head.appendChild(script);
} else { var loadJs=function(d,a){var c=document.getElementsByTagName("head")[0]||document.head||document.documentElement;var b=document.createElement("script");b.setAttribute("type","text/javascript");b.setAttribute("charset","UTF-8");b.setAttribute("src",d);if(typeof a==="function"){if(window.attachEvent){b.onreadystatechange=function(){var e=b.readyState;if(e==="loaded"||e==="complete"){b.onreadystatechange=null;a()}}}else{b.onload=a}}c.appendChild(b)};loadJs("https://cy-cdn.kuaizhan.com/upload/changyan.js",function(){window.changyan.api.config({appid:appid,conf:conf})}); } })(); </script>
    """)

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def clean(self):
        if BlogSettings.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能有一个配置'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refresh_blog_setting()
    
    @classmethod
    def get_blog_setting(cls):
        value = cache.get('get_blog_setting')
        if value:
            return value
        else:
            if not BlogSettings.objects.count():
                setting = BlogSettings()
                setting.name = '黄少的博客'
                setting.description = '黄少的博客'
                setting.seo_description = '黄少的博客,python,odoo'
                setting.keywords = 'Django,Python'
                setting.article_sub_length = 300
                setting.sidebar_article_count = 10
                setting.sidebar_comment_count = 5
                setting.show_google_adsense = False
                setting.open_site_comment = True
                setting.analyticscode = ''
                setting.beiancode = ''
                setting.show_gongan_code = False
                setting.save()
            value = BlogSettings.objects.first()
            logger.info('set cache get_blog_setting')
            cache.set('get_blog_setting', value)
            return value

    def refresh_blog_setting(self):
        cache.delete('get_blog_setting')
        return self.get_blog_setting()