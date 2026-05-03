import requests
import time
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com"

# Fetches HTML content of a page
def fetch_page(url):
    try:
        response = requests.get(url) 	# Make a GET request to the URL
        response.raise_for_status() 	# Check if the request was successful (status code 200)
        return response.text 			# Return the HTML content of the page
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        raise


def normalise_url(url):
	url = url.rstrip('/') 								# Remove trailing slash from the URL
	if url == "https://quotes.toscrape.com/page/1": 	# Normalise first page URL to the base URL
		url = "https://quotes.toscrape.com"
	return url


# Extracts all valid links from the HTML content
def extract_links(html):
	soup = BeautifulSoup(html, 'html.parser')
	links = []
	for tag in soup.find_all('a', href=True): 	# Find all anchor tags with an href
		href = tag['href']
		if href.startswith('/'): 				# Only consider relative links that start with '/'
			link = URL + href 					# Construct the full URL
			link = normalise_url(link)			# Normalise URL
			links.append(link) 					# Add the full URL to the list of links
	return links


# Main crawling function that uses BFS to traverse website
def crawl():
	visited = set() 								# Set to keep track of visited URLs to avoid duplicates
	to_visit = [URL]
	pages = {}										# Dictionary to store crawled pages with URL: HTML content as key-value pairs

	while to_visit: 								# BFS loop to crawl through URLs
		url = to_visit.pop(0)
		if url in visited:
			continue
		
		try:
			html = fetch_page(url)
			pages[url] = html
			print(f"Crawled: {url}")
			links = extract_links(html)
			to_visit.extend(links) 					# Add new links to the queue
			visited.add(url)
		except Exception as e:
			print(f"Error crawling {url}: {e}")

		if to_visit:
			time.sleep(0.2) # Sleep for 0.2 seconds between requests (testing)
			# time.sleep(6) # Sleep for 6 seconds between requests

	return pages


# if __name__ == '__main__':
# 	crawled_pages = crawl()
# 	print(f"Total pages crawled: {len(crawled_pages)}")
