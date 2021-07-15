# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл

import requests
import json

username = 'ulengov'
token = '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'

req = requests.get('https://api.github.com/user', auth=(username, token))

data = req.json()

with open('data2.json', 'w') as f:
  json.dump(data, f, ensure_ascii=False)
