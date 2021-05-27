import scrapy
import os
import json

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
    allowed_domains = ['https://www.qidian.com']
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(GetAllNovelSpider, self).__init__(name=name, **kwargs)
        self.web_settings = json.load(open(SETTING_PATH, 'r'))
        self.init_start_urls()

    def init_start_urls(self):
        for cate_param in self.web_settings['category_param']:
            for key, values in self.web_settings['url_param'].items():
                for value in values:
                    _url = ''
                   self.start_urls.append(_url)

    def parse(self, response):
        print(web_settings)


if __name__ == '__main__':
    run('get_qidian_category')
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