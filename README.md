# Santorini Game Implementation Using Object-Oriented Design Patterns
## Introduction
This document describes the implementation of the Santorini game using object-oriented design patterns. Our focus was on leveraging these patterns to create a flexible, maintainable, and scalable game structure. We incorporated four key design patterns: Strategy, Factory, Memento, and Command.

## 1. Strategy Pattern
### Overview
The Strategy pattern is crucial for defining different game-playing strategies. It involves an abstract base class, Strategy, and three concrete strategy classes: HumanStrategy, RandomStrategy, and HeuristicStrategy.

### Implementation
Strategy Class: An abstract base class declaring the generate_make_and_build method.
Concrete Strategies:
HumanStrategy for human player interactions.
RandomStrategy for AI with random moves.
HeuristicStrategy for AI using heuristic values to determine actions.
Context Class: Holds a reference to a Strategy instance, delegating behavior execution to the strategy’s method.
Usage: The Player class, along with its derivatives (HumanPlayer, RandomPlayer, HeuristicPlayer), utilizes the Context class to set its strategy and execute moves and builds.
## 2. Factory Pattern
### Overview
The Factory pattern simplifies player creation, abstracting the instantiation logic.

### Implementation
FactoryofPlayers Class: Encapsulates the logic for creating Player objects.
Method: initiate_player determines the player type and instantiates the appropriate object.
Advantage: Simplifies the introduction of new player types with unique strategies.

## 3. Memento Pattern
### Overview
The Memento pattern allows for efficient game state management, enabling undo/redo functionality.

### Implementation
Caretaker Class: Manages game states.
State Management: Uses _game_state_mementos list to store game states.
Methods: save for storing current state, undo and redo for state navigation.

## 4. Command Pattern
### Overview
The Command pattern encapsulates move and build actions into a single object, streamlining game operations.

### Implementation
MoveandBuild Class: Represents move and build commands.
Initialization: Constructor sets up the board, active worker, and directions.
Methods: move and build to execute respective actions.

## Conclusion
By integrating these four design patterns, the Santorini game implementation achieves a high level of modularity, making it easier to modify or extend the game's functionalities. This approach ensures a clear separation of concerns, making the codebase more understandable and maintainable.

