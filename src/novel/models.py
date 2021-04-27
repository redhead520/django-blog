from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Q


class NovelBase(models.Model):
    name = models.CharField('名称', max_length=50)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True
    

class BookSource(NovelBase):
    name = models.CharField('名称', max_length=70)
    host = models.CharField('域名', max_length=70)
    book_url = models.CharField('小说详情地址', max_length=170, default='https://book.qidian.com/info/{}#Catalog')
    chapter_url = models.CharField('小说目录地址', max_length=170, default='https://book.qidian.com/info/{}#Catalog')
    
    select_novel_name = models.CharField('书名-选择器', max_length=170,  default="xpath|content|meta[property='og:title']")
    select_author = models.CharField('作者-选择器', max_length=170, default="meta[property='og:novel:author']")
    select_cover = models.CharField('封面图-选择器', max_length=170, default="meta[property='og:image']")
    select_description = models.CharField('内容简介-选择器', max_length=170, default="meta[property='og:description']")
    select_state = models.CharField('状态-选择器', max_length=170, default="meta[property='og:novel:status']")
    select_novels_category = models.CharField('分类-选择器', max_length=170, default="meta[property='og:novel:category']")
    select_novel_chapter_name = models.CharField('章节标题-选择器', max_length=170, default='div#voteList a.index')
    select_novel_chapter_url = models.CharField('章节地址-选择器', max_length=170, default='div#voteList a.index')
    select_novel_chapter_content = models.CharField('章节内容-选择器', max_length=170, default='div#voteList a.index')
    select_latest_chapter = models.CharField('最新章节-选择器', max_length=170, default="meta[property='og:novel:latest_chapter_name']")
    select_latest_chapter_url = models.CharField('最新章节地址-选择器', max_length=170, default="meta[property='og:novel:latest_chapter_url']")
    select_latest_chapter_time = models.CharField('最后更新时间-选择器', max_length=170, default="meta[property='og:novel:update_time']")
    sequence = models.IntegerField('排序', unique=True, default=10)
    active = models.BooleanField('是否启用', default=True)
    
    class Meta:
        verbose_name = "网站来源"
        verbose_name_plural = verbose_name


class Author(NovelBase):
    
    name = models.CharField('姓名', max_length=20, unique=True)
    sequence = models.IntegerField('排序', unique=True, default=10)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name


class Category(NovelBase):
    CHANNEL_CHOICES = (
        ('boy', '男频'),
        ('girl', '女频'),
        ('normal', '图书'),
    )
    name = models.CharField('名称', max_length=30, unique=True)
    channel = models.CharField('频道', max_length=30, choices=CHANNEL_CHOICES, default=CHANNEL_CHOICES[0][0])
    sequence = models.IntegerField('排序', unique=True, default=10)
    
    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(NovelBase):
    sequence = models.IntegerField('排序', unique=True, default=10)
    
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name
        

class Book(NovelBase):
    STATE_CHOICES = (
        ('continue', '连载中'),
        ('done', '完本')
    )
    name = models.CharField('书名', max_length=70, unique=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(Author, verbose_name='作者', on_delete=models.CASCADE)
    state = models.CharField('状态', max_length=30, choices=STATE_CHOICES, default=STATE_CHOICES[0][0])
    
    # store_des = models.IntegerField(verbose_name='book_table_index', null=True)
    cover = models.CharField('封面图', max_length=70, null=True)
    description = models.CharField('内容简介', max_length=300, null=True)
    words_count = models.IntegerField('字数', default=0)
    collection_count = models.IntegerField('收藏数', default=0)
    ranking = models.IntegerField('排名权重', default=0)

    latest_chapter = models.CharField('最新章节', max_length=70, null=True)
    latest_chapter_url = models.CharField('最新章节地址', max_length=70, null=True)
    latest_chapter_time = models.DateTimeField('最后更新时间', null=True)

    class Meta:
        verbose_name = "小说"
        verbose_name_plural = verbose_name


class Chapter(NovelBase):
    
    name = models.CharField('标题', max_length=70)
    book = models.ForeignKey(Book, verbose_name='小说', on_delete=models.CASCADE)
    sequence = models.IntegerField('排序', unique=True, default=10)
    content = models.TextField('内容')
    source_id = models.ForeignKey(BookSource, verbose_name='网站来源', on_delete=models.CASCADE)
    next_chapter_id = models.IntegerField(verbose_name='下一章节', default=0)
    prev_chapter_id = models.IntegerField(verbose_name='上一章节', default=0)
    
    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name


