from lxml import html
import requests

header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'}

response = requests.get('https://news.mail.ru/', headers=header)
dom = html.fromstring(response.text)
big_news = dom.xpath('//div[contains(@class, "daynews__item")]')
small_news = dom.xpath('//a[@class="list__text"]')[2:]
news = []
for big_new in big_news:
    n = {}
    article = big_new.xpath(".//span[contains(@class, 'photo__title')]/text()")
    href = big_new.xpath(".//span[contains(@class, 'photo__title')]/../../@href")
    response = requests.get(href[0], headers=header)
    dom = html.fromstring(response.text)
    descr = dom.xpath("//div[@class='article__intro meta-speakable-intro']//text()")[0].replace(r'\xa', '').replace('\xa0', '')
    n['article'] = article[0].replace(r'\xa', '')
    n['href'] = href[0]
    n['description'] = descr
    time = dom.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
    source = dom.xpath('//a[@class="link color_gray breadcrumbs__link"]//text()')
    n['time'] = time[0]
    n['source'] = source[0]
    news.append(n)
for new in small_news:
    n = {}
    response = requests.get(new.xpath("./@href")[0], headers=header)
    dom = html.fromstring(response.text)
    time = dom.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
    source = dom.xpath('//a[@class="link color_gray breadcrumbs__link"]//text()')
    descr = dom.xpath("//div[@class='article__intro meta-speakable-intro']//text()")[0].replace(r'\xa', '').replace(
        '\xa0', '')
    n['description'] = descr
    n['time'] = time[0]
    n['source'] = source[0]
    n['href'] = new.xpath("./@href")[0]
    n['article'] = new.xpath(".//text()")[0].replace(r'\xa', '').replace('\xa0', '')
    news.append(n)
