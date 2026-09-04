from Gameboard import Gameboard

def get_players():
    while True:
        modo = input("Choose game mode (1 for vs Computer, 2 for 2 Players): ")
        modo = modo.strip()
        p = int(modo) if mode.isdigit() else None
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
            position = int(input(f"Player {current_player}, enter your move (1-9): "))
            position = int(position) if position_isdigit() else None
        