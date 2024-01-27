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
    Worker _worker;

public:
    // Constructor
    Cell(int row, int col) : _row(row), _col(col), _height(0), _worker(NULL) {}

    // Note: the code from here until line 46 is for learning purposes only (Move Consytructor and Move Assignment Operator)
    // Another Note: If we define move contsructor, we should also define copy constructor, otherwise the comiler deletes the implicit one.
    // Move constructor
    Cell(Cell&& cell) noexcept
        : _row(cell._row), _col(cell._col), _height(cell._height), _worker(cell._worker) {}

    //Move constrcutor assignment operator- make sure it returns Cell&
    Cell& operator=(Cell&& cell) noexcept {
        _row = cell._row;
        _col = cell._col;
        _height = cell._height;
        _worker = cell._worker;
        return *this;
    }

    // Copy constructor
    Cell(const Cell& other) = default; 

    // Copy assignment operator
    Cell& operator=(const Cell& other) = default; //default means that the compiler will generate the code for us

    
    // Getters
    int getRow() const { return _row; }
    int getCol() const { return _col; }
    int getHeight() const { return _height; }
    const Worker& getWorker() const { return _worker; }

    // Setters
    void setWorker(const Worker& worker) { _worker = worker; }
    
    void increaseHeight() { _height < 4 ? _height++ : _height = 4; };

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
    // Constructor
    Board() : _board(5, std::vector<Cell>(5, Cell(0, 0))) {
        for (int i; i < 5; i++) {
            for (int j; j < 5; j++) {
                _board[i][j] = Cell(i, j);
            }
        }
    }

    // Getters
    const Cell& getCell(int row, int col) const { return _board[row][col]; }

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


/** 
 * The following code/examples are for learning purposes only.
 * Lets demonstrate the use of move semantics.
 * Cell c1(1, 1);
 * Cell c2(2, 2);
 * Cell c3(3, 3);
 * Now move c1 in to c2
 * c2 = std::move(c1);
 * Now c1 is empty and c2 has the values of c1
 * 
 * Now move c2 in to c3
 * c3 = std::move(c2);
 * Now c2 is empty and c3 has the values of c2
 * 
 * Now move c3 in to c1
 * c1 = std::move(c3);
 * Now c3 is empty and c1 has the values of c3
 * 
 * c3 = std::move(c2) = std::move(c1);
 * The order of the move operations is from right to left.
 * So, c1 is empty and c3 has the values of c1
 * 
 * We can also do move without using the  = operator 
 * c3(std::move(c2));
 * This operation is equivalent to c3 = std::move(c2);
 * Basically moves the values of c2 in to c3 and c2 is empty.
*/