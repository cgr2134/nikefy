import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url(url):
    return requests.get(url)
    
def get_html_parser(response):
    return BeautifulSoup(response.content, 'html.parser')

def get_product_info(url):
    response = get_url(url)
    soup = get_html_parser(response)

    product_info = []
    products = soup.find_all('div', {'class': 'product-card__body'})
     
    for product in products:
        name = product.find('div', {'class': 'product-card__title'}).text.strip()
        price = product.find('div', {'class': 'product-price'}).text.strip()
        product_info.append({'Product Name': name, 'Price': price})

    data = pd.DataFrame(product_info)
    
    return data
    

