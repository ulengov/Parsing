# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from ..items import AvitoAutoItem

class AvitoAutoSpider(scrapy.Spider):

    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://vladivostok.leroymerlin.ru/catalogue/posudomoechnye-mashiny/']

    def parse(self, response: HtmlResponse):

        ad_links = response.css('div.largeCard a::attr(href)')

        for link in ad_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):

        loader = ItemLoader(item=AvitoAutoItem(), response=response)

        loader.add_css('title',
                       'h1.header-2::text')

        loader.add_css('images',
                       'img[alt="product image"]::attr(data-origin)')

        loader.add_css('auto_params', 'div.def-list__group dt::text')

        loader.add_value('url', response.url)

        yield loader.load_item()

