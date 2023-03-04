import requests
from bs4 import BeautifulSoup

def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_info = []
    products = soup.find_all('div', {'class': 'product-card__body'})
    
    for product in products:
        name = product.find('div', {'class': 'product-card__title'}).text.strip()
        price = product.find('div', {'class': 'product-price'}).text.strip()
        product_info.append({'name': name, 'price': price})

    return product_info

