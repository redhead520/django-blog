import scrapy
import os
import json

ROOT_DIR = os.path.dirname(__file__)
web_settings = json.load(open(os.path.join(ROOT_DIR, 'conf', 'qidian.json'), 'r'))

def run(crawl_name):
    from scrapy.utils.project import get_project_settings
    from scrapy.crawler import CrawlerRunner
    from twisted.internet import reactor

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(crawl_name)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

class CategorySpider(scrapy.Spider):
    name = 'get_qidian_category'
    allowed_domains = ['www.qidian.com']
    start_urls = ["https://www.qidian.com/all"]

    # def __init__(self, name=None, **kwargs):
    #     super(CategorySpider, self).__init__(name=name, **kwargs)
    #     self.init_website_data()

    def parse(self, response):
        for cate in response.css(".select-list .sub-type a"):
            print(cate)


class GetAllNovelSpider(scrapy.Spider):
    name = 'qidian_all_novel'
    allowed_domains = ['https://www.qidian.com']
    start_urls = ['https://www.qidian.com/']

    def __init__(self, name=None, **kwargs):
        super(GetAllNovelSpider, self).__init__(name=name, **kwargs)
        self.init_website_data()

    def init_website_data(self):
        pass

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