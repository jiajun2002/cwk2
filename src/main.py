from crawler import crawl
from indexer import build_index, load_index, save_index
from search import print_word, find_word

INDEX_FILEPATH = 'data/index.json'

def main():
	index = {}
	print("\nWelcome to the Quote Search Engine! Type 'build' to begin building the index, or 'help' for a list of commands.")

	while True:
		command = input("Enter command: ").strip().lower()
		if not command:
			continue
		parts = command.split()    				# Split command into parts to separate the command from its arguments
		cmd = parts[0]

		if cmd == "build":
			if len(parts) != 1:
				print("Usage: build (no additional arguments)")
				continue
			else:
				pages = crawl()
				index = build_index(pages)
				save_index(index, INDEX_FILEPATH)
				print("Index saved.")
		
		elif cmd == "load":
			if len(parts) != 1:
				print("Usage: load (no additional arguments)")
				continue
			else:
				try:
					index = load_index(INDEX_FILEPATH)
					print("Index loaded.")
				except FileNotFoundError:
					print("Index file not found. Please build the index first.")

		elif cmd == "print":
			if not index:
				print("Index not loaded. Please build or load the index first.")
				continue
			words = parts[1:]                      # Get list of words after the command
			result = print_word(index, words)      # Call print_word with the list of words, which will handle normalisation and validation
			print(result)

		elif cmd == "find":
			if not index:
				print("Index not loaded. Please build or load the index first.")
				continue
			words = parts[1:]                      # Get list of words after the command
			result = find_word(index, words)       # Call find_word with the list of words, which will handle normalisation and validation
			for url in result:
				print(f"  {url}")

		elif cmd == "help":
			print("Available commands:")
			print("  build - Crawl the website and build the index")
			print("  load - Load the index from file")
			print("  print <word> - Print frequency and positions of a word")
			print("  find <word1> <word2> ... - Find pages containing all specified words")
			print("  exit - Exit the program")

		elif cmd == "exit":
			print("Exiting program.")
			break

		else:
			print("Unknown command.")
			print("Available commands: build, load, print <word>, find <word1> <word2>.")

if __name__ == "__main__":
	main()
		