from board import Board
from player import Player, HumanPlayer, RandomPlayer, PlayerFactory
from strategy import HumanStrategy
from game import Game
from sys import argv 

class Santorini:
    """Santorini is the driver class for the game.

    It is responsible for initializing the game, executing the game loop,
    and terminating the game.
    """
    def __init__(self, white_type, blue_type, undo_redo, display):
        """Initialize the game."""
        self._board = Board()
        self._players = []
        self._players.append(PlayerFactory().create_player(white_type, "white", self._board))
        self._players.append(PlayerFactory().create_player(blue_type, "blue", self._board))
        self._state = Game(self._board, self._players)
        self._undo_redo = undo_redo
        self._display = display

    def __call__(self):
        while not self._state.game_state_end_check():
            print(self._state)
            self._state._cur_player.player_move(self._state)
        print(self._state)
        print(self._state.winner + " has won")


if __name__ == '__main__':
    try:
        white_type = str(argv[1])
    except IndexError:
        white_type = "human"
    try:
        blue_type = str(argv[2])
    except IndexError:
        blue_type = "human"
    try:
        undo_redo = str(argv[3])
    except IndexError:
        undo_redo = "off"
    try:
        display = str(argv[4])
    except IndexError:
        display = "off"

    newGame = Santorini(white_type, blue_type, undo_redo, display)
    newGame()
    again = input("Play again?\n")
    while again == "yes":
        newGame = Santorini(white_type, blue_type, undo_redo, display)
        newGame()
        again = input("Play again?\n")