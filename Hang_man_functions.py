class HangMan:
    def __init__(self, word_list, num_lives=5):
        self.board = {}
        self.word_list = word_list
        self.num_lives = num_lives
        self.word = choice(self.word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.list_of_guesses = []
 
    def load_board(self):
        for i in range(0,7):
            with open(f"board{i}.txt", "r") as f:
                self.board[i] = f.read()
 
    def display_board(self):
        print(self.board[self.num_lives])
        print("".join(self.word_guessed))
        print(f"Lives left: {self.num_lives}")
        print(f"Guessed letters: {', '.join(self.list_of_guesses)}")
 
 
if __name__ == "__main__":
    word_list = ["python","java","javascript","hangman","programing"]
    hangman_game = HangMan(word_list)
    hangman_game.load_board()
    hangman_game.display_board()