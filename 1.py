# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json

username = 'ulengov'
req = requests.get('https://api.github.com/users/'+username+'/repos')

data = req.json()
for i in range(0,len(data)):
  print("Project Number:",i+1)
  print("Project Name:",data[i]['name'])
  print("Project URL:",data[i]['svn_url'],"\n")

with open('data1.json', 'w') as f:
  json.dump(data, f, ensure_ascii=False)

