import requests
from bs4 import BeautifulSoup as BS
from re import sub
from decimal import Decimal


def get_price(url):
    r = requests.get(url)
    html = BS(r.content, 'html.parser')
    price = html.find("div", {"class": "snow-price_SnowPrice__mainM__jlh6el"})
    value = Decimal(sub(r'[^\d.]', '', price.text.replace(',', '.')))
    return value

