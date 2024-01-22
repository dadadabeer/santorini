#include <iostream>
#include <vector>
#include <string>

// TODO: Paste this to a separate file and include it here
struct Position {
    int row;
    int col;
};


/**
 * Implementation of the Cell class. 
 * 
 * The Cell class represents a single cell on the board.
 */
class Cell {
private:
    int _row;
    int _col;
    int _height;
    std::string _worker; //change this to a worker object

public:
    // Constructor
    Cell(int row, int col) : _row(row), _col(col), _height(0), _worker("") {}

    // Getters
    int getRow() const { return _row; }
    int getCol() const { return _col; }
    int getHeight() const { return _height; }

    // Setters
    void setWorker(const std::string& worker) { _worker = worker; }
    

    // Increase the height of the cell by 1
    void increaseHeight() { _height < 4 ? _height++ : _height = 4; };

    // Returns the position of the cell as a struct
    Position getPosition() const { return Position{_row, _col}; }

    // String representation of the cell by overloading the << operator
    friend std::ostream& operator<<(std::ostream& os, const Cell& cell){
        std::string worker_repr = "A"; //replace this with the worker object's alphabet
        return os << cell._height << worker_repr;

    }

};


/**
 * Implementation of the Board class.
 * 
 * The Board class represents the game board.
 */

class Board {
private:
    std::vector<std::vector<Cell>> _board;

public:
    Board() : _board(5, std::vector<Cell>(5, Cell(0, 0))) {
        for (int i; i < 5; i++) {
            for (int j; j < 5; j++) {
                _board[i][j] = Cell(i, j);
            }
        }
    }

    // Getters
    Cell getCell(int row, int col) const { return _board[row][col]; }

    // String representation of the board by overloading the << operator
    friend std::ostream& operator<<(std::ostream& os, const Board& board) {
        os << "+--+--+--+--+--+" << std::endl;
        for (int i = 0; i < 5; i++) {
            os << "|";
            for (int j = 0; j < 5; j++) {
                os << board.getCell(i, j) << "|";
            }
            os << std::endl;
            os << "+--+--+--+--+--+" << std::endl;
        };
        return os;
    }

};


// Testing code for the board representation (to be removed)
int main() {
    Board board;
    std::cout << board << std::endl;
    return 0;
}