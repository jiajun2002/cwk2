# from src.indexer import load_index

def print_word(index, words):
    if len(words) != 1:
        return "Please only input a single word."
    
    word = words[0]  							# Take the first word
    word = word.strip().lower()  # Normalize to lowercase and strip whitespace
    if word not in index:
        return f"'{word}' not found in index."
    
    result = f"Results for '{word}':\n"
    for url, stats in index[word].items():    	# Iterate through each URL where the word appears, and append its frequency and position
        result += f"  Page: {url}\n"
        result += f"    Frequency: {stats['frequency']}\n"
        result += f"    Positions: {stats['positions']}\n"
    return result


def find_word(index, words):
    if not words:
        return ["No input provided."]
    
    sets = []									# Initialise list of sets to store URLs for each word
    norm_words = [w.strip().lower() for w in words]
    for word in norm_words:
        if word not in index:
            return ["No results found."]
        sets.append(set(index[word].keys()))    # Append the URLs as a set
        
    if not sets:
        return ["No results found."]

    result = sets[0].intersection(*sets[1:])	# Find intersection of all sets
    if not result:
            return ["No results found."]
    return sorted(result)						# Return sorted list of URLs

# if __name__ == "__main__":
#     index = load_index('data/index.json')
#     print(print_word(index, "chungus    "))
#     print(find_word(index, "oop"))