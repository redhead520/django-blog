import scrapy
import os
import json
import re
from pprint import pprint

ROOT_DIR = os.path.dirname(__file__)
SETTING_PATH = os.path.join(ROOT_DIR, 'conf', 'qidian.json')
web_settings = json.load(open(SETTING_PATH, 'r'))
cate_mapping = {ca: c for c in web_settings['category'] for ca in web_settings['category'][c]}


def run(crawl_name):
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerRunner
    from twisted.internet import reactor

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(crawl_name)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

class CategoryItem(scrapy.Item):
    # define the fields for your item here like:
    cate_param = scrapy.Field()
    cate_name = scrapy.Field()
    tag = scrapy.Field()


class CategorySpider(scrapy.Spider):
    name = 'get_qidian_category'
    allowed_domains = ['www.qidian.com']
    start_url = "https://www.qidian.com/all"
    start_urls = []
    category_param = []

    def __init__(self, name=None, **kwargs):
        super(CategorySpider, self).__init__(name=name, **kwargs)
        self.web_settings = json.load(open(SETTING_PATH, 'r'))
        self.cate_mapping = {ca: c for c in self.web_settings['category'] for ca in self.web_settings['category'][c]}


    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.first_parse)

    def first_parse(self, response):
        for cate in response.css(".select-list .type-filter ul>li"):
            _id = cate.css("li::attr(data-id)").extract_first()
            if _id != '-1':
                _url = cate.css("a::attr(href)").extract_first()
                _url = 'https:' + _url if _url.startswith('//www.q') else _url
                self.start_urls.append(_url)
        for _url in self.start_urls:
                yield scrapy.Request(url=_url, callback=self.parse)

    def parse(self, response):
        for cate in response.css(".select-list .type-filter div.sub-type dl:not(.hidden)>dd"):
            _tag = cate.css("a::text").extract_first()
            self.category_param.append({
                'tag': _tag,
                'cate_name': self.cate_mapping.get(_tag),
                'cate_param': cate.css("a::attr(href)").re('.*(chanId=\d+&subCateId=\d+)')[0]
            })

    def closed(self, reson):
        self.web_settings['category_param'] = self.category_param
        with open(SETTING_PATH, 'w') as f:
            json.dump(self.web_settings, f, indent=4, ensure_ascii=False)


class GetAllNovelSpider(scrapy.Spider):
    name = 'qidian_all_novel'
    allowed_domains = ['www.qidian.com']
    start_urls = ["https://www.qidian.com/all?chanId=20076&subCateId=20078&size=3&action=1&orderId=&page=2&vip=1&sign=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0"]

    def __init__(self, name=None, **kwargs):
        super(GetAllNovelSpider, self).__init__(name=name, **kwargs)
        self.web_settings = json.load(open(SETTING_PATH, 'r'))
        self.cate_mapping = {c['cate_param']: c for c in self.web_settings['category_param']}
        self.count = 0
        self.init_start_urls()

    def init_start_urls(self):
        for cate_param in self.web_settings['category_param']:
            for size in self.web_settings['url_param']['size']:
                for vip in self.web_settings['url_param']['vip']:
                    for action in self.web_settings['url_param']['action']:
                        for sign in self.web_settings['url_param']['sign']:
                            for update in self.web_settings['url_param']['update']:
                                for page in self.web_settings['url_param']['page']:
                                    _url = self.web_settings['start_url'].format(
                                        cate_param=cate_param['cate_param'],
                                        size=size,
                                        vip=vip,
                                        action=action,
                                        sign=sign,
                                        update=update,
                                        page=page
                                    )
                                    if self.count == 0:
                                        self.start_urls.append(_url)
                                    self.count += 1
                                    # print(self.count)

    def parse(self, response):
        cate_param = re.search('(chanId=\d+&subCateId=\d+)', response.url).group()
        cate = self.cate_mapping[cate_param]
        print(response.url)
        if response.css("div.no-data"):
            print(response.css("div.no-data>h3::text").extract_first())  # 没有找到符合条件的书
            yield
        for novel in response.css("div.all-book-list .book-img-text ul.all-img-list>li"):
            name = novel.css("div.book-mid-info>h4>a::text").extract_first()
            novel_url = novel.css("div.book-img-box>a::attr(href)").extract_first()
            novel_author = novel.css("div.book-mid-info>p.author>a.name::text").extract_first()
            novel_author_home_url = novel.css("div.book-mid-info>p.author>a.name::attr(href)").extract_first()
            novel_type = novel.css("div.book-mid-info > p.author > a:nth-child(4)::text").extract_first()
            novel_cover = novel.css("div.book-img-box img::attr(src)").extract_first()
            novel_abstract = novel.css("div.book-mid-info p.intro::text").extract_first()
            # novel_size = novel.css("div.book-mid-info p.update>span>span::text").extract_first()
            novel_item = {
                "name": name,
                "novel_url": 'https:' + novel_url if novel_url.startswith('//book.qidian') else novel_url,
                "novel_author": novel_author,
                # "novel_size": novel_size,
                "novel_author_home_url": 'https:' + novel_author_home_url if novel_author_home_url.startswith('//my.qidian') else novel_author_home_url,
                "novel_type": novel_type,
                "novel_cover": 'https:' + novel_cover if novel_cover.startswith('//bookcover') else novel_cover,
                "novel_abstract": novel_abstract.replace('\r', '').strip(),
                "novel_cate": cate['cate_name'],
                "tag": cate['tag'],
            }
            pprint(novel_item)

            yield novel_item


if __name__ == '__main__':
    # run('get_qidian_category')
    run('qidian_all_novel')
    # from scrapy.utils.project import get_project_settings
    # from scrapy.crawler import CrawlerRunner
    # from twisted.internet import reactor
    #
    # runner = CrawlerRunner(get_project_settings())
    # d = runner.crawl()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()
    # print(web_settings['category_select'])
    # print(web_settings['category'])