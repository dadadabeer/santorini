
# COMMAND PATTERN

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

# can break the MoveAndBuild class into Command Interface, Concrete Command Class, Receiver, Invoker
class MoveandBuild:
    def __init__(self, board, selectedWorker, directionMove, directionBuild):
        self._board = board
        self._active_worker = selectedWorker
        self._move_direction = directionMove
        self._build_direction = directionBuild
        self._move_cell = None
        self._build_cell = None

    def move(self):
        """Moves the worker to a new position on the board."""
        currPos = self._active_worker.cell.pos()
        delta_row, delta_col = DIRECTIONS.get(self._move_direction)
        newPos = delta_row + currPos[0], delta_col + currPos[1]
        self._active_worker.cell.worker = None
        self._move_cell = self._board.get_cell(newPos[0], newPos[1])
        self._move_cell.worker = self._active_worker
        self._active_worker.cell = self._move_cell
    
    def build(self):
        """Builds a floor on the corresponding cell."""
        delta_row, delta_col = DIRECTIONS.get(self._build_direction)
        newPos = delta_row + self._move_cell.pos()[0], delta_col + self._move_cell.pos()[1]
        self._build_cell = self._board.get_cell(newPos[0], newPos[1])
        self._build_cell.increase_height()
        print(self._active_worker.alpha + "," + self._move_direction + "," + self._build_direction, end='')
        