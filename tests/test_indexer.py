import os
import unittest
from src.indexer import tokenise, build_index, save_index, load_index

class TestIndexer(unittest.TestCase):
    def test_tokenise(self):
        html = "<html><body><span>Hello, world!</span><script>var x=1;</script></body></html>"
        tokens = tokenise(html)
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertNotIn("var", tokens)

    def test_tokenise_filters_stopwords(self):
        html = "<p>the quick login next previous and fox</p>"
        tokens = tokenise(html)
        self.assertNotIn('the', tokens)
        self.assertNotIn('login', tokens)
        self.assertNotIn('next', tokens)
        self.assertIn('quick', tokens)
        self.assertIn('fox', tokens)

    def test_tokenise_empty_html(self):
        tokens = tokenise("<html></html>")
        self.assertEqual(tokens, [])

    def test_build_index_contains_word(self):
        pages = {"https://quotes.toscrape.com": "<span class='text' itemprop='text'>“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>"}
        index = build_index(pages)
        self.assertIn("world", index)
        self.assertNotIn("span", index)

    def test_build_index_frequency(self):
        pages = {"https://quotes.toscrape.com": "<span class='text' itemprop='text'>“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>}"}
        index = build_index(pages)
        frequency = index["thinking"]["https://quotes.toscrape.com"]["frequency"]
        self.assertEqual(frequency, 2)

    def test_build_index_positions(self):
        pages = {"https://quotes.toscrape.com": "<span class='text' itemprop='text'> The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>}"}
        index = build_index(pages)
        positions = index["thinking"]["https://quotes.toscrape.com"]["positions"]
        self.assertEqual(positions, [6, 13])

    def test_build_index_multiple_pages(self):
        pages = {
            "https://quotes.toscrape.com": "<span class='text' itemprop='text'>“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>",
            "https://quotes.toscrape.com/page/2/": "<span class='text' itemprop='text'>“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”</span>"
        }
        index = build_index(pages)
        self.assertIn("https://quotes.toscrape.com", index["thinking"])
        self.assertIn("https://quotes.toscrape.com/page/2/", index["thinking"])

    def test_save_and_load_index(self):
        test_index = {"foo": {"bar": {"frequency": 1, "positions": [0]}}}
        test_path = "data/test_index.json"
        save_index(test_index, test_path)
        loaded = load_index(test_path)
        self.assertEqual(test_index, loaded)
        os.remove(test_path)

if __name__ == "__main__":
    unittest.main()