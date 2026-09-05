from Gameboard import Gameboard

def get_players():
    while True:
        modo = input("Choose game mode (1 for vs Computer, 2 for 2 Players): ")
        modo = modo.strip()
        p = int(modo) if modo.isdigit() else None
        if p in [1, 2]:
            return p
        else:
            print("Invalid input. Please enter 1 or 2.")
        
    
    

def main():
    gameboard = Gameboard()
    player = get_players()
    current_player = "X"
    while True:
        gameboard.display_board()
        if player == 1 and current_player == "O":
            message = gameboard.computer_move(current_player)
        else:
            position = input(f"Player {current_player}, enter your move (1-9): ")
            position = int(position) if position.isdigit() else None
        if position not in range(1,10):
            print("Invalid position. Please enter a number between 1 and 9.")
            continue
        message = gameboard.player_move(current_player, position)
        print(message)
        winner = gameboard.check_winner()
        
        if winner:
            gameboard.display_board()
            status = {"X": "Player X wins!","O": "Player O wins!","-": "It's a draw!"}
            print(status[winner])
            gameboard.update_scoreboard(winner)
            print(f"Scoreboard: {gameboard.scoreboard}")
            continue_playing = input("Do you want to play again? (y/n): ")
            
            gameboard.reset_board()
            break
        current_player = "O" if current_player == "X" else "X"
if __name__ == "__main__":
    main()