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
    def __init__(self, alpha, color, cell, board):
        """Initialize a worker."""
        self._alpha = alpha
        self._color = color
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
        new_row, new_col = self._cell.row + delta_row, self._cell.col + delta_col
        # Check if the new cell is on the board
        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            return False
        # Check if the new cell is occupied
        if self._board.get_cell(new_row, new_col).worker is not None:
            return False
        # Check if the new cell is too high
        curr_floors = self._cell.height
        new_floors = self._board.get_cell(new_row, new_col).height
        if new_floors - curr_floors > 1:
            return False
        # Check if the new cell is inaccesible
        if self._board.get_cell(new_row, new_col).height == 4:
            return False
        return True

    def validate_build(self, to):
        """Validate the build to the given cell."""
        delta_row, delta_col = DIRECTIONS[to]
        new_row, new_col = self._cell.row + delta_row, self._cell.col + delta_col
        # Check if the new cell is on the board
        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            return False
        # Check if the new cell is occupied
        if self._board.get_cell(new_row, new_col).worker is not None:
            return False
        # Check if the new cell is too high
        if self._board.get_cell(new_row, new_col).height == 4:
            return False
        return True
    
    def __str__(self):
        """Return the string representation of the worker."""
        return self._alpha
    
    

class Player:
    def __init__(self, colour, board):
        """Initialize a player."""
        self._colour = colour # either white or blue
        self._board = board
        self._workers  = None, None
        #self._strategy = None
        if self._colour == "white":
            self._workers = Worker("A", "white", self._board.get_cell(3,1), self._board), Worker("B", "white", self._board.get_cell(1,3), self._board)
        elif self._colour ==  "blue":
            self._workers = Worker("Y", "blue", self._board.get_cell(1,1), self._board), Worker("Z", "blue", self._board.get_cell(3,3), self._board)

    def players_move(self):
        """Determined by the game state and the strategy."""
        pass