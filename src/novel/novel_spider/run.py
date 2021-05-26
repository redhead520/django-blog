# encoding: utf-8
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings


def run1_single_spider():
    '''Running spiders outside projects
    只调用spider，不会进入pipeline'''
    from scrapy.crawler import CrawlerProcess
    from .novel_spider.spiders import get_all_novel
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(get_all_novel)
    process.start()  # the script will block here until the crawling is finished


def run2_inside_scrapy():
    '''会启用pipeline'''
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(get_project_settings())
    process.crawl('get_all_novel')  # scrapy项目中spider的name值
    process.start()


def spider_closing(arg):
    print('spider close')
    reactor.stop()


def run3_crawlerRunner():
    '''如果你的应用程序使用了twisted，建议使用crawlerrunner 而不是crawlerprocess
    Note that you will also have to shutdown the Twisted reactor yourself after the spider is finished. This can be achieved by adding callbacks to the deferred returned by the CrawlerRunner.crawl method.
    '''
    from scrapy.crawler import CrawlerRunner
    runner = CrawlerRunner(get_project_settings())

    # 'spidername' is the name of one of the spiders of the project.
    d = runner.crawl('get_all_novel')

    # stop reactor when spider closes
    # d.addBoth(lambda _: reactor.stop())
    d.addBoth(spider_closing)  # 等价写法

    reactor.run()  # the script will block here until the crawling is finished


def run4_multiple_spider():
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()

    from .novel_spider.spiders import get_all_novel, get_new_novel
    for s in [get_all_novel, get_new_novel]:
        process.crawl(s)
    process.start()


def run5_multiplespider():
    '''using CrawlerRunner'''
    from twisted.internet import reactor
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging

    configure_logging()
    runner = CrawlerRunner()
    from .novel_spider.spiders import get_all_novel, get_new_novel
    for s in [get_all_novel, get_new_novel]:
        runner.crawl(s)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished


def run6_multiplespider():
    '''通过链接(chaining) deferred来线性运行spider'''
    from twisted.internet import reactor, defer
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.log import configure_logging
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        from .novel_spider.spiders import get_all_novel, get_new_novel
        for s in [get_all_novel, get_new_novel]:
            yield runner.crawl(s)
        reactor.stop()

    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished


if __name__ == '__main__':
    run3_crawlerRunner()
    # run5_multiplespider()
    # run6_multiplespider()