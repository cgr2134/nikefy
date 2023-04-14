import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def validate_url(url):
    pattern = r'https?://www\.nike.com/.*'
    if not re.match(pattern, url):
        raise ValueError('Invalid URL: Must be a valid Nike.com URL.')


def request_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_nike_products(url):
    validate_url(url)
    soup = request_page(url)
    products_info = []
    products = soup.find_all('div', {'class': 'product-card__body'})
    for product in products:
        name = product.find('div', {'class': 'product-card__title'}).text.strip()
        price = product.find('div', {'class': 'product-price'}).text.strip()
        type = product.find('div', {'class': 'product-card__subtitle'}).text.strip()
        product_url = product.find('a').get('href')
        description = get_product_description(product_url)
        data = {
            'Product Name': name,
            'Price': price,
            'Type': type,
            'Description': description,
            'Product URL': product_url,
        }
        products_info.append(data)
    data = pd.DataFrame(products_info)
    return data


def sort_nike_products(products_info, sort_order='asc'):
    if sort_order == 'asc':
        return products_info.sort_values(
            'Price', ascending=True, key=lambda val: val.str.replace('$', '').astype('float64'), ignore_index=True
        )
    elif sort_order == 'desc':
        return products_info.sort_values(
            'Price', ascending=False, key=lambda val: val.str.replace('$', '').astype('float64'), ignore_index=True
        )
    else:
        raise ValueError('Invalid sort order: Must be "asc" or "desc".')


def get_product_description(product_url):
    validate_url(product_url)
    soup = request_page(product_url)
    description = soup.find('div', {'class': 'description-preview body-2 css-1pbvugb'}).text.strip()
    return description
