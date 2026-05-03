import unittest
from src.search import print_word, find_word

# test index 
MOCK_INDEX = {
    "love": {
        "https://quotes.toscrape.com/": {"frequency": 3, "positions": [0, 5, 10]},
        "https://quotes.toscrape.com/page/2/": {"frequency": 1, "positions": [2]}
    },
    "world": {
        "https://quotes.toscrape.com/": {"frequency": 1, "positions": [1]}
    }
}


class TestSearch(unittest.TestCase):
    def test_print_word_known_word_returns_result(self):
        result = print_word(MOCK_INDEX, ["love"])
        self.assertIn("love", result)
        self.assertIn("https://quotes.toscrape.com/", result)

    def test_print_word_unknown_word_returns_not_found(self):
        result = print_word(MOCK_INDEX, ["zzzzz"])
        self.assertIn("not found", result)

    def test_print_word_empty_input_returns_error(self):
        result = print_word(MOCK_INDEX, [])
        self.assertIn("single word", result)

    def test_print_word_case_insensitive(self):
        result_lower = print_word(MOCK_INDEX, ["love"])
        result_upper = print_word(MOCK_INDEX, ["LOVE"])
        self.assertEqual(result_lower, result_upper)

    def test_print_word_multiple_words_returns_error(self):
        result = print_word(MOCK_INDEX, ["love", "world"])
        self.assertIn("single word", result)

    def test_print_word_extra_whitespace_handled(self):
        result = print_word(MOCK_INDEX, ["  love  "])
        self.assertIn("love", result)

    def test_find_word_single_word_returns_pages(self):
        result = find_word(MOCK_INDEX, ["love"])
        self.assertIn("https://quotes.toscrape.com/", result)

    def test_find_word_multi_word_intersection(self):
        result = find_word(MOCK_INDEX, ["love", "world"])
        self.assertIn("https://quotes.toscrape.com/", result)
        self.assertNotIn("https://quotes.toscrape.com/page/2/", result)

    def test_find_word_unknown_word_returns_no_results(self):
        result = find_word(MOCK_INDEX, ["zzzzz"])
        self.assertEqual(result, ["No results found."])

    def test_find_word_empty_input_returns_no_input(self):
        result = find_word(MOCK_INDEX, [])
        self.assertEqual(result, ["No input provided."])

    def test_find_word_case_insensitive(self):
        result_lower = find_word(MOCK_INDEX, ["love"])
        result_upper = find_word(MOCK_INDEX, ["LOVE"])
        self.assertEqual(result_lower, result_upper)


if __name__ == "__main__":
    unittest.main()