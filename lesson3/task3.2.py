import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pprint import pprint


def find(x):
    global prod
    return prod.find({"$or": [{'Качество': {"$gte": x}}, {'Rating': {"$gte": x}}]})


client = MongoClient('127.0.0.1', 27017)
db = client['products_base']
prod = db.prod
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
            info['Name'] = name.replace('"', '')
            info['Rating'] = rate
            p.append(info)
            prod.insert_one(info)
            for m in find(50):
                pprint(m)
