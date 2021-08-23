import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint

# https://astrakhan.hh.ru/search/vacancy?clusters=true&area=15&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=
url = 'https://astrakhan.hh.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                         '(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
params = {'clusters': 'true',
          'area': '15',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'salary': '&',
          'st': 'searchVacancy',
          'text': input('Искомая вакансия:')}
response = requests.get(url + 'search/vacancy', headers=headers, params=params)
soup = bs(response.text, 'html.parser')
vacancies = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
v = []
for vacancy in vacancies:
    info = {}
    name = vacancy.find('a').text
    link = vacancy.find('a')['href']
    try:
        price = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        value = price.split(' ')[-1]
        price = price.replace('руб.', '').replace(' ', '').replace('\u202f', '')
        if price[0] == 'о':
            min_price = int(price.replace('от', ''))
            max_price = None
        elif price[0] == 'д':
            min_price = None
            max_price = int(price.replace('до', ''))
        else:
            min_price, max_price = map(int, price.split('–'))
    except AttributeError:
        value = None
        min_price = None
        max_price = None
    info['name'] = name
    info['link'] = link
    info['price'] = [min_price, max_price, value]
    info['site'] = url
    v.append(info)

with open('vacancies.json', 'w') as f:
    json.dump(v, f)
pprint(v)
