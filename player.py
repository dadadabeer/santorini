from strategy import HumanStrategy, Context, RandomStrategy, HeuristicStrategy

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

class Worker:
    def __init__(self, alpha, colour, cell, board):
        """Initialize a worker."""
        self._alpha = alpha
        self.colour = colour
        self._cell = cell
        self._board = board
        self._cell.worker = self

    @property
    def alpha(self):
        """Return the alpha of the worker."""
        return self._alpha
    
    @property
    def cell(self):
        """Return the cell the worker is on."""
        return self._cell
    
    @cell.setter
    def cell(self, cell):
        """Set the cell the worker is on."""
        self._cell = cell
    
    def validate_move(self, to):
        """Validate the move to the given cell."""
        delta_row, delta_col = DIRECTIONS[to]
        new_row, new_col = self._cell._row + delta_row, self._cell._col + delta_col
        
        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            return False
        
        if self._board.get_cell(new_row, new_col).worker is not None:
            return False
        
        curr_floors = self._cell.height
        new_floors = self._board.get_cell(new_row, new_col).height
        if new_floors - curr_floors > 1:
            return False

        if self._board.get_cell(new_row, new_col).height == 4:
            return False
        return True

    def validate_build(self, moveto, buildto):
        """Validate the build to the given cell (also depends on the move direction)."""
        delta_row_move, delta_col_move = DIRECTIONS[moveto]
        delta_row_build, delta_col_build = DIRECTIONS[buildto]
        new_row, new_col = self._cell._row + delta_row_move + delta_row_build, self._cell._col + delta_col_move + delta_col_build

        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            return False

        if self._board.get_cell(new_row, new_col).worker is not None:
            if (new_row, new_col) != self._cell.pos():
                return False

        if self._board.get_cell(new_row, new_col).height == 4:
            return False
        return True
    
    def valid_moves(self):
        """Return a list of valid moves for the worker."""
        all_directions = DIRECTIONS.keys()
        valid_moves = []
        for dir in all_directions:
            if self.validate_move(dir):
                valid_moves.append(dir)
        return valid_moves

    def valid_builds(self, moveto):
        """Return a list of valid builds for the worker given a move direction."""
        all_directions = DIRECTIONS.keys()
        valid_builds = []
        for dir in all_directions:
            if self.validate_build(moveto, dir):
                valid_builds.append(dir)
        return valid_builds
        
    
    def __str__(self):
        """Return the string representation of the worker."""
        return self._alpha
    
    

class Player:
    def __init__(self, board, colour):
        """Initialize a player."""
        self._board = board
        self._colour = colour
        self._workers  = None, None
        self._strategy_type = None
        if self._colour == "white":
            self._workers = Worker("A", "white", self._board.get_cell(3,1), self._board), Worker("B", "white", self._board.get_cell(1,3), self._board)
        elif self._colour ==  "blue":
            self._workers = Worker("Y", "blue", self._board.get_cell(1,1), self._board), Worker("Z", "blue", self._board.get_cell(3,3), self._board)

    def player_move(self, game, display):
        """Determined by the game state and the strategy."""
        move_and_build_request = self._strategy_type.context_interface(game)
        move_and_build_request.move()
        move_and_build_request.build()
        if display:
            print(" " + self.display_score(game))
        else:
            print()
        game.increment_turn_counter()
        game.change_player()

    @property
    def workers(self):
        return self._workers
    
    def height_score(self):
        return self._workers[0].cell.height + self._workers[1].cell.height
    
    def center_score(self):
        center_score = 0
        for worker in self._workers:
            row, col = worker.cell.pos()
            if (row, col) == (2, 2):
                center_score += 2
            elif 1 <= row <= 3 and 1 <= col <= 3:
                center_score += 1
        return center_score
    
    def distance_score(self, players):
        def chebyshev_distance(cell1, cell2):
            row1, col1 = cell1.pos()
            row2, col2 = cell2.pos()
            return max(abs(row1 - row2), abs(col1 - col2))

        player1, player2 = players[0], players[1]
        worker_A_loc = player1.workers[0].cell
        worker_B_loc = player1.workers[1].cell
        worker_Y_loc = player2.workers[0].cell
        worker_Z_loc = player2.workers[1].cell

        Z_to_A = chebyshev_distance(worker_Z_loc, worker_A_loc)
        Y_to_A = chebyshev_distance(worker_Y_loc, worker_A_loc)
        Z_to_B = chebyshev_distance(worker_Z_loc, worker_B_loc)
        Y_to_B = chebyshev_distance(worker_Y_loc, worker_B_loc)

        for_blue = min(Z_to_A, Y_to_A) + min(Z_to_B, Y_to_B)
        for_white = min(Z_to_A, Z_to_B) + min(Y_to_A, Y_to_B)

        if self._colour == "white":
            return 8 - for_white
        return 8 - for_blue
    
    def display_score(self, game):
        return f"({self.height_score()}, {self.center_score()}, {self.distance_score(game.players)})"
            
        
class HumanPlayer(Player):
    def __init__(self, board, colour):
        super().__init__(board, colour)
        self._strategy_type = Context(HumanStrategy(self._board, self._workers))

class RandomPlayer(Player):
    def __init__(self, board, colour):
        super().__init__(board, colour)
        self._strategy_type = Context(RandomStrategy(self._board, self._workers))

class HeuristicPlayer(Player):
    def __init__(self, board, colour):
        super().__init__(board, colour)
        self._strategy_type = Context(HeuristicStrategy(self._board, self._workers))
    
class FactoryofPlayers():
    def initiate_player(self, board, colour, player_type):
        if player_type == "human":
            return HumanPlayer(board, colour)
        if player_type == "random":
            return RandomPlayer(board, colour)
        if player_type == "heuristic":
            return HeuristicPlayer(board, colour)
