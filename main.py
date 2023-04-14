from Board import Board
from Player import Player
from monopoly import Monopoly

if __name__ == '__main__':
    player_name = input("Player 1: Please Enter Your Name: ")
    player_1 = Player(name=player_name)
    # player_name = input("Player 2: Please Enter Your Name: ")
    player_2 = Player(name="Agent")
    monopoly_game = Monopoly(board=Board.return_board(), players=[player_1, player_2], current_player=0, game_over=False)
    monopoly_game.start_game()

