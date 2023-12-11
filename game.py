from board import Board
from player import Player

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

    def game_state(self):
        pass
    
    def __str__(self):
        #details = "Turn: " + {self._turn_counter} + ", " {self._current_player.colour}
        return str(self._board)


# board = Board()
# player1 = Player("white", board)
# player2 = Player("blue", board)
# testGameState = Game(board, [player1, player2])

# print(testGameState)
    
    


        