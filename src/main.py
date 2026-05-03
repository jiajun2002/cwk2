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
		parts = command.split()
		cmd = parts[0]

		if cmd == "build" and len(parts) == 1:
			pages = crawl()
			index = build_index(pages)
			save_index(index, INDEX_FILEPATH)
			print("Index built and saved.")
		
		elif cmd == "load" and len(parts) == 1:
			try:
				index = load_index(INDEX_FILEPATH)
				print("Index loaded.")
			except FileNotFoundError:
				print("Index file not found. Please build the index first.")

		elif cmd == "print":
			if not index:
				print("Index not loaded. Please build or load the index first.")
				continue
			words = parts[1:]
			result = print_word(index, words)
			print(result)

		elif cmd == "find":
			if not index:
				print("Index not loaded. Please build or load the index first.")
				continue
			words = parts[1:]
			result = find_word(index, words)
			for url in result:
				print(url)

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
			print("Unknown command. Available commands: build, load, print <word>, find <word1> <word2>.")

if __name__ == "__main__":
	main()
		