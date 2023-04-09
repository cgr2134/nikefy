from nikefy import *
from unittest.mock import patch, mock_open, Mock, call
import unittest


class TestNikefy(unittest.TestCase):

    def test_validate_url_valid(self):
        url = 'https://www.nike.com/'
        self.assertIsNone(validate_url(url))

    def test_validate_url_invalid(self):
        url = 'https://www.adidas.com/'
        with self.assertRaises(ValueError):
            validate_url(url)

    def test_sort_nike_products_asc(self):
        products_info = pd.DataFrame({'Product Name': ['Nike Alphafly 2', 'Nike Vaporfly 3', 'Jordan Retro 6 G NRG'],
                                      'Price': ['$275', '$250', '$220']})
        expected_output = pd.DataFrame({'Product Name': ['Jordan Retro 6 G NRG', 'Nike Vaporfly 3', 'Nike Alphafly 2'],
                                      'Price': ['$220', '$250', '$275']})
        self.assertTrue(expected_output.equals(sort_nike_products(products_info, 'asc')))

    def test_sort_nike_products_desc(self):
        products_info = pd.DataFrame({'Product Name': ['Nike Air Max 270', 'Nike Air Max 95', "Nike Air Force 1 '07"],
                                      'Price': ['$160', '$175', '$110']})
        expected_output = pd.DataFrame({'Product Name': ['Nike Air Max 95', 'Nike Air Max 270', "Nike Air Force 1 '07"],
                                         'Price': ['$175', '$160', '$110']})
        print((sort_nike_products(products_info, 'desc')))
        self.assertTrue(expected_output.equals(sort_nike_products(products_info, 'desc')))

    def test_sort_nike_products_invalid_order(self):
        products_info = pd.DataFrame({'Product Name': ['Nike Air Max 270', 'Nike Air Max 95', "Nike Air Force 1 '07"],
                                      'Price': ['$160', '$175', '$110']})
        with self.assertRaises(ValueError):
            sort_nike_products(products_info, 'invalid')

    def test_get_product_description(self):
        with patch('nikefy.request_page') as mock_request_page:
            mock_request_page.return_value = BeautifulSoup('<div class="description-preview body-2 '
                                                           'css-1pbvugb"><p>Once you take a few strides in the Nike '
                                                           'Air Zoom Alphafly NEXT% 2, you’ll never look at your '
                                                           'favorite pair of old racing shoes the same way again. '
                                                           'These rocket ships are made to help shave precious time '
                                                           'off your personal records without surrendering the '
                                                           'foundation you need to go the full distance. A thick, '
                                                           'lightweight support system marries the 2 worlds of '
                                                           'comfort and speed in holy running matrimony. Enjoy the '
                                                           'greatest energy return of all our racing shoes while you '
                                                           'chase your personal bests.</p></div>', 'html.parser')
            description = get_product_description('https://www.nike.com/t/alphafly-2-mens-road-racing-shoes-8lD0jN'
                                                  '/DN3555-600')
            self.assertEqual(description, 'Once you take a few strides in the Nike Air Zoom Alphafly NEXT% 2, you’ll '
                                          'never look at your favorite pair of old racing shoes the same way again. '
                                          'These rocket ships are made to help shave precious time off your personal '
                                          'records without surrendering the foundation you need to go the full '
                                          'distance. A thick, lightweight support system marries the 2 worlds of '
                                          'comfort and speed in holy running matrimony. Enjoy the greatest energy '
                                          'return of all our racing shoes while you chase your personal bests.Shown: '
                                          'Hyper Pink/Laser Orange/White/BlackStyle: DN3555-600')

    def test_get_nike_products_integration(self):
        url = 'https://www.nike.com/w/mens-shoes-nik1zy7ok'
        data = get_nike_products(url)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()
