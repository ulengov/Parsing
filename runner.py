from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from job_parser import settings
from job_parser.spiders.hh_ru import HhRuSpider
from job_parser.spiders.superjob import SuperjobRuSpider

if __name__ == '__main__':
    vacancy = 'менеджер'

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(HhRuSpider, vacancy=vacancy)
    process.crawl(SuperjobRuSpider, vacancy=vacancy)

    process.start()
