from board import Board

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

class HumanStrategy:
    "Strategy for a human player"
    def __init__(self, board, workers):
        self._board = board
        self._workers = workers
        self._active_worker = None


    def choose_worker(self):
        """Ask the user to choose one worker from the two."""
        colour_map = {
            "white": ("A", "B"),
            "blue": ("Y", "Z")
        }
        colour_category = self._workers[0].colour
        choice_of_worker = input("Select a worker to move\n")
        while choice_of_worker not in colour_map[colour_category]:
            if choice_of_worker in ("A", "B", "Y", "Z"):
                print("That is not your worker")
            else:
                print("Not a valid worker")
            choice_of_worker = input("Select a worker to move\n")
        if choice_of_worker == colour_map[colour_category][0]:
            self._active_worker = self._workers[0]
        else:
            self._active_worker = self._workers[1]
        return self._active_worker


    def choose_move_direction(self):
        """Ask the user to choose a direction to move to."""
        selected_move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
        all_directions = DIRECTIONS.keys()
        while selected_move not in all_directions or not self._active_worker.validate_move(selected_move):
            if selected_move not in all_directions:
                print("Not a valid direction")
            else:
                print(f"Cannot move {selected_move}")
            selected_move = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)\n")
        return selected_move


    def choose_build_direction(self, selected_move):
        """Ask the user to choose a direction to build at."""
        selected_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
        all_directions = DIRECTIONS.keys()
        while selected_build not in  all_directions or not self._active_worker.validate_build(selected_move, selected_build):
            if selected_build not in all_directions:
                print("Not a valid direction")
            else:
                print(f"Cannot build {selected_build}")
            selected_build = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)\n")
        return selected_build


    def player_makes_move(self):
        selected_worker = self.choose_worker()
        selected_move = self.choose_move_direction()
        selected_dir = self.choose_build_direction(selected_move)
        return MoveandBuild(self._board,selected_worker , selected_move, selected_dir)



# COMMAND PATTERN
# can break the MoveAndBuild class into Command Interface, Concrete Command Class, Receiver, Invoker
class MoveandBuild:
    def __init__(self, board : Board, selectedWorker, directionMove, directionBuild):
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
        print(self._active_worker.alpha + "," + self._move_direction + "," + self._build_direction)
        