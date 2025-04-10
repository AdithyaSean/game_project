"""
Tic-Tac-Toe game implementation with 5x5 board and computer player algorithms.
"""
import tkinter as tk
from tkinter import messagebox
import random
import time
import numpy as np
import sys
import os
import math
from functools import partial

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.utils import timer_decorator, GameException, InvalidMoveException
from database.db_schema import GameDatabase

class TicTacToeGame:
    """Tic-Tac-Toe game with 5x5 board and computer player algorithms."""
    
    def __init__(self, root, player_name, db, return_callback):
        """Initialize the Tic-Tac-Toe game."""
        self.root = root
        self.player_name = player_name
        self.db = db
        self.return_callback = return_callback
        
        # Game state
        self.board_size = 5
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1  # 1 for human (X), -1 for computer (O)
        self.game_over = False
        self.winner = None
        
        # Algorithm selection
        self.algorithm = "minimax"  # Default algorithm
        
        # Game ID for database
        self.game_id = self.db.add_game("tic_tac_toe")
        
        # Set up the UI
        self.setup_ui()
        
        # Start the game
        self.update_status()
    
    def setup_ui(self):
        """Set up the game UI."""
        self.root.title("Tic-Tac-Toe (5x5)")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Tic-Tac-Toe (5x5)", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Player info
        player_frame = tk.Frame(main_frame)
        player_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            player_frame, 
            text=f"Player: {self.player_name} (X)", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            player_frame, 
            text="Computer (O)", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.RIGHT)
        
        # Algorithm selection
        algo_frame = tk.Frame(main_frame)
        algo_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            algo_frame, 
            text="Computer Algorithm:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.algo_var = tk.StringVar(value="minimax")
        
        tk.Radiobutton(
            algo_frame, 
            text="Minimax with Alpha-Beta Pruning", 
            variable=self.algo_var, 
            value="minimax",
            font=("Arial", 12),
            command=self.set_algorithm
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            algo_frame, 
            text="Monte Carlo Tree Search", 
            variable=self.algo_var, 
            value="mcts",
            font=("Arial", 12),
            command=self.set_algorithm
        ).pack(side=tk.LEFT)
        
        # Game board
        board_frame = tk.Frame(main_frame)
        board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 16, "bold"),
                    width=4,
                    height=2,
                    command=partial(self.make_move, i, j)
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        # Status label
        self.status_label = tk.Label(
            main_frame, 
            text="", 
            font=("Arial", 14),
            wraplength=600
        )
        self.status_label.pack(pady=20)
        
        # Algorithm performance
        self.performance_label = tk.Label(
            main_frame, 
            text="", 
            font=("Arial", 12),
            wraplength=600
        )
        self.performance_label.pack(pady=(0, 20))
        
        # Control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            control_frame, 
            text="New Game", 
            font=("Arial", 12),
            command=self.new_game
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="Return to Menu", 
            font=("Arial", 12),
            command=lambda: self.return_callback(self.root)
        ).pack(side=tk.RIGHT)
    
    def set_algorithm(self):
        """Set the computer player algorithm."""
        self.algorithm = self.algo_var.get()
        self.update_status()
    
    def update_status(self):
        """Update the status label."""
        if self.game_over:
            if self.winner == 1:
                status_text = "Game Over: You Win!"
            elif self.winner == -1:
                status_text = "Game Over: Computer Wins!"
            else:
                status_text = "Game Over: Draw!"
        else:
            if self.current_player == 1:
                status_text = "Your Turn (X)"
            else:
                status_text = "Computer's Turn (O)"
                # Trigger computer move after a short delay
                self.root.after(500, self.computer_move)
        
        self.status_label.config(text=status_text)
    
    def update_board_ui(self):
        """Update the board UI based on the current board state."""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == 1:
                    self.buttons[i][j].config(text="X", state=tk.DISABLED)
                elif self.board[i, j] == -1:
                    self.buttons[i][j].config(text="O", state=tk.DISABLED)
                else:
                    self.buttons[i][j].config(text="", state=tk.NORMAL)
    
    def make_move(self, row, col):
        """Make a move on the board."""
        if self.game_over or self.current_player != 1 or self.board[row, col] != 0:
            return
        
        # Update board
        self.board[row, col] = self.current_player
        
        # Check for win or draw
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
            self.save_game_result()
        elif self.check_draw():
            self.game_over = True
            self.winner = 0
            self.save_game_result()
        else:
            # Switch player
            self.current_player = -1
        
        # Update UI
        self.update_board_ui()
        self.update_status()
    
    def computer_move(self):
        """Make a computer move."""
        if self.game_over or self.current_player != -1:
            return
        
        # Choose algorithm
        if self.algorithm == "minimax":
            move, execution_time = self.minimax_move()
        else:  # mcts
            move, execution_time = self.mcts_move()
        
        # Record algorithm performance
        self.db.add_algorithm_performance(
            self.game_id,
            f"tic_tac_toe_{self.algorithm}",
            execution_time,
            1  # Game round
        )
        
        # Update performance label
        self.performance_label.config(
            text=f"Algorithm: {self.algorithm.upper()}, Execution time: {execution_time:.4f} seconds"
        )
        
        # Make the move
        row, col = move
        self.board[row, col] = self.current_player
        
        # Check for win or draw
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
            self.save_game_result()
        elif self.check_draw():
            self.game_over = True
            self.winner = 0
            self.save_game_result()
        else:
            # Switch player
            self.current_player = 1
        
        # Update UI
        self.update_board_ui()
        self.update_status()
    
    @timer_decorator
    def minimax_move(self):
        """Determine the best move using Minimax algorithm with alpha-beta pruning."""
        best_score = float('-inf')
        best_move = None
        
        # Get all available moves
        available_moves = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i, j] == 0]
        
        # Randomize move order for more varied gameplay
        random.shuffle(available_moves)
        
        for move in available_moves:
            row, col = move
            # Make the move
            self.board[row, col] = -1
            
            # Calculate score using minimax
            score = self.minimax(0, 3, True, float('-inf'), float('inf'))  # Depth limited to 3 for performance
            
            # Undo the move
            self.board[row, col] = 0
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, depth, max_depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning."""
        # Check for terminal states
        if self.check_win():
            return -10 + depth if is_maximizing else 10 - depth
        
        if self.check_draw() or depth == max_depth:
            return self.evaluate_board()
        
        if is_maximizing:  # Human player (X)
            best_score = float('-inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i, j] == 0:
                        self.board[i, j] = 1
                        score = self.minimax(depth + 1, max_depth, False, alpha, beta)
                        self.board[i, j] = 0
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:  # Computer player (O)
            best_score = float('inf')
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i, j] == 0:
                        self.board[i, j] = -1
                        score = self.minimax(depth + 1, max_depth, True, alpha, beta)
                        self.board[i, j] = 0
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    
    def evaluate_board(self):
        """Evaluate the current board state for the minimax algorithm."""
        # Simple evaluation: count the number of potential winning lines
        score = 0
        
        # Check rows
        for i in range(self.board_size):
            for j in range(self.board_size - 3):
                window = self.board[i, j:j+4]
                score += self.evaluate_window(window)
        
        # Check columns
        for i in range(self.board_size - 3):
            for j in range(self.board_size):
                window = self.board[i:i+4, j]
                score += self.evaluate_window(window)
        
        # Check diagonals (top-left to bottom-right)
        for i in range(self.board_size - 3):
            for j in range(self.board_size - 3):
                window = [self.board[i+k, j+k] for k in range(4)]
                score += self.evaluate_window(window)
        
        # Check diagonals (bottom-left to top-right)
        for i in range(3, self.board_size):
            for j in range(self.board_size - 3):
                window = [self.board[i-k, j+k] for k in range(4)]
                score += self.evaluate_window(window)
        
        return score
    
    def evaluate_window(self, window):
        """Evaluate a window of 4 positions."""
        # Count pieces in the window
        computer_count = np.count_nonzero(window == -1)
        human_count = np.count_nonzero(window == 1)
        empty_count = np.count_nonzero(window == 0)
        
        # Score the window
        if computer_count == 4:
            return 100  # Computer win
        elif computer_count == 3 and empty_count == 1:
            return 5  # Computer can win next move
        elif computer_count == 2 and empty_count == 2:
            return 2  # Computer has potential
        elif human_count == 3 and empty_count == 1:
            return -10  # Block human win
        elif human_count == 2 and empty_count == 2:
            return -2  # Block human potential
        
        return 0
    
    @timer_decorator
    def mcts_move(self):
        """Determine the best move using Monte Carlo Tree Search."""
        # Create root node
        root = MCTSNode(self.board.copy(), None, None, -1)
        
        # Run MCTS for a fixed number of iterations
        iterations = 1000
        for _ in range(iterations):
            # Selection and expansion
            node = self.select_node(root)
            
            # Simulation
            result = self.simulate_game(node.board.copy(), node.player)
            
            # Backpropagation
            self.backpropagate(node, result)
        
        # Choose the best move
        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.move
    
    def select_node(self, node):
        """Select a node for expansion in MCTS."""
        # If node is not fully expanded, expand it
        if not node.is_fully_expanded():
            return node.expand()
        
        # If node is terminal, return it
        if node.is_terminal():
            return node
        
        # Otherwise, select the best child according to UCT
        return self.select_node(node.best_child())
    
    def simulate_game(self, board, player):
        """Simulate a random game from the current board state."""
        current_player = player
        
        while True:
            # Check for terminal states
            if self.check_win_board(board):
                return -current_player  # Return the winner (opposite of current player)
            
            if self.check_draw_board(board):
                return 0  # Draw
            
            # Make a random move
            available_moves = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if board[i, j] == 0]
            if not available_moves:
                return 0  # Draw (no moves available)
            
            row, col = random.choice(available_moves)
            board[row, col] = current_player
            
            # Switch player
            current_player = -current_player
    
    def backpropagate(self, node, result):
        """Backpropagate the simulation result up the tree."""
        while node is not None:
            node.visits += 1
            if node.player == -result:  # If the result is a win for this node's player
                node.wins += 1
            node = node.parent
    
    def check_win(self):
        """Check if the current player has won."""
        return self.check_win_board(self.board)
    
    def check_win_board(self, board):
        """Check if there is a win on the given board."""
        # Check rows
        for i in range(self.board_size):
            for j in range(self.board_size - 3):
                if board[i, j] != 0 and board[i, j] == board[i, j+1] == board[i, j+2] == board[i, j+3]:
                    return True
        
        # Check columns
        for i in range(self.board_size - 3):
            for j in range(self.board_size):
                if board[i, j] != 0 and board[i, j] == board[i+1, j] == board[i+2, j] == board[i+3, j]:
                    return True
        
        # Check diagonals (top-left to bottom-right)
        for i in range(self.board_size - 3):
            for j in range(self.board_size - 3):
                if board[i, j] != 0 and board[i, j] == board[i+1, j+1] == board[i+2, j+2] == board[i+3, j+3]:
                    return True
        
        # Check diagonals (bottom-left to top-right)
        for i in range(3, self.board_size):
            for j in range(self.board_size - 3):
                if board[i, j] != 0 and board[i, j] == board[i-1, j+1] == board[i-2, j+2] == board[i-3, j+3]:
                    return True
        
        return False
    
    def check_draw(self):
        """Check if the game is a draw."""
        return self.check_draw_board(self.board)
    
    def check_draw_board(self, board):
        """Check if the given board is a draw."""
        return np.count_nonzero(board == 0) == 0
    
    def save_game_result(self):
        """Save the game result to the database."""
        # Add player to database if not exists
        player_id = self.db.add_player(self.player_name)
        
        # Determine the correct answer
        if self.winner == 1:
            correct_answer = "win"
        elif self.winner == -1:
            correct_answer = "loss"
        else:
            correct_answer = "draw"
        
        # Add game result
        self.db.add_game_result(
            player_id,
            self.game_id,
            correct_answer,
            0  # Time taken (not applicable for Tic-Tac-Toe)
        )
        
        # Add Tic-Tac-Toe specific data
        self.db.add_tic_tac_toe_game(
            self.game_id,
            str(self.board.tolist()),
            "X" if self.winner == 1 else "O" if self.winner == -1 else "Draw"
        )
    
    def new_game(self):
        """Start a new game."""
        # Reset game state
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
        # Create new game in database
        self.game_id = self.db.add_game("tic_tac_toe")
        
        # Reset performance label
        self.performance_label.config(text="")
        
        # Update UI
        self.update_board_ui()
        self.update_status()


class MCTSNode:
    """Node for Monte Carlo Tree Search."""
    
    def __init__(self, board, parent, move, player):
        """Initialize a MCTS node."""
        self.board = board
        self.parent = parent
        self.move = move
        self.player = player  # Player who made the move to reach this state
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = [
            (i, j) for i in range(len(board)) for j in range(len(board))
            if board[i, j] == 0
        ]
    
    def is_fully_expanded(self):
        """Check if all possible moves have been tried."""
        return len(self.untried_moves) == 0
    
    def is_terminal(self):
        """Check if this node represents a terminal state."""
        # Check for win
        game = TicTacToeGame(None, "", None, None)
        if game.check_win_board(self.board):
            return True
        
        # Check for draw
        if game.check_draw_board(self.board):
            return True
        
        return False
    
    def expand(self):
        """Expand the node by adding a child."""
        if not self.untried_moves:
            return self
        
        # Choose a random untried move
        move = random.choice(self.untried_moves)
        self.untried_moves.remove(move)
        
        # Create a new board with the move applied
        new_board = self.board.copy()
        row, col = move
        new_player = -self.player  # Switch player
        new_board[row, col] = new_player
        
        # Create a child node
        child = MCTSNode(new_board, self, move, new_player)
        self.children.append(child)
        
        return child
    
    def best_child(self, c_param=1.4):
        """Select the best child according to UCT formula."""
        # UCT formula: wins/visits + c_param * sqrt(ln(parent_visits) / visits)
        choices = [
            (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]


def main():
    """Main function to start the Tic-Tac-Toe game."""
    root = tk.Tk()
    db = GameDatabase()
    game = TicTacToeGame(root, "Player", db, lambda w: w.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()
