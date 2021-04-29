import scrapy


class GetNovelChapterSpider(scrapy.Spider):
    name = 'get_novel_chapter'
    allowed_domains = ['https://www.qidian.com']
    start_urls = ['http://https://www.qidian.com/']

    def parse(self, response):
        pass
