# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import HtmlResponse
from ..items import JobParserItem

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']

    def __init__(self, vacancy=None):
        super(HhRuSpider, self).__init__()
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={vacancy}'
        ]

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.bloko-button::attr(href)').extract()[-1]

        yield response.follow(next_page, callback=self.parse)

        vacancy_items  = response.css(
            'div.vacancy-serp \
            div.vacancy-serp-item \
            div.vacancy-serp-item__row_header \
            a.bloko-link::attr(href)'
        ).extract()

        for vacancy_link in vacancy_items:
            yield response.follow(vacancy_link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):

        name = response.css('div.vacancy-title h1.bloko-header-1::text').extract_first()

        salary = response.css('div.vacancy-title p.vacancy-salary span.bloko-header-2::text').extract_first()

        if salary != '':
            salary = salary.replace(u'\xa0', u' ')
            salary = re.split(r'\s|-', salary)
        else:
            salary = ['*']

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1]+salary[2])
            salary_currency = salary[3]
        elif salary[0] == 'от':
            salary_min = int(salary[1]+salary[2])
            if salary[3] == 'до':
                salary_max = int(salary[4] + salary[5])
                salary_currency = salary[6]
            else:
                salary_max = None
                salary_currency = salary[3]
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
