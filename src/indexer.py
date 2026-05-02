from bs4 import BeautifulSoup
from crawler import fetch_page
import re

def tokenise(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'meta', 'link']):
        tag.decompose() 
    text = soup.get_text()
    tokens = re.findall(r"\b[a-z]+\b", text.lower())
    return tokens

def build_index(pages):
    index = {}
    for url, html in pages.items():
        tokens = tokenise(html)
        for position, word in enumerate(tokens):
            if word not in index:
                index[word] = {}
            if url not in index[word]:
                index[word][url] = {"frequency": 0, "positions": []}
            index[word][url]["frequency"] += 1
            index[word][url]["positions"].append(position)
    return index

if __name__ == '__main__':
	pages = fetch_page('https://quotes.toscrape.com')
	index = build_index({ 'https://quotes.toscrape.com': pages })
	print(index)