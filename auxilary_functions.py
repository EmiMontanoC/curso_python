
def load_book(file_path: str) -> list:
    """Load words from a file and return them as a list."""
    with open(file_path, "r", encoding="utf-8") as f:
        words = f.read().split()
    return words


def clean_list_of_words(word_list:list) -> list:
    """Clean a list of words by removing punctuation and converting to lowercase."""
    cleaned_words = []
    for word in word_list:
        word = word.lower().strip(".,!?;:\"'()[]{}1234567890")
        print(word)
        cleaned_words.append(word)
    return cleaned_words

if __name__ == "__main__":
    book_path = "Dracula.txt"
    words = load_book(book_path)
    words = clean_list_of_words(words)
    print(len(words))
    print(len(words[0]))
    print(words[0])
    print(words[0:100])
    print(words[:20])
    cleaned_words=clean_list_of_words(words)
