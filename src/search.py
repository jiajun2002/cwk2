from indexer import load_index

def print_word(index, input):
    words = input.strip().lower().split()  		# Normalise and split the input into words
    if len(words) != 1:
        print("Please only input a single word.")
        return
    
    word = words[0]  							# Take the first word
    if word not in index:
        print(f"'{word}' not found in index.")
        return
    
    result = f"Results for '{word}':\n"
    for url, stats in index[word].items():    	# Iterate through each URL where the word appears, and append its frequency and position
        result += f"  Page: {url}\n"
        result += f"    Frequency: {stats['frequency']}\n"
        result += f"    Positions: {stats['positions']}\n"
    print(result)
    return


def find_word(index, input):
    words = input.strip().lower().split()  		# Normalise and split the input into words
    
    if not words:
        print("No input provided.")
        return
    
    sets = []									# Initialise list of sets to store URLs for each word
    for word in words:
        if word not in index:
            continue
        sets.append(set(index[word].keys()))    # Append the URLs as a set
        
    if not sets:
        print("No results found.")
        return
    
    result = sets[0].intersection(*sets[1:])	# Find intersection of all sets
    print(f"Results for '{input}':")
    for page in sorted(result):                 # Print the URLs in sorted order
        print(f"Page: {page}")
    return

if __name__ == "__main__":
    index = load_index('data/index.json')
    print_word(index, "charles    ")
    find_word(index, "oop")