# Game Collection - User Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Main Menu](#main-menu)
4. [Tic-Tac-Toe](#tic-tac-toe)
5. [Traveling Salesman Problem](#traveling-salesman-problem)
6. [Tower of Hanoi](#tower-of-hanoi)
7. [Eight Queens Puzzle](#eight-queens-puzzle)
8. [Knight's Tour Problem](#knights-tour-problem)
9. [Statistics](#statistics)
10. [Troubleshooting](#troubleshooting)

## Introduction

Welcome to the Game Collection! This application features five classic games and puzzles, each implemented with multiple algorithms and interactive user interfaces. The games are designed to demonstrate various computational approaches to solving problems, from simple board games to complex mathematical puzzles.

Each game includes:
- Multiple algorithm implementations
- Interactive user interface
- Performance tracking
- Database integration for storing results

This documentation will guide you through installing and using the application, as well as provide details on each game's rules and features.

## Installation

### System Requirements
- Python 3.10 or higher
- Tkinter (usually included with Python)
- SQLite3 (usually included with Python)
- Matplotlib
- NumPy

### Installation Steps

1. Clone or download the repository to your local machine.

2. Install the required dependencies:
   ```
   pip install matplotlib numpy
   ```

3. Run the application:
   ```
   python main.py
   ```

## Main Menu

The main menu is the central hub for accessing all games and features.

### Features
- **Player Name**: Enter your name to track your performance across all games.
- **Game Selection**: Choose from five different games to play.
- **Statistics**: View performance statistics for players, games, and algorithms.

### Usage
1. Enter your name in the "Player Name" field.
2. Click on any game button to start playing that game.
3. Click "View Statistics" to see performance data.
4. Click "Exit" to close the application.

## Tic-Tac-Toe

A 5x5 version of the classic Tic-Tac-Toe game, where you need to get 4 in a row to win.

### Rules
- The game is played on a 5x5 grid.
- Players take turns placing their symbol (X or O) on the board.
- The first player to get 4 of their symbols in a row (horizontally, vertically, or diagonally) wins.
- If the board fills up without a winner, the game is a draw.

### Features
- Play against two different AI algorithms:
  - **Minimax with Alpha-Beta Pruning**: A perfect player that considers all possible moves.
  - **Monte Carlo Tree Search (MCTS)**: A probabilistic algorithm that simulates random games.
- Choose your symbol (X or O) and who goes first.
- Performance tracking for both algorithms.

### Usage
1. Select your symbol (X or O) and the algorithm you want to play against.
2. Choose who goes first.
3. Click on a cell to make your move.
4. The game will automatically detect wins, losses, or draws.
5. Click "New Game" to start a new game or "Return to Menu" to go back to the main menu.

## Traveling Salesman Problem

Find the shortest route that visits all cities exactly once and returns to the starting city.

### Rules
- You are given a set of cities with distances between them.
- You must find a route that visits each city exactly once and returns to the starting city.
- The goal is to minimize the total distance traveled.

### Features
- Random generation of cities and distances.
- Three different algorithms to find solutions:
  - **Nearest Neighbor**: A greedy algorithm that always chooses the closest unvisited city.
  - **Dynamic Programming**: An exact algorithm that guarantees the optimal solution.
  - **Genetic Algorithm**: A population-based approach inspired by natural selection.
- Visual representation of cities and routes.
- Performance comparison between algorithms.

### Usage
1. The game will generate a random set of cities with distances between them.
2. You can manually select cities to create your own route or use one of the algorithms.
3. To manually create a route, click on cities in the order you want to visit them.
4. To use an algorithm, select it from the radio buttons and click "Find Route".
5. The total distance of your route will be displayed.
6. Click "New Game" for a new set of cities or "Return to Menu" to go back to the main menu.

## Tower of Hanoi

Move a stack of disks from one peg to another, following specific rules.

### Rules
- The game starts with a stack of disks on the first peg (Source).
- You must move all disks to the third peg (Destination).
- Only one disk can be moved at a time.
- A larger disk cannot be placed on top of a smaller disk.

### Features
- Random number of disks (5-10) for each game.
- Two solution algorithms:
  - **Recursive**: A classic recursive approach.
  - **Iterative**: A non-recursive implementation.
- Visual representation of pegs and disks.
- Option to input your own solution.

### Usage
1. The game will generate a random number of disks (5-10).
2. To make a move, select the source and destination pegs from the dropdowns and click "Make Move".
3. Alternatively, you can click directly on the pegs to select them.
4. To see a solution, click "Show Solution (Recursive)" or "Show Solution (Iterative)".
5. To submit your own solution, enter the number of moves and the move sequence in the provided fields.
6. Click "New Game" for a new set of disks or "Return to Menu" to go back to the main menu.

## Eight Queens Puzzle

Place eight queens on a chessboard so that no queen can attack another.

### Rules
- You must place 8 queens on an 8x8 chessboard.
- No queen can attack another queen.
- Queens can move any number of squares horizontally, vertically, or diagonally.
- There are 92 distinct solutions to this puzzle.

### Features
- Interactive chessboard for placing queens.
- Two solution algorithms:
  - **Backtracking**: A systematic approach that finds all solutions.
  - **Genetic Algorithm**: A population-based approach that evolves solutions.
- Solution tracking with flags for already recognized solutions.
- Visual representation of the chessboard and queens.

### Usage
1. Click on a square to place or remove a queen.
2. Once you have placed 8 queens, click "Check Solution" to verify if your solution is valid.
3. To see a solution, click "Show Solution".
4. The game will keep track of how many unique solutions you have found.
5. Click "New Game" to reset the board or "Return to Menu" to go back to the main menu.

## Knight's Tour Problem

Find a sequence of moves for a knight to visit every square on a chessboard exactly once.

### Rules
- The knight starts at a random position on an 8x8 chessboard.
- The knight must visit every square exactly once.
- The knight moves in an L-shape: 2 squares in one direction and then 1 square perpendicular to that direction.
- A closed tour ends with the knight being able to move back to its starting position.

### Features
- Random starting position for each game.
- Three solution algorithms:
  - **Backtracking**: A systematic approach that explores all possible moves.
  - **Warnsdorff's Algorithm**: A heuristic approach that chooses the move with the fewest onward moves.
  - **Neural Network**: A simplified neural approach using heuristics.
- Visual representation of the chessboard and knight's moves.
- Option to input your own solution.

### Usage
1. The game will generate a random starting position for the knight.
2. To make a move, click on a valid square or enter the row and column in the input fields.
3. Valid moves are knight's moves (L-shape) to unvisited squares.
4. To see a solution, select an algorithm and click "Show Solution".
5. To submit your own solution, enter the move sequence in the provided field.
6. Click "New Game" for a new starting position or "Return to Menu" to go back to the main menu.

## Statistics

The Statistics section provides performance data for players, games, and algorithms.

### Features
- **Player Statistics**: Shows each player's performance across all games.
- **Game Statistics**: Shows overall performance for each game type.
- **Algorithm Performance**: Shows execution times for different algorithms.

### Usage
1. From the main menu, click "View Statistics".
2. Navigate between the tabs to view different types of statistics.
3. Click "Close" to return to the main menu.

## Troubleshooting

### Common Issues

#### The application doesn't start
- Make sure you have Python 3.10 or higher installed.
- Verify that all dependencies are installed.
- Check that you're running the application from the correct directory.

#### Game windows appear blank or with missing elements
- Ensure that Tkinter is properly installed with your Python distribution.
- Try resizing the window to refresh the display.

#### Database errors
- The application creates a database file automatically. Make sure the directory is writable.
- If you encounter database errors, try deleting the database file and restarting the application.

### Contact

If you encounter any issues not covered in this documentation, please contact the developer or submit an issue on the project repository.

---

Thank you for using the Game Collection! Enjoy exploring the different games and algorithms.
