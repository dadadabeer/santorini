#include <iostream>
#include <vector>
#include <string>
#include <tuple>
#include "board.cpp"
#include "util.h"

class Worker {
private:
    char _alpha;
    std::string _color;
    Cell _cell;
    Board _board;
public:
    // Constructor
    Worker(char alpha, std::string color, Cell cell, Board board) : _alpha(alpha), _color(color), _cell(cell), _board(board) {
        // _cell.setWorker(*this);
    }

    // Getter(s)
    char alpha() const{ return _alpha; }
    const Cell& getCell() const { return _cell; }

    // Setter(s)
    void setCell(const Cell& cell) { _cell = cell; }

    // bool validateMove(const std::string& to) {
    //     // std::tuple delta = DIRECTIONS[to];
    //     // int delta_row = std::get<0>(delta);
    //     // int delta_col = std::get<1>(delta);
    //     // the same is achieved directly:
    //     auto [deltaRow, deltaCol] = DIRECTIONS[to];
    //     int newRow = _cell.getRow() + deltaRow;
    //     int newCol = _cell.getCol() + deltaCol;

    //     if (!(0 <= newRow && newRow < 5 && 0 <= newCol && newCol < 5)) 
    //         return false;
        
    //     if (_board.getCell(newRow, newCol).getWorker() != NULL) 
    //         return false;
        
    //     int newFloors = _board.getCell(newRow, newCol).getHeight();
    //     int currFloors = _cell.getHeight();

    //     if (newFloors - currFloors > 1 || newFloors == 4)
    //         return false;

    //     return true;
    // }

    // bool validateBuild(const std::string& moveto, const std::string& buildto) {
    //     auto [deltaRowMove, deltaColMove] = DIRECTIONS[moveto];
    //     auto [deltaRowBuild, deltaColBuild] = DIRECTIONS[buildto];
    //     int newRow = _cell.getRow() + deltaRowMove + deltaRowBuild;
    //     int newCol = _cell.getCol() + deltaColMove + deltaColBuild;

    //     if (!(0 <= newRow && newRow < 5 && 0 <= newCol && newCol < 5)) 
    //         return false;
        
    //     if (_board.getCell(newRow, newCol).getWorker() != NULL) 
    //         return false;
        
    //     int newFloors = _board.getCell(newRow, newCol).getHeight();

    //     if (newFloors == 4)
    //         return false;

    //     return true;
    // }

    // std::vector<std::string> validMoves() {
    //     std::vector<std::string> valid_moves; // or std::vector<std::string> valid_moves = {};
    //     std::vector<std::string> all_directions = extractKeys(DIRECTIONS);

    //     for (const auto& dir: all_directions) {
    //         if (validateMove(dir)) {
    //             valid_moves.push_back(dir);
    //         }
    //     }
    //     return valid_moves;
    // }
    
    
    // std::vector<std::string> validBuilds() {
    //     std::vector<std::string> valid_builds; // or std::vector<std::string> valid_moves = {};
    //     std::vector<std::string> all_directions = extractKeys(DIRECTIONS);

    //     for (const auto& dir: all_directions) {
    //         if (validateBuild(dir)) {
    //             valid_builds.push_back(dir);
    //         }
    //     }
    //     return valid_builds;
    // }

    friend std::ostream& operator<<(std::ostream& os, const Worker& worker) {
        return os<<worker.alpha();
    }

};

class Player {
protected:
    Board _board;
    std::string _color;
    std::tuple<Worker, Worker> _workers = std::make_tuple(Worker(), Worker()); //consider changing this to a tuple of null pointers: std::tuple<Worker*, Worker*> _workers = std::make_tuple(nullptr, nullptr);
    Strategy strategy_type;

    int chebyshev_distance(const Cell& cell1, const Cell& cell2) {
        auto [row1, col1] = cell1.getPosition();
        auto [row2, col2] = cell1.getPosition();
        return std::max(abs(row1 - row2), abs(col1 - col2));
    }

public:
    Player(const Board& board, std::string color) : _board(board), _color(color) {
        if (_color == "white")
            _workers = std::make_tuple(Worker('A', "white", _board.getCell(3,1), _board), Worker('B', "white", _board.getCell(1,3), _board));

        if (_color == "blue")
            _workers = std::make_tuple(Worker('Y', "blue", _board.getCell(1,1), _board), Worker('Z', "blue", _board.getCell(3,3), _board));
    }

