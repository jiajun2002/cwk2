import os
from bs4 import BeautifulSoup
import json
import re

# Common noise words that are not useful for searching
STOP = {                                             
    'login', 'next', 'previous',                            # Navigation noise specific to the site
    'a', 'i',                                               # Single letters 
    'the', 'and', 'of', 'to', 'in', 'is', 'it', 'by', 'as'  # Common words with no search value
}

# Extracts text content from HTML, removing non-content tags and tokenising into lowercase words
def tokenise(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'meta', 'link']): 		# Remove non-content tags
        tag.decompose() 

    for a in list(soup.find_all('a')):
        if a.get_text(strip=True).lower() in STOP:
            a.decompose()

    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = re.findall(r'\b[a-z]+\b', text.lower())
    return [t for t in tokens if t not in STOP]


# Builds an inverted index, tracking frequency and positions of each word in each URL
def build_index(pages):
    if not pages:
        print("No pages to index.")
        return {}
    index = {}
    print("Building index...")
    for url, html in pages.items():    							# Iterate through each crawled page
        tokens = tokenise(html)	
        for position, word in enumerate(tokens):   				# Track position of each word in the page
            if word not in index:                       		# Initialize index entry for new words
                index[word] = {}
            if url not in index[word]:                  		# Initialize index entry for new URLs for word
                index[word][url] = {"frequency": 0, "positions": []}  
            index[word][url]["frequency"] += 1               	# Increment frequency for the word in the URL
            index[word][url]["positions"].append(position)   	# Add position to the list for the word in the URL
    print("Index built.")
    return index


def save_index(index, filepath):
    dirpath = os.path.dirname(filepath)         
    if dirpath and not os.path.exists(dirpath):  # Create the directory if it doesn't exist
        os.makedirs(dirpath)
    with open(filepath, 'w') as f:               # Save the index as a JSON file
        json.dump(index, f, indent=2)


def load_index(filepath):
	if not os.path.exists(filepath):             # Check if the index file exists before trying to load it
		raise FileNotFoundError(f"Index file not found: {filepath}")
	with open(filepath, 'r') as f:               # Load the index from a JSON file
		return json.load(f)
    