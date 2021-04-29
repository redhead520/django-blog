import scrapy


class GetNewNovelSpider(scrapy.Spider):
    name = 'get_new_novel'
    allowed_domains = ['https://www.qidian.com']
    start_urls = ['http://https://www.qidian.com/']

    def parse(self, response):
        pass
