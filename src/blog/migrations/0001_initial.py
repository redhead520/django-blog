# Generated by Django 2.2.13 on 2020-12-13 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='字节阁', max_length=200, verbose_name='网站名称')),
                ('title', models.CharField(default='字节阁 - 黄少的博客', max_length=200, verbose_name='网站标题')),
                ('description', models.TextField(default='', max_length=1000, verbose_name='网站描述')),
                ('seo_description', models.TextField(default='', max_length=1000, verbose_name='网站SEO描述')),
                ('keywords', models.TextField(default='', max_length=1000, verbose_name='关键字')),
                ('article_sub_length', models.IntegerField(default=300, verbose_name='文章摘要长度')),
                ('sidebar_article_count', models.IntegerField(default=10, verbose_name='侧边栏文章数目')),
                ('sidebar_comment_count', models.IntegerField(default=5, verbose_name='侧边栏评论数目')),
                ('show_google_adsense', models.BooleanField(default=False, verbose_name='是否显示谷歌广告')),
                ('google_adsense_codes', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='广告内容')),
                ('open_site_comment', models.BooleanField(default=True, verbose_name='是否打开网站评论功能')),
                ('show_carousels', models.BooleanField(default=True, verbose_name='是否显示轮播图')),
                ('analyticscode', models.TextField(blank=True, default='', max_length=1000, null=True, verbose_name='网站统计代码')),
                ('copy_right', models.CharField(blank=True, default='2020-2022 字节阁-黄少', max_length=2000, null=True, verbose_name='版权申明')),
                ('beiancode', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='ICP备案号')),
                ('show_gongan_code', models.BooleanField(default=False, null=True, verbose_name='是否显示公安备案号')),
                ('gongan_beiancode', models.CharField(blank=True, default='', max_length=2000, null=True, verbose_name='公安备案号')),
                ('resource_path', models.CharField(default='/var/www/resource/', max_length=300, null=True, verbose_name='静态文件保存地址')),
                ('multi_messages', models.TextField(blank=True, default='', max_length=1000, null=True, verbose_name='滚动消息')),
                ('github_url', models.URLField(blank=True, default='https://github.com/redhead520', max_length=1000, null=True, verbose_name='GitHub地址')),
                ('download_url', models.URLField(blank=True, default='https://github.com/redhead520', max_length=1000, null=True, verbose_name='下载地址')),
                ('changyan_code', models.TextField(blank=True, default='\n<script type="text/javascript">\n(function(){\nvar appid = \'cyv9d1zOD\';\nvar conf = \'prod_65d69aa1e9903b59a3753409fde50f27\';\nvar width = window.innerWidth || document.documentElement.clientWidth;\nif (width < 960) {\nvar head = document.getElementsByTagName(\'head\')[0]||document.head||document.documentElement;\nvar script = document.createElement(\'script\');\nscript.type = \'text/javascript\';\nscript.charset = \'utf-8\';\nscript.id = \'changyan_mobile_js\';\nscript.src = \'https://cy-cdn.kuaizhan.com/upload/mobile/wap-js/changyan_mobile.js?client_id=\' + appid + \'&conf=\' + conf;\nhead.appendChild(script);\n} else { var loadJs=function(d,a){var c=document.getElementsByTagName("head")[0]||document.head||document.documentElement;var b=document.createElement("script");b.setAttribute("type","text/javascript");b.setAttribute("charset","UTF-8");b.setAttribute("src",d);if(typeof a==="function"){if(window.attachEvent){b.onreadystatechange=function(){var e=b.readyState;if(e==="loaded"||e==="complete"){b.onreadystatechange=null;a()}}}else{b.onload=a}}c.appendChild(b)};loadJs("https://cy-cdn.kuaizhan.com/upload/changyan.js",function(){window.changyan.api.config({appid:appid,conf:conf})}); } })(); </script>\n    ', max_length=2000, null=True, verbose_name='畅言评论代码')),
            ],
            options={
                'verbose_name': '网站配置',
                'verbose_name_plural': '网站配置',
            },
        ),
        migrations.CreateModel(
            name='Carousels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标题')),
                ('image', models.ImageField(default='default/mygirl.jpg', upload_to='carousels/', verbose_name='图片')),
                ('link', models.CharField(max_length=200, verbose_name='跳转地址')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否启用')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='文章类型')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '文章类型',
                'verbose_name_plural': '文章类型',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('source_id', models.CharField(max_length=25, verbose_name='文章id或source名称')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='评论时间')),
                ('user_name', models.CharField(max_length=25, verbose_name='评论用户')),
                ('url', models.CharField(max_length=100, verbose_name='链接')),
                ('comment', models.CharField(max_length=500, verbose_name='评论内容')),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='链接名称')),
                ('link', models.URLField(verbose_name='链接地址')),
                ('sequence', models.IntegerField(unique=True, verbose_name='排序')),
                ('description', models.TextField(default='', max_length=1000, verbose_name='网站描述')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('last_mod_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('date_time', models.DateField(auto_now_add=True, verbose_name='日期')),
                ('content', mdeditor.fields.MDTextField(blank=True, null=True, verbose_name='正文')),
                ('digest', models.TextField(blank=True, null=True, verbose_name='摘要')),
                ('view', models.BigIntegerField(default=0, verbose_name='阅读数')),
                ('comment', models.BigIntegerField(default=0, verbose_name='评论数')),
                ('picture', models.CharField(max_length=200, verbose_name='图片地址')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='文章类型')),
                ('tag', models.ManyToManyField(to='blog.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['-date_time'],
            },
        ),
    ]