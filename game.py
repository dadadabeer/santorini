class Game:
    def __init__(self, board, players ):
        self._board = board
        self._players = players
        self._turn_counter = 1
        self._cur_player = self._players[0]
        self.winner = None
    
    @property
    def players(self):
        return self._players
    
    @property
    def turn_counter(self):
        return self._turn_counter
    
    def increment_turn_counter(self):
        self._turn_counter += 1
    
    def set_current_turn(self, turn_count):
        self._current_turn = turn_count

    def change_player(self):
        if self._turn_counter % 2 == 0:
            self._cur_player = self._players[1]
        else:
            self._cur_player = self._players[0]

    def game_state_end_check(self):
        for player in self._players:
            fs_worker, snd_worker = player.workers
            if fs_worker.cell.height == 3 or snd_worker.cell.height == 3:
                self.winner = fs_worker.colour
                return True
            if fs_worker.valid_moves() == [] and fs_worker.valid_moves == []:
                self.winner = "white" if fs_worker.colour == "blue" else "white"
                return True
        return False
    
    def current_game_state(self, withScores=False):
        letters = "AB" if self._cur_player._colour == "white" else "YZ"
        additional_details = "" if not withScores else ", " + self._cur_player.display_score(self)
        details = "Turn: " + str(self._turn_counter) + ", " + self._cur_player._colour + " (" + letters + ")" + additional_details
        return str(self._board) + details
