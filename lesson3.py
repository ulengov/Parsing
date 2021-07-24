import pandas as pd
from pymongo import MongoClient

#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, записывающую собранные вакансии в созданную БД.
# я использую файл vacancy.csv, сформированый в прошлом уроке.

def creat_base(mycol,df):

    mycol.drop()

    for index, row in df.iterrows():
        mycol.insert_one(
            {'vacancy_name': row['vacancy_name'],
            'salary_min': row['salary_min'],
            'salary_max': row['salary_max'],
            'salary_currency': row['salary_currency'],
            'vacancy_link': row['vacancy_link'],
            'site': row['site']}
        )
#2 Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы.
# Я не смог использолвать конструкцию {$gte: x} вместо x. Payton ругается

def find_base(mycol, df, x):

    return mycol.find({'salary_min': x})

#3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
# Мне на хватило времени разобратся. Как я понимаю что для нового списка вакнсий надо
# сдеалть поиск в базе и не добавлять если такая запись уже есть

client = MongoClient('localhost', 27017)
mydb = client['test_db']
mycol = mydb['hanter']

df = pd.read_csv('vacancy.csv')

creat_base(mycol,df)

res = find_base(mycol, df, 50000)

for item in res:
    print(item)
