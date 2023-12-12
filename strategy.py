from board import Board
import abc
import random
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

class Context:
    """
    Defines the interface to the clients and maintins a refernce to the strategy object.
    """
    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self):
        return self._strategy.generate_make_and_build()

    def set_strategy(self, strategy):
        self._strategy = strategy
        

class Strategy(metaclass=abc.ABCMeta):
    """
    Declare an interface common to all supported algorithms. Context
    uses this interface to call the algorithm defined by a
    ConcreteStrategy.
    """
    def __init__(self, board, workers):
        self._board = board
        self._workers = workers
        self._active_worker = None

    @abc.abstractmethod
    def generate_make_and_build(self):
        pass



class HumanStrategy(Strategy):
    "Strategy for a human player"
    def __init__(self, board, workers):
        super().__init__(board, workers)

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
        if self._active_worker.valid_moves() == []:
                print("That worker cannot move")
                self.choose_worker()
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


    def generate_make_and_build(self):
        selected_worker = self.choose_worker()
        selected_move = self.choose_move_direction()
        selected_dir = self.choose_build_direction(selected_move)
        return MoveandBuild(self._board,selected_worker , selected_move, selected_dir)
    
class RandomStrategy(Strategy):
    "Strategy for a random player"
    def __init__(self, board, workers):
        super().__init__(board, workers)

    def random_worker(self):
        """Ask the user to choose one worker from the two."""
        colour_map = {
            "white": ("A", "B"),
            "blue": ("Y", "Z")
        }
        colour_category = self._workers[0].colour
        possible_workers = colour_map[colour_category]
        choice_of_worker = random.choice(possible_workers)

        if choice_of_worker == colour_map[colour_category][0]:
            self._active_worker = self._workers[0]
        else:
            self._active_worker = self._workers[1]

        if self._active_worker.valid_moves() == []:
                print("That worker cannot move")
                self.random_worker()

        return self._active_worker

    def random_move_direction(self):
        """Ask the user to choose a direction to move to."""
        random_move = random.choice(self._active_worker.valid_moves())
        return random_move


    def random_build_direction(self, random_move):
        """Ask the user to choose a direction to build at."""
        random_build = random.choice(self._active_worker.valid_builds(random_move))
        return random_build


    def generate_make_and_build(self):
        random_worker = self.random_worker()
        random_move = self.random_move_direction()
        random_dir = self.random_build_direction(random_move)
        return MoveandBuild(self._board,random_worker , random_move, random_dir)

        
class HeuristicStrategy(Strategy):
    def __init__(self, board, workers):
        super().__init__(board, workers)
    
    def heuristic_worker(self):
        pass

    def heuristic_move_direction(self):
        pass

    def heuristic_build_direction(self):
        pass

    def generate_make_and_build(self):
        pass




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
        