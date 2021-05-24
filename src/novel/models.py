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
        
# 起点 https://www.qidian.com/all?orderId=&page=1&style=1&pageSize=50&siteid=1&pubflag=0&hiddenField=0 前5页

# 玄幻 东方玄幻 异世大陆 王朝争霸 高武世界 历史神话  https://www.qidian.com/all?chanId=21&subCateId=8&orderId=&page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0
# 奇幻 现代魔法 剑与魔法 史诗奇幻 黑暗幻想 另类幻想
# 武侠 传统武侠 武侠幻想 国术无双 古武未来 武侠同人
# 仙侠 修真文明 幻想修仙 现代修真 神话修真 古典仙侠
# 都市 都市生活 都市异能 异术超能 青春校园 娱乐明星 商战职场
# 现实 社会乡土 生活时尚 文学艺术 成功励志 青春文学 爱情婚姻 现实百态
# 军事 军旅生涯 军事战争 战争幻想 抗战烽火 谍战特工
# 历史 架空历史 秦汉三国 上古先秦 历史传记 两晋隋唐 五代十国 两宋元明 清史民国 外国历史 民间传说
# 游戏 电子竞技 虚拟网游 游戏异界 游戏系统 游戏主播
# 体育 篮球运动 体育赛事 足球运动
# 科幻 古武机甲未 来世界 星际文明 超级科技 时空穿梭 进化变异 末世危机
# 悬疑 诡秘悬疑 奇妙世界 侦探推理 探险生存 古今传奇
# 轻小说 原生幻想 恋爱日常 衍生同人 搞笑吐槽
# 短篇 诗歌散文 人物传记 影视剧本 评论文集 生活随笔 美文游记 短篇小说

# 纵横中文网 http://book.zongheng.com/store/c1/c3116/b0/u0/p1/v9/s9/t0/u0/i1/ALL.html  基本上所有的小说
# 奇幻玄幻 变身情缘  东方玄幻 异世大陆 转世重生 异术超能 上古神话 魔法校园 王朝争霸 吸血传奇 === 西方奇幻
# 武侠仙侠 古典仙侠 现代修真  奇幻修真 === 新派武侠 传统武侠
# 历史军事 穿越历史 架空历史 历史传记 ===
# 都市娱乐 现实题材 职场商战 江湖情仇 都市重生 都市异能 都市生活 青春校园 ===
# 科幻游戏 穿梭时空 末世危机 进化变异 星际争霸  科技时代 === 游戏攻略 游戏小说 游戏评论 游戏设定 虚拟网游
# 悬疑灵异 推理悬念  === 恐怖惊悚 灵异神怪 探险异闻 神秘文化
# 竞技同人 动漫同人 影视同人 小说同人 游戏同人 ===> (轻小说)  电子竞技 体育竞技 ==>（游戏）
# 评论文集 个人文集 集体创作   ==> 短篇
# 二次元  原生幻想 青春日常 动漫衍生 游戏世界 变身入替 奇妙物语

# 17K https://www.17k.com/all/book/2_21_122_0_0_0_0_0_1.html 所有的小说
# 男频
# 玄幻奇幻 异世争霸  东方玄幻 异界大陆 异术超能 === 魔法校园 领主贵族 西方奇幻
# 仙侠武侠 洪荒封神 现代异侠 奇幻修真 现代修真 古典仙侠 === 国术古武 传统武侠 历史武侠
# 都市小说 都市生活 都市异能 都市重生 职场励志 现实题材 娱乐明星 都市激战 商业大亨 校园风云 乡村乡土
# 历史军事 历史穿越 架空历史 历史传奇  === 战史风云 谍战特工 战争幻想 军旅生涯
# 游戏竞技 虚拟网游 电子竞技 游戏生涯 篮球风云 天下足球 棋牌桌游 游戏异界 体育竞技  ==> (游戏)
# 科幻末世 末世危机 进化变异 时空穿梭 未来幻想 古武机甲 星际战争  ===> (科幻)
# 悬疑推理 民间奇谈 恐怖悬疑 侦探推理 探险揭秘 ===> (悬疑)
# 轻小说 爆笑幽默 男生同人 宅系小说 萌系小说 灵魂转换
# 女频
# 都市言情  总裁豪门 游戏情缘 都市情缘 现代重生 娱乐明星 民国旧影 跨国情缘 职场丽人 婚恋爱情
# 古装言情 快意江湖 架空历史 古代重生 前世今生 经商种田 宫廷贵族 穿越时空 家宅恩怨
# 幻想言情 玄幻仙侠 异界魔法 星际科幻 灵异悬疑 末世危机 异能空间 西方奇幻
# 浪漫青春 网配快穿 校园青春 纯爱青春 悲伤青春 女生同人

# 多多看书 https://xiaoshuo.sogou.com/ 基本上所有的小说
# 男频 https://xs.sogou.com/nansheng/
# 女频 https://xs.sogou.com/nvsheng/
# 男生分类
# 玄幻 奇幻 武侠 仙侠 都市 (现实, 轻小说) 游戏 悬疑 历史 军事 灵异 言情 科幻 职场 恐怖 体育 二次元 短篇 其他 乡村
# 女生分类
# 现代言情 穿越重生 豪门总裁 仙侠奇缘 古代言情 青春校园 同人小说 耽美小说 玄幻言情 悬疑灵异 科幻空间 游戏竞技 其他 二次元


# 笔趣阁

# 玄幻 修真 都市 穿越 网游 科幻 其他 灵异
# http://www.tycqxs.com/
# http://www.xbiquge.la/
# https://www.xbiquge.cc/
# https://www.biqudd.com
# http://www.biquger.com/
# http://www.biquge.se/
# https://www.biquduu.com/
# https://www.biquge5200.cc/
# https://www.biqubao.com/
# https://www.1biquge.com/
# https://www.biquwu.cc/






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
    abstract = models.CharField('内容摘要', max_length=300, null=True)
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


