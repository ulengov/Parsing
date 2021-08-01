# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class JobParserPipeline(object):

    def __init__(self):

        client =  MongoClient('localhost', 27017)
        mybase = client['vacancy_db']
        self.mycoll = mybase['hanter']

    def process_item(self, item, spider):

        vacancy_name = item['name']
        salary_min = item['salary'][0]
        salary_max = item['salary'][1]
        salary_currency = item['salary'][2]
        vacancy_link = item['vacancy_link']
        site_scraping = item['site_scraping']

        vacancy_json = {
            'vacancy_name': vacancy_name, \
            'salary_min': salary_min, \
            'salary_max': salary_max, \
            'salary_currency': salary_currency, \
            'vacancy_link': vacancy_link, \
            'site_scraping': site_scraping
        }

        self.mycoll.insert_one(vacancy_json)
        return vacancy_json

#class JobParserPipeline:
#    def process_item(self, item, spider):
#        return item
