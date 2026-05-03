import unittest
import requests
from unittest.mock import patch, MagicMock
from src.crawler import fetch_page, extract_links, normalise_url, crawl

class TestCrawler(unittest.TestCase):
    def test_normalise_url_homepage(self):
        self.assertEqual(normalise_url("https://quotes.toscrape.com/"), "https://quotes.toscrape.com")
        self.assertEqual(normalise_url("https://quotes.toscrape.com"), "https://quotes.toscrape.com")
        self.assertEqual(normalise_url("https://quotes.toscrape.com/page/1"), "https://quotes.toscrape.com")
        self.assertEqual(normalise_url("https://quotes.toscrape.com/page/1/"), "https://quotes.toscrape.com")

    def test_normalise_url_tag_pages(self):
        self.assertEqual(normalise_url("https://quotes.toscrape.com/tag/life/"), "https://quotes.toscrape.com/tag/life")
        self.assertEqual(normalise_url("https://quotes.toscrape.com/tag/inspirational/"), "https://quotes.toscrape.com/tag/inspirational")

    def test_extract_links(self):
        html = '''
				<html>
					<a href="/page/2/">Page 2</a>
					<a href="/tag/life/">Life</a>
					<a href="/login">Login</a>
				</html>
			'''
        links = extract_links(html)
        self.assertIn("https://quotes.toscrape.com/page/2", links)
        self.assertIn("https://quotes.toscrape.com/tag/life", links)
        self.assertIn("https://quotes.toscrape.com/login", links)

    def test_extract_links_ignores_external(self):
        html = '''
        		<html>
                	<a href="https://www.zyte.com/">External</a>
                    <a href="/page/2/">Page 2</a>
				</html>
			'''
        links = extract_links(html)
        self.assertNotIn("https://www.zyte.com/", links)
        self.assertIn("https://quotes.toscrape.com/page/2", links)

    def test_extract_links_empty_html(self):
        links = extract_links("<html></html>")
        self.assertEqual(links, [])

    @patch('src.crawler.requests.get')
    def test_fetch_page_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html>OK</html>'
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        html = fetch_page('https://quotes.toscrape.com')
        self.assertEqual(html, '<html>OK</html>')

    @patch('src.crawler.requests.get')
    def test_fetch_page_raises_on_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.RequestException('404')
        mock_get.return_value = mock_response

        with self.assertRaises(requests.RequestException):
            fetch_page('https://quotes.toscrape.com/notfound')

    @patch('src.crawler.requests.get')
    def test_fetch_page_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        with self.assertRaises(requests.RequestException):
            fetch_page('https://quotes.toscrape.com')

    @patch('src.crawler.time.sleep')
    @patch('src.crawler.fetch_page')
    def test_crawl_returns_pages(self, mock_fetch, mock_sleep):
        mock_fetch.return_value = "<html><body></body></html>"
        pages = crawl()
        self.assertIsInstance(pages, dict)
        self.assertGreater(len(pages), 0)

    @patch('src.crawler.time.sleep')
    @patch('src.crawler.fetch_page')
    def test_crawl_does_not_revisit_pages(self, mock_fetch, mock_sleep):
        mock_fetch.return_value = "<html><body><a href='/'>Home</a></body></html>"
        crawl()
        self.assertEqual(mock_fetch.call_count, 1)

    @patch('src.crawler.time.sleep')
    @patch('src.crawler.fetch_page')
    def test_crawl_skips_failed_pages(self, mock_fetch, mock_sleep):
        mock_fetch.side_effect = requests.RequestException("failed")
        pages = crawl()
        self.assertEqual(pages, {})

    @patch('src.crawler.time.sleep')
    @patch('src.crawler.fetch_page')
    def test_crawl_observes_politeness_window(self, mock_fetch, mock_sleep):
        mock_fetch.return_value = "<html><body><a href='/page/2/'>Next</a></body></html>"
        crawl()
        mock_sleep.assert_called_with(6)

if __name__ == '__main__':
    unittest.main()