    // Getter(s)
    std::tuple<Worker, Worker> getWorkers() { return _workers; };

    void player_move(Game& game, bool display) {
        MoveAndBuildRequest move_and_build_request = _strategy_type.contextInterface(game); // we need contextInterface to return a reference to the MoveAndBuild object instead of a copy
        move_and_build_request.move();
        move_and_build_request.build();
        if (display)
            std::cout << " " << display_score(game);
        std::cout << std::endl;
        game.incrementTurnCounter();
        game.changePlayer()
    };

    int height_score() const {
        auto [worker1, worker2] = _workers;
        return worker1.getCell().getHeight() + worker1.getCell().getHeight();
    }
    // quite an elegant function to understand capturing of variables/lambda functions
    int center_score() const {
        int center_score = 0;
        std::apply([&center_score](const auto&... workers) {
            ([&center_score](const auto& worker) {
                auto [row, col] = worker.getCell().getPosition();
                if (row == 2 && col == 2)
                    center_score += 2;
                else if (1 <= row && row <= 3 && 1 <= col && col <= 3) {
                    center_score += 1;
                }
            }(workers), ...);
        }, _workers);
        return center_score;
    }

    int distance_score(std::tuple<Player,Player> players) {
        auto [player1, player2] = players;

        auto workers = player1.getWorkers();
        auto worker_A_loc = std::get<0>(workers).getCell();
        auto worker_B_loc = std::get<1>(workers).getCell();

        workers = player2.getWorkers();
        auto worker_Y_loc = std::get<0>(workers).getCell();
        auto worker_Z_loc = std::get<0>(workers).getCell();

        int Z_to_A = chebyshev_distance(worker_Z_loc, worker_A_loc);
        int Y_to_A = chebyshev_distance(worker_Y_loc, worker_A_loc);
        int Z_to_B = chebyshev_distance(worker_Z_loc, worker_B_loc);
        int Y_to_B = chebyshev_distance(worker_Y_loc, worker_B_loc);

        int for_blue = std::min(Z_to_A, Y_to_A) + std::min(Z_to_B, Y_to_B);
        int for_white = std::min(Z_to_A, Z_to_B) + std::min(Y_to_A, Y_to_B);

        if (_color == "white")
            return 8 - for_white;
        return 8 - for_blue;
    };

    std::string display_score(const Game& game) const {
        return std::to_string(height_score()) + ", " + std::to_string(center_score()) + std::to_string(distance_score(game.players));
    };

};


class HumanPlayer: public Player {
public:
    HumanPlayer(const Board& board, const std::string& color): Player(board, color) {
        _strategy_type = Context(HumanStrategy)
    }

};


class RandomPlayer: public Player {
public:
    RandomPlayer(const Board& board, const std::string& color): Player(board, color) {
        _strategy_type = Context(HumanStrategy(_board, _workers));
    };
};


class HeuristicPlayer: public Player {
public:
    HeuristicPlayer(const Board& board, const std::string& color): Player(board, color) {
        _strategy_type = Context(RandomStrategy(_board, _workers));
    };
};


/**
 * @brief Factory of Players (Factory Pattern)- creates and returns a Player object based on the specified player type.
 *
 * This function creates a player of the type specified by the `player_type`
 * parameter. The created player is associated with a given board and color.
 *
 * @param board The game board to associate with the player.
 * @param color The color assigned to the player.
 * @param player_type The type of player to create. Supported types are "human",
 *                    "random", and "heuristic".
 * @return A Player object of the specified type. If `player_type` is not recognized,
 *         the behavior is undefined.
 */
Player initiate_player(Board& board, std::string color, std::string player_type) {
    if (player_type == "human")
        return HumanPlayer(board, color);
    if (player_type == "random")
        return RandomPlayer(board, color);
    if (player_type == "heuristic")
        return HeuristicPlayer(board, color);
}

/*
We cannot just use auto anywhere. It can generally only be used for local variables.
I tried doing auto strategy_type under private (like where we define class variables) and it didn't work.
Notice how we have Game& game in the parametr list of player_move instead of Game& game because we are changing its state in the function 
we cannot apply rangebased for loops over tuples, we can use std::apply or we can use a for loop with indices if we know the length of the tuple
Can also unpack Structs using auto [row, col] = position
The main thing in this file to learn would be quite the elegant function to understand capturing of variables/lambda functions
*/