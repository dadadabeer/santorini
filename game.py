from board import Board
from player import Worker, Player
from strategy import HumanStrategy, MoveandBuild
DIRECTIONS = {
    'n': (-1, 0),
    'ne': (-1, 1),
    'nw': (-1, -1),
    's': (1, 0),
    'se': (1, 1),
    'sw': (1, -1),
    'e': (0, 1),
    'w': (0, -1)
}
class Game:
    def __init__(self, board, players ):
        self._board = board
        self._players = players
        self._turn_counter = 1
        self._cur_player = self._players[0]
        self.winner = None
    
    @property
    def turn_counter(self):
        return self._turn_counter
    
    def increment_turn_counter(self):
        self._turn_counter += 1

    def change_player(self):
        if self._turn_counter % 2 == 0:
            self._cur_player = self._players[1]
        else:
            self._cur_player = self._players[0]

    def game_state_end_check(self):
        # make a getter for workers later
        for player in self._players:
            fs_worker, snd_worker = player._workers
            if fs_worker.cell.height == 3 or snd_worker.cell.height == 3:
                self.winner = fs_worker.colour
                return True
            if fs_worker.valid_moves() == [] and fs_worker.valid_moves == []:
                self.winner = "white" if fs_worker.colour == "blue" else "white"
                return True
        return False
    
    def __str__(self):
        letters = "AB" if self._cur_player._colour == "white" else "YZ"
        details = "Turn: " + str(self._turn_counter) + ", " + self._cur_player._colour + " (" + letters + ")"
        return str(self._board) + details

