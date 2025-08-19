
import unittest
from unittest.mock import MagicMock, patch
from bs4 import BeautifulSoup
from product_amazon_crawler.functions import find_price, get_links_from_page

class TestOtherFunctions(unittest.TestCase):
	@patch('product_amazon_crawler.functions.WebDriverWait')
	def test_get_links_from_page_no_a_tags(self, mock_wait):
		mock_driver = MagicMock()
		mock_elem = MagicMock()
		mock_elem.find_elements.return_value = []
		mock_wait.return_value.until.return_value = mock_elem
		region_data = MagicMock(navbar_xpath='//div')
		links = get_links_from_page(mock_driver, region_data)
		self.assertFalse(links)

	@patch('product_amazon_crawler.functions.WebDriverWait')
	def test_get_links_from_page_some_none_hrefs(self, mock_wait):
		mock_driver = MagicMock()
		mock_elem = MagicMock()
		mock_a1 = MagicMock()
		mock_a1.get_attribute.return_value = 'http://example.com'
		mock_a2 = MagicMock()
		mock_a2.get_attribute.return_value = None
		mock_elem.find_elements.return_value = [mock_a1, mock_a2]
		mock_wait.return_value.until.return_value = mock_elem
		region_data = MagicMock(navbar_xpath='//div')
		links = get_links_from_page(mock_driver, region_data)
		self.assertEqual(links, ['http://example.com'])
	@patch('product_amazon_crawler.functions.WebDriverWait')
	def test_get_links_from_page_success(self, mock_wait):
		mock_driver = MagicMock()
		mock_elem = MagicMock()
		mock_a = MagicMock()
		mock_a.get_attribute.return_value = 'http://example.com'
		mock_elem.find_elements.return_value = [mock_a]
		mock_wait.return_value.until.return_value = mock_elem
		region_data = MagicMock(navbar_xpath='//div')
		links = get_links_from_page(mock_driver, region_data)
		self.assertEqual(links, ['http://example.com'])

	@patch('product_amazon_crawler.functions.WebDriverWait')
	def test_get_links_from_page_timeout(self, mock_wait):
		mock_driver = MagicMock()
		mock_wait.return_value.until.side_effect = Exception('timeout')
		region_data = MagicMock(navbar_xpath='//div')
		links = get_links_from_page(mock_driver, region_data)
		self.assertFalse(links)

class TestBasicFunctions(unittest.TestCase):
	def test_find_price_with_whitespace(self):
		html = '<span class="a-color-price">   $8.99   </span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup).strip(), "$8.99")

	def test_find_price_with_html_entity(self):
		html = '<span class="a-color-price">&dollar;9.99</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertIn("9.99", find_price(soup))

	def test_find_price_multiple_classes_in_one_span(self):
		html = '<span class="a-color-price a-size-base">$11.99</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup), "$11.99")
	def test_find_price_multiple_spans(self):
		html = '''<div><span class="a-color-price">$1.99</span><span class="a-size-base sc-price">$2.99</span></div>'''
		soup = BeautifulSoup(html, 'lxml')
		# Should return the first matching price (a-color-price)
		self.assertEqual(find_price(soup), "$1.99")

	def test_find_price_nested_spans(self):
		html = '<span class="a-color-price">$3.99<span class="a-size-base sc-price">$4.99</span></span>'
		soup = BeautifulSoup(html, 'lxml')
		# Should return the outer span's text, including inner span
		self.assertIn("$3.99", find_price(soup))

	def test_find_price_empty(self):
		html = ''
		soup = BeautifulSoup(html, 'lxml')
		self.assertIsNone(find_price(soup))

	def test_find_price_malformed_html(self):
		html = '<span class="a-color-price">$7.99'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup), "$7.99")
	def test_find_price_color_price(self):
		html = '<span class="a-color-price">$10.99</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup), "$10.99")

	def test_find_price_size_base(self):
		html = '<span class="a-size-base sc-price">$5.99</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup), "$5.99")

	def test_find_price_color_secondary(self):
		html = '<span class="a-color-secondary">$2.99</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertEqual(find_price(soup), "$2.99")

	def test_find_price_none(self):
		html = '<span class="other-class">No price</span>'
		soup = BeautifulSoup(html, 'lxml')
		self.assertIsNone(find_price(soup))

if __name__ == '__main__':
	unittest.main()

# Create your tests here.
