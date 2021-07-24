from lxml import html
import requests
from datetime import datetime
from pprint import pprint

news = []
keys = ('title', 'date', 'link')

def get_news_lenta_ru():

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}
    link = 'https://lenta.ru/'
    request = requests.get(link, headers=headers)

    root = html.fromstring(request.text)
    root.make_links_absolute(link) #добавляет к ссылкам полный путь

    news_links = root.xpath('//div[@class ="item"]/a/@href')
    news_text = root.xpath('//div[@class ="item"]/a/text()')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//time[@class="g-date"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i],'%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

def get_news_mail_ru():

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'}
    link = 'https://mail.ru/'
    request = requests.get(link, headers=headers)

    root = html.fromstring(request.text)
    root.make_links_absolute(link) #добавляет к ссылкам полный путь

    news_links = root.xpath('//div[@class="news-item svelte-1kcqj27"]/a/@href')
    news_text = root.xpath('//div[@class="news-item svelte-1kcqj27"]/a/text()')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        news_date.extend(date)

    for i in range(len(news_date)):
        news_date[i] = datetime.strptime(news_date[i],'%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'mail.ru'
        news.append(news_dict)

get_news_lenta_ru()
get_news_mail_ru()

pprint(news)




