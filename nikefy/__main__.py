from .nikefy import *

if __name__ == "__main__":
    url = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'
    nike_products = get_nike_products(url)
    print(nike_products)
    sorted_nike_products = sort_nike_products(nike_products, sort_order='desc')
    print(sorted_nike_products)

