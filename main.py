from board import Board
from player import Player
from strategy import HumanStrategy
from game import Game

class Santorini:
    """Santorini is the driver class for the game.

    It is responsible for initializing the game, executing the game loop,
    and terminating the game.
    """
    def __init__(self):
        """Initialize the game."""
        self._board = Board()
        self._players = []
        self._players.append(Player("white", self._board))
        self._players.append(Player("blue", self._board))
        self._state = Game(self._board, self._players)

    def __call__(self):
        while not self._state.game_state_end_check():
            print(self._state)
            self._state._cur_player.player_move(self._state)
        print(self._state._cur_player._colour + " has won")

        

# #Turn: 22, blue (YZ)
# white has won
# Play again?
# no

if __name__ == '__main__':
    newGame = Santorini()
    newGame()
    again = input("Play again?\n")
    while again == "yes":
        newGame = Santorini()
        newGame()
        again = input("Play again?\n")