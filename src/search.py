
# Prints frequency and position of a single word in the index
def print_word(index, words):
    if len(words) != 1:
        return "Please only input a single word."
    
    word = words[0]  							# Take the first word
    word = word.strip().lower()                 # Normalize to lowercase and strip whitespace
    if word not in index:
        return f"'{word}' not found in index."
    
    pageCount = len(index[word])					# Get the number of pages containing the word
    result = f"{pageCount} result(s) for '{word}':\n"
    for url, stats in index[word].items():    	    # Iterate through each URL where the word appears, and append its frequency and position
        result += f"  Page: {url}\n"
        result += f"    Frequency: {stats['frequency']}\n"
        result += f"    Positions: {stats['positions']}\n"
    return result


# Finds pages containing all input words
def find_word(index, words):
    if not words:
        return ["No input provided."]
    
    sets = []									    # Initialise list of sets to store URLs for each word
    norm_words = [w.strip().lower() for w in words] # Normalise input words to lowercase and strip whitespace
    for word in norm_words:
        if word not in index:
            return ["No results found."]            # If any word is not in the index, return no results immediately
        sets.append(set(index[word].keys()))        # Append the URLs with the word as a set
      
    if not sets:
        return ["No results found."]                # If no valid words were found, return no results   
    result = sets[0].intersection(*sets[1:])	    # Find intersection of all sets
    if not result:
        return ["No results found."]
    print(f"Found {len(result)} page(s) containing all words: {', '.join(norm_words)}") 
    return sorted(result)						    # Return sorted list of URLs
