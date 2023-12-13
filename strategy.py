from board import Board
import abc
import random
from command import MoveandBuild
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

    def context_interface(self, game):
        return self._strategy.generate_make_and_build(game)

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
    def generate_make_and_build(self, game):
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


    def generate_make_and_build(self, game):
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


    def generate_make_and_build(self, game):
        random_worker = self.random_worker()
        random_move = self.random_move_direction()
        random_dir = self.random_build_direction(random_move)
        return MoveandBuild(self._board,random_worker , random_move, random_dir)

        
class HeuristicStrategy(Strategy):
    def __init__(self, board, workers):
        super().__init__(board, workers)

    def height_score_if_move(self, worker, dir):
        other_worker = self._workers[0] if worker == self._workers[1] else self._workers[1]
        delta_row, delta_col = DIRECTIONS.get(dir)
        curr_row, curr_col = worker.cell.pos()[0], worker.cell.pos()[1]
        landing_cell_row, landing_cell_col = delta_row + curr_row, delta_col + curr_col
        landing_cell = self._board.get_cell(landing_cell_row, landing_cell_col)
        return landing_cell.height + other_worker.cell.height
    
    def center_score_if_move(self, worker, dir):
        delta_row, delta_col = DIRECTIONS.get(dir)
        curr_row, curr_col = worker.cell.pos()[0], worker.cell.pos()[1]
        landing_cell_row, landing_cell_col = delta_row + curr_row, delta_col + curr_col
        center_score = 0
        if landing_cell_row == 2 and landing_cell_col == 2:
            center_score += 2
        elif 1 <= landing_cell_row <= 3 and 1 <= landing_cell_col <= 3:
            center_score += 1

        other_worker = self._workers[0] if worker == self._workers[1] else self._workers[1]
        other_worker_row, other_worker_col = other_worker.cell.pos()[0], other_worker.cell.pos()[1]
        if other_worker_row == 2 and other_worker_col == 2:
            center_score += 2
        elif 1 <= other_worker_row <= 3 and 1 <= other_worker_col <= 3:
            center_score += 1
    
        return center_score

    def distance_score_if_move(self, worker, dir, game):
        def chebyshev_distance(cell1, cell2):
            row1, col1 = cell1.pos()
            row2, col2 = cell2.pos()
            return max(abs(row1 - row2), abs(col1 - col2))
    
        delta_row, delta_col = DIRECTIONS.get(dir)
        curr_row, curr_col = worker.cell.pos()[0], worker.cell.pos()[1]
        landing_cell_row, landing_cell_col = delta_row + curr_row, delta_col + curr_col
        landing_cell = self._board.get_cell(landing_cell_row, landing_cell_col)

        player1, player2 = game.players

        worker_A_loc = player1.workers[0].cell
        worker_B_loc = player1.workers[1].cell
        worker_Y_loc = player2.workers[0].cell
        worker_Z_loc = player2.workers[1].cell

        if worker.alpha == "A":
            worker_A_loc = landing_cell
        elif worker.alpha == "B":
            worker_B_loc = landing_cell
        elif worker.alpha == "Y":
            worker_Y_loc = landing_cell
        elif worker.alpha == "Z":
            worker_Z_loc = landing_cell

        Z_to_A = chebyshev_distance(worker_Z_loc, worker_A_loc)
        Y_to_A = chebyshev_distance(worker_Y_loc, worker_A_loc)
        Z_to_B = chebyshev_distance(worker_Z_loc, worker_B_loc)
        Y_to_B = chebyshev_distance(worker_Y_loc, worker_B_loc)

        for_blue = min(Z_to_A, Y_to_A) + min(Z_to_B, Y_to_B)
        for_white = min(Z_to_A, Z_to_B) + min(Y_to_A, Y_to_B)

        if worker.colour == "white":
            return 8 - for_white
        return 8 - for_blue

    def heuristic_move_direction(self, game):
        c1, c2, c3 = 3, 2, 1
        possible_moves = []
        for worker in self._workers:
            valid_moves = worker.valid_moves()
            print("Valid moves for the worker ", worker.alpha, " are ", valid_moves)
            for dir in valid_moves:
                move_score = c1 * self.height_score_if_move(worker, dir) + c2 * self.center_score_if_move(worker, dir) + c3 * self.distance_score_if_move(worker, dir, game)
                possible_moves.append((move_score, worker, dir))
        
        possible_moves.sort(key=lambda x: x[0], reverse=True)
        ties = []
        for move in possible_moves:
            if move[0] == possible_moves[0][0]:
                ties.append(move)
        random_choice = random.choice(ties)
        self._active_worker = random_choice[1]
        return random_choice[2]
            

    def heuristic_build_direction(self, heuristic_move):
        random_build = random.choice(self._active_worker.valid_builds(heuristic_move))
        return random_build

    def generate_make_and_build(self, game):
        heuristic_move = self.heuristic_move_direction(game)
        heuristic_dir = self.heuristic_build_direction(heuristic_move)
        return MoveandBuild(self._board, self._active_worker, heuristic_move, heuristic_dir)

