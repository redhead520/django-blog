import scrapy


class GetNovelHotWeightSpider(scrapy.Spider):
    name = 'get_novel_hot_weight'
    allowed_domains = ['https://www.baidu.com']
    start_urls = ['http://https://www.baidu.com/']

    def parse(self, response):
        pass
