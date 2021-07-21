from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

def _parser_item_hh(item):
    vacancy_date = {}

    # vacancy_name
    vacancy_name = item.find('a', {'class': 'bloko-link'}).getText()
    vacancy_date['vacancy_name'] = vacancy_name

    # salary
    salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText()

        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1]+salary[2])
            salary_currency = salary[3]
        elif salary[0] == 'от':
            salary_min = int(salary[1]+salary[2])
            salary_max = None
            salary_currency = salary[3]
        else:
            salary_min = int(salary[0]+salary[1])
            salary_max = int(salary[3]+salary[4])
            salary_currency = salary[5]

    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency

    # link
    vacancy_link = item.find('span', {'class': 'resume-search-item__name'}).find('a')['href']

    vacancy_date['vacancy_link'] = vacancy_link

    # site
    vacancy_date['site'] = 'hh.ru'

    return vacancy_date

def _parser_hh(vacancy,pages):

    vacancy_date = []

    params = {
        'text': vacancy, \
        'search_field': 'name', \
        'items_on_page': '100', \
        'page': ''
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    link = 'https://hh.ru/search/vacancy'

    html = requests.get(link, params=params, headers=headers)

    if html.ok:
        parsed_html = bs(html.text, 'html.parser')

        page_block = parsed_html.find('div', {'data-qa': 'pager-block'})

        if not page_block:
            last_page = 1
        else:
            last_page = int(page_block.find_all('a', {'class': 'bloko-button'})[-2].getText())

        if last_page > pages:
            last_page = pages

        for page in range(0, last_page):
            params['page'] = page
            html = requests.get(link, params=params, headers=headers)

            if html.ok:
                parsed_html = bs(html.text, 'html.parser')

                vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div', {'class': 'vacancy-serp-item'})

                for item in vacancy_items:
                    vacancy_date.append(_parser_item_hh(item))

    return vacancy_date

def _parser_item_superjob(item):
    vacancy_date = {}

    # vacancy_name
    vacancy_name = item.find_all('a')
    vacancy_name = vacancy_name[0].getText()
    vacancy_date['vacancy_name'] = vacancy_name

    # salary
    salary = item.find('span', {'class': '_1h3Zg'})

    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText()

        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1]+salary[2])
            salary_currency = salary[3]
        elif salary[0] == 'от':
            salary_min = int(salary[1]+salary[2])
            salary_max = None
            salary_currency = salary[3]
        elif len(salary) == 6:
            salary_min = int(salary[0]+salary[1])
            salary_max = int(salary[3]+salary[4])
            salary_currency = salary[5]
        else:
            salary_min = None
            salary_max = None
            salary_currency = None

    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency

    # link
    vacancy_link = item.find_all('a')

    if len(vacancy_link) > 1:
        vacancy_link = vacancy_link[-2]['href']
    else:
        vacancy_link = vacancy_link[0]['href']

    vacancy_date['vacancy_link'] = f'https://www.superjob.ru{vacancy_link}'

    # site
    vacancy_date['site'] = 'superjob.ru'

    return vacancy_date


def _parser_superjob(vacancy, pages):
    vacancy_date = []

    params = {
        'keywords': vacancy, \
        'profession_only': '1', \
        'geo[c][0]': '15', \
        'geo[c][1]': '1', \
        'geo[c][2]': '9', \
        'page': ''
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    link = 'https://www.superjob.ru/vacancy/search/'

    html = requests.get(link, params=params, headers=headers)

    if html.ok:
        parsed_html = bs(html.text, 'html.parser')
        page_block = parsed_html.find('a', {'class': 'f-test-button-1'})

        if not page_block:
            last_page = 1
        else:
            page_block = page_block.findParent()
            last_page = int(page_block.find_all('a')[-2].getText())

        if last_page > pages:
            last_page = pages

        for page in range(0, last_page):
            params['page'] = page
            html = requests.get(link, params=params, headers=headers)

            if html.ok:
                parsed_html = bs(html.text, 'html.parser')
                vacancy_items = parsed_html.find_all('div', {'class': 'f-test-vacancy-item'})

                for item in vacancy_items:
                    vacancy_date.append(_parser_item_superjob(item))


    return vacancy_date


def parser_vacancy(vacancy, pages):
    vacancy_date = []
    vacancy_date.extend(_parser_hh(vacancy, pages))
    vacancy_date.extend(_parser_superjob(vacancy, pages))
    df = pd.DataFrame(vacancy_date)
    return df

vacancy = 'Python'
pages = 3
df = parser_vacancy(vacancy, pages)

df.to_csv('vacancy.csv', index=False, encoding='utf-8')


