import requests
from bs4 import BeautifulSoup as bs
import json
from pprint import pprint

# https://roscontrol.com/category/produkti/
# grid-padding

url = 'https://roscontrol.com/category/produkti/'
site = 'https://roscontrol.com'
response = requests.get(url)
soup = bs(response.text, 'html.parser')
categories = soup.findAll('div', {
    'class': "grid-padding grid-column-3 grid-column-large-6 grid-flex-mobile grid-column-middle-6 grid-column-small-12 grid-left"})
p = []
for category in categories:
    href = category.find('a', {'class': 'catalog__category-item'})['href']
    response = requests.get(site + href)
    soup = bs(response.text, 'html.parser')
    products = soup.findAll('div', {
        'class': "grid-padding grid-column-3 grid-column-large-6 grid-flex-mobile grid-column-middle-6 grid-column-small-12 grid-left"})
    for product in products:
        href = product.find('a', {'class': 'catalog__category-item'})['href']
        response = requests.get(site + href)
        soup = bs(response.text, 'html.parser')
        i = soup.findAll('div', {'class': 'util-table'})
        for info_product in i:
            info = {}
            name = info_product.find('div', {'class': 'product__item-link'}).text
            try:
                rate = int(info_product.find('div', {'class': 'rate'}).text)
            except:
                rate = None
            qualities = info_product.findAll('div', {'class': 'row'})
            for quality in qualities:
                info[quality.find('div', {'class': "text"}).text] = int(quality.find('div', {'class': 'right'}).text)
            info['Название'] = name.replace('"', '')
            info['Рейтинг'] = rate
            p.append(info)
with open('products.json', 'w') as f:
    json.dump(p, f)
pprint(p)
