# Game Development Plan

## Project Overview
This project involves implementing 5 different games with UI, database integration, and multiple algorithm approaches as specified in the coursework requirements:

1. Tic-Tac-Toe (5x5)
2. Traveling Salesman Problem
3. Tower of Hanoi
4. Eight Queens Puzzle
5. Knight's Tour Problem

## Technology Stack
- **Programming Language**: Python
- **UI Framework**: Tkinter (for cross-platform GUI)
- **Database**: SQLite (for storing player information and algorithm performance)
- **Testing**: Python's unittest framework

## Common Components
1. **Main Menu System**
   - Central navigation hub for all games
   - Player name input/selection
   - Game selection interface

2. **Database Structure**
   - Player information (name, games played)
   - Game results (correct answers, completion time)
   - Algorithm performance metrics (execution time per algorithm)

3. **Utility Functions**
   - Timer functionality for measuring algorithm performance
   - Input validation
   - Exception handling
   - Database connection management

## Game-Specific Implementation Plans

### 1. Tic-Tac-Toe (5x5)
- **Data Structures**: 2D array/matrix for game board
- **Algorithms**:
  - Minimax algorithm with alpha-beta pruning
  - Monte Carlo Tree Search (MCTS)
- **UI Components**:
  - 5x5 grid of buttons
  - Game status display (win/lose/draw)
  - Player turn indicator
- **Database Requirements**:
  - Store player name
  - Store correct responses
  - Record algorithm execution time

### 2. Traveling Salesman Problem
- **Data Structures**: Graph representation (adjacency matrix)
- **Algorithms**:
  - Nearest Neighbor algorithm
  - Dynamic Programming approach
  - Genetic Algorithm
- **UI Components**:
  - Visual representation of cities and distances
  - City selection interface
  - Route display
  - Home city indicator
- **Database Requirements**:
  - Store player name
  - Store home city
  - Store selected cities
  - Store shortest route
  - Record algorithm execution time

### 3. Tower of Hanoi
- **Data Structures**: Stacks for each peg
- **Algorithms**:
  - Recursive solution
  - Iterative solution
- **UI Components**:
  - Visual representation of pegs and disks
  - Move input interface
  - Move counter
- **Database Requirements**:
  - Store player name
  - Store number of disks
  - Store move sequence
  - Record algorithm execution time

### 4. Eight Queens Puzzle
- **Data Structures**: 2D array/matrix for chessboard
- **Algorithms**:
  - Backtracking
  - Genetic Algorithm
- **UI Components**:
  - 8x8 chessboard
  - Queen placement interface
  - Solution counter
- **Database Requirements**:
  - Store player name
  - Store solution configuration
  - Flag for already recognized solutions
  - Record algorithm execution time

### 5. Knight's Tour Problem
- **Data Structures**: 2D array/matrix for chessboard
- **Algorithms**:
  - Backtracking
  - Warnsdorff's algorithm
  - Neural Network approach
- **UI Components**:
  - Chessboard with knight position
  - Move sequence display
  - Starting position selection
- **Database Requirements**:
  - Store player name
  - Store starting position
  - Store move sequence
  - Record algorithm execution time

## Development Phases

### Phase 1: Setup and Infrastructure
- Create project structure
- Set up database schema
- Implement common utilities
- Create main menu system

### Phase 2: Game Implementation
- Implement each game one by one
- For each game:
  - Implement core game logic
  - Implement algorithms
  - Create UI components
  - Add database integration
  - Implement validation and exception handling
  - Write unit tests

### Phase 3: Integration and Testing
- Integrate all games with the main menu
- Perform system testing
- Optimize performance
- Fix bugs

### Phase 4: Documentation and Delivery
- Create user documentation
- Document code
- Prepare demonstration
- Create video clip showing game features

## Timeline
- Tic-Tac-Toe: 2 days
- Traveling Salesman Problem: 2 days
- Tower of Hanoi: 2 days
- Eight Queens Puzzle: 2 days
- Knight's Tour Problem: 2 days
- Integration and Testing: 1 day
- Documentation and Delivery: 1 day

Total estimated time: 12 days
