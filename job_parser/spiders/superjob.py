# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import HtmlResponse
from ..items import JobParserItem

class SuperjobRuSpider(scrapy.Spider):
    name = 'superjob_ru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacancy=None):
        super(SuperjobRuSpider, self).__init__()
        self.start_urls = [
            f'https://www.superjob.ru/vacancy/search/?keywords={vacancy}'
        ]

    def parse(self, response):
        next_page = response.css('a[class*=f-test-button-dalshe][href^="/vakansii"]::attr(href)').extract_first()

        yield response.follow(next_page, callback=self.parse)

        vacancy_items  = response.css('div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        name = response.css('h1 ::text').extract_first()

        salary = response.css('div._3MVeX span._1OuF_ span._1h3Zg::text').extract()
#        salary = [item.replace(u'\xa0', u' ') for item in salary]

        salary = ' '.join(salary)
        salary = salary.replace(u'\xa0', u' ')
        salary = salary.replace(u'  ', u' ')
        salary = salary.replace(u'  ', u' ')
        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1]+salary[2])
            salary_currency = salary[3]
        elif salary[0] == 'от':
            salary_min = int(salary[1]+salary[2])
            salary_max = None
            salary_currency = salary[3]
        elif salary[0] != 'По':
            if salary[3] == 'месяц':
                salary_min = int(salary[0] + salary[1])
                salary_max = int(salary[0] + salary[1])
                salary_currency = salary[2]
            else:
                salary_min = int(salary[0] + salary[1])
                salary_max = int(salary[2] + salary[3])
                salary_currency = salary[4]
        else:
            salary_min = None
            salary_max = None
            salary_currency = None

        salary= [salary_min, salary_max, salary_currency]

        vacancy_link = response.url

        site_scraping = self.allowed_domains[0]

        yield JobParserItem(
            name=name, \
            salary=salary, \
            vacancy_link=vacancy_link, \
            site_scraping=site_scraping
        )