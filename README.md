# COMP3011 Search Engine
 
A command-line search engine that crawls [quotes.toscrape.com](https://quotes.toscrape.com/), builds an inverted index, and lets you search for pages containing given words.
 
---
 
## Project Overview
 
| Module | Responsibility |
|--------|----------------|
| `crawler.py` | Fetches pages via HTTP, discovers links, respects a 6-second politeness window |
| `indexer.py` | Parses HTML, tokenises text, builds and persists an inverted index |
| `search.py` | Formats query results from the index for display |
| `main.py` | Interactive command-line shell tying everything together |
 
The **inverted index** maps each lowercase word to a dictionary of page URLs, storing the term frequency and the list of word positions for each page.

Example Index:
```
{
  "love": {
      "https://quotes.toscrape.com/: 
          {"frequency": 3, "positions": [0, 5, 10]},
      "https://quotes.toscrape.com/page/2/": 
          {"frequency": 1, "positions": [2]}
  },
  "good": {
      "https://quotes.toscrape.com/: 
          {"frequency": 1, "positions": [1]}
  }
}
```
 
---
 
## Installation
 
**Requirements:** Python 3.8+
 
```bash
# Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
 
# Install dependencies
pip install -r requirements.txt
```
 
---
 
## Usage
 
Run the shell:
 
```bash
python src/main.py
```
 
### Commands
 
#### 1. `build`
Crawls the website, builds the inverted index, and saves it to `data/index.json`.
 
```
> build
```
 
#### 2. `load`
Loads a previously saved index from `data/index.json` so you don't need to re-crawl.
 
```
> load
```
 
#### 3. `print <word>`
Displays the inverted index entry for a single word, showing every page it appears on, its frequency, and its positions.
 
```
> print love
```

Example output:
```
1 result(s) for 'love':
  Page: https://quotes.toscrape.com
    Frequency: 1
    Positions: [3]
```
 
#### 4. `find <query>`
Returns all pages containing **every** word in the query.
```
> find indifference
> find good friends
```

Example output for `find good friends`:
```
Found 3 page(s) containing all words: good, friends
  https://quotes.toscrape.com
  https://quotes.toscrape.com/author/George-Eliot
  https://quotes.toscrape.com/author/J-K-Rowling
```

#### 5. `help`
Displays available commands and their usage.

#### 6. `exit`
Exits the program.
 
 
---
 
## Testing
 
Run all tests from the project root:
 
```bash
python -m unittest discover -s tests     
```
 
Or run individual test files:
 
```bash
python -m unittest tests/test_crawler.py     
python -m unittest tests/test_indexer.py 
python -m unittest tests/test_search.py 
```
 
---

 
## Design Decisions
 
- **Data structure:** The index is a nested Python dict (`word → urls → {frequency, positions}`), serialised as JSON. This gives O(1) word lookups and is trivially human-readable for debugging.
- **AND semantics for multi-word queries:** `find good friends` returns pages containing both words, implemented via set intersection.
- **Politeness window:** A 6-second `time.sleep()` between requests prevents overloading the target server.