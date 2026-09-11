class Hangman:
    """Class to represent the Hangman game."""
    LIVES = 7

    def __init__(self, word_list:list):
        self.board = {}
        self.word_list = word_list
        self.reset_game()

    def reset_game(self):
        """Reset the game state with a new random word."""
        self.num_lives = self.LIVES
        self.word = choice(self.word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.list_of_guesses = []

    def current_board_index(self):
        """Return the current board stage based on failed attempts."""
        return self.LIVES - self.num_lives

    def load_board(self):
        """Load the the game board."""
        board_dir = Path(__file__).parent
        for i in range(0, self.LIVES + 1):
            file_path = os.path.join(board_dir, f"board_{i}.txt")
            with open(file_path, "r", encoding="utf-8") as f:
                self.board[i] = f.read()
                
    def display_board(self):
        """Display the current state of the game board."""
        print(self.board[self.current_board_index()])
        print(" ".join(self.word_guessed))
        print(f"Lives remaining: {self.num_lives}")
        print(f"Guessed letters: {', '.join(self.list_of_guesses)}")

    def refresh_view(self, message: str | None = None):
        """Render the current terminal state of the game."""


    def game_won(self):
        """Return True when the player has guessed the entire word."""


    def game_lost(self):
        """Return True when the player has no lives left."""


    def check_guess(self, guess:str):
        """Check if the guessed letter is in the word."""


    def submit_guess(self, guess: str):
        """Apply a terminal guess and return the resulting message."""


    def restart_game(self):
        """Restart the terminal game."""


    def play(self):
        """Run the hangman game loop in the terminal."""
        
        
        
