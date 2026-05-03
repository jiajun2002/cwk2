import os
from bs4 import BeautifulSoup
from crawler import crawl
import json
import re


def tokenise(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'meta', 'link']): 		# Remove non-content tags
        tag.decompose() 
    text = soup.get_text()
    tokens = re.findall(r"\b[a-z]+\b", text.lower()) 			# Extract all words, converting to lowercase
    return tokens


def build_index(pages):
    index = {}
    for url, html in pages.items():    							# Iterate through each crawled page
        tokens = tokenise(html)	
        for position, word in enumerate(tokens):   				# Track position of each word in the page
            if word not in index:                       		# Initialize index entry for new words
                index[word] = {}
            if url not in index[word]:                  		# Initialize index entry for new URLs
                index[word][url] = {"frequency": 0, "positions": []}  
            index[word][url]["frequency"] += 1               	# Increment frequency count for the word in the URL
            index[word][url]["positions"].append(position)   	# Add position to the list of positions for the word in the URL
    return index


def save_index(index, filepath):
	with open(filepath, 'w') as f:      # Save the index as a JSON file
		json.dump(index, f)             


def load_index(filepath):
	if not os.path.exists(filepath):     # Check if the index file exists before trying to load it
		raise FileNotFoundError(f"Index file not found: {filepath}")
	with open(filepath, 'r') as f:       # Load the index from a JSON file
		return json.load(f)
    

if __name__ == '__main__':
    pages = crawl()
    index = build_index(pages)
    save_index(index, 'data/index.json')
    print(index)