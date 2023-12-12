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
        fs_worker, snd_worker = self._cur_player._workers
        if fs_worker.cell.height == 3 or snd_worker.cell.height == 3:
            return True
        all_directions = DIRECTIONS.keys()
        valid_moves = False
        for worker in (fs_worker, snd_worker):
            for dir in all_directions:
                if worker.validate_move(dir):
                    valid_moves = True
                    break
                else:
                    continue
            if valid_moves:
                break
        if not valid_moves:
            self.change_player()
            return True
        return False
    
    def __str__(self):
        letters = "AB" if self._cur_player._colour == "white" else "YZ"
        details = "Turn: " + str(self._turn_counter) + ", " + self._cur_player._colour + " (" + letters + ")"
        return str(self._board) + details

