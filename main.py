from board import Board
from player import Factory
from game import Game
from sys import argv 
from UndoRedo import Caretaker

class Santorini:
    """Santorini is the driver class for the game.

    It is responsible for initializing the game, executing the game loop,
    and terminating the game.
    """
    def __init__(self, white_type, blue_type, undo_redo, display):
        """Initialize the game."""
        self._board = Board()
        self._players = []
        self._players.append(Factory().create_player(white_type, "white", self._board))
        self._players.append(Factory().create_player(blue_type, "blue", self._board))
        self._state = Game(self._board, self._players)
        self._undo_redo = undo_redo
        self._display = True if display == "on" else False
        self._caretaker = Caretaker(self._state)

    def __call__(self):
        while not self._state.game_state_end_check():
            print(self._state.current_game_state(self._display))
            if self._undo_redo == "on":
                chooseMove = input("undo, redo, or next\n") 
            else:
                chooseMove = "next"

            if chooseMove == "next":
                self._state._cur_player.player_move(self._state, self._display)
                self._caretaker.save(self._state)
                
            elif chooseMove == "undo":
                prev_state = self._caretaker.undo()
                if prev_state != None:
                    self._state = prev_state
            elif chooseMove == "redo":
                next_state = self._caretaker.redo()
                if next_state is not None:
                    self._state = next_state
            else:
                continue
            
        print(self._state.current_game_state(self._display))
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
    # again = "yes"
    while again == "yes":
        newGame = Santorini(white_type, blue_type, undo_redo, display)
        newGame()
        again = input("Play again?\n")
        # again = "yes"