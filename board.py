class Cell:
    """Cell of a board for Santorini game."""
    def __init__(self, row, col):
        """Initialize a cell."""
        self._row = row
        self._col = col
        self._height = 0
        self._worker = None

    @property
    def height(self):
        """Return the height of the cell."""
        return self._height

    def increase_height(self):
        """Change the height of the cell."""
        if self._height < 4:
            self._height += 1
    
    @property
    def worker(self):
        """Return the worker on the cell."""
        return self._worker
    
    @worker.setter
    def worker(self, worker):
        """Set the worker on the cell."""
        self._worker = worker

    def pos(self):
        return (self._row, self._col)
    
    def __str__(self):
        """String representation of the cell."""
        worker_repr = self._worker if self._worker else ' '
        return f"{self._height}{worker_repr}"

class Board:
    """Board class for Santorini game."""
    def __init__(self):
        """Initialize the board."""
        self._board = [[0 for _ in range(5)] for _ in range(5)]
        for row in range(5):
            for col in range(5):
                self._board[row][col] = Cell(row, col)
    
    def get_cell(self, row, col):
        """Return the cell at the given row and column."""
        return self._board[row][col]
    
    def __str__(self):
        """Return a string representation of the board."""
        representation = '+--+--+--+--+--+\n'
        for row in self._board:
            representation += '|'
            for cell in row:
                representation += str(cell) + '|'
            representation += '\n'
            representation += '+--+--+--+--+--+\n'
        return representation