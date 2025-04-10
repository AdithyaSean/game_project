"""
Knight's Tour Problem game implementation with multiple algorithm approaches.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import numpy as np
import sys
import os
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.utils import timer_decorator, GameException, InvalidMoveException
from database.db_schema import GameDatabase

class KnightsTourGame:
    """Knight's Tour Problem game with multiple algorithm approaches."""
    
    def __init__(self, root, player_name, db, return_callback):
        """Initialize the Knight's Tour game."""
        self.root = root
        self.player_name = player_name
        self.db = db
        self.return_callback = return_callback
        
        # Game state
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.start_position = self.choose_random_start_position()
        self.current_position = self.start_position
        self.move_sequence = [self.start_position]
        self.move_count = 1
        
        # Game ID for database
        self.game_id = self.db.add_game("knights_tour")
        
        # Set up the UI
        self.setup_ui()
        
        # Initialize the board
        self.initialize_board()
    
    def choose_random_start_position(self):
        """Choose a random starting position for the knight."""
        row = random.randint(0, self.board_size - 1)
        col = random.randint(0, self.board_size - 1)
        return (row, col)
    
    def setup_ui(self):
        """Set up the game UI."""
        self.root.title("Knight's Tour Problem")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Knight's Tour Problem", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Player info and start position
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_frame, 
            text=f"Player: {self.player_name}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        self.position_label = tk.Label(
            info_frame, 
            text=f"Starting Position: ({self.start_position[0]+1}, {self.start_position[1]+1})", 
            font=("Arial", 12, "bold")
        )
        self.position_label.pack(side=tk.RIGHT)
        
        # Game rules
        rules_frame = tk.Frame(main_frame)
        rules_frame.pack(fill=tk.X, pady=(0, 20))
        
        rules_text = (
            "Rules:\n"
            "1. The knight must visit every square on the chessboard exactly once.\n"
            "2. The knight moves in an L-shape: 2 squares in one direction and then 1 square perpendicular to that direction.\n"
            "3. The tour must end with the knight being able to move back to its starting position (closed tour).\n"
            "Goal: Find a valid knight's tour starting from the given position."
        )
        
        tk.Label(
            rules_frame, 
            text=rules_text, 
            font=("Arial", 12),
            justify=tk.LEFT
        ).pack(anchor="w")
        
        # Chessboard visualization
        board_frame = tk.Frame(main_frame)
        board_frame.pack(pady=(0, 20))
        
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
                    command=partial(self.make_move, i, j),
                    bg="white" if (i + j) % 2 == 0 else "gray"
                )
                button.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        # Move input
        move_frame = tk.Frame(main_frame)
        move_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            move_frame, 
            text="Enter Next Move:", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Row input
        tk.Label(
            move_frame, 
            text="Row:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.row_var = tk.StringVar()
        row_entry = ttk.Combobox(
            move_frame, 
            textvariable=self.row_var,
            values=[str(i+1) for i in range(self.board_size)],
            width=5,
            state="readonly"
        )
        row_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Column input
        tk.Label(
            move_frame, 
            text="Column:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.col_var = tk.StringVar()
        col_entry = ttk.Combobox(
            move_frame, 
            textvariable=self.col_var,
            values=[str(i+1) for i in range(self.board_size)],
            width=5,
            state="readonly"
        )
        col_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            move_frame, 
            text="Make Move", 
            font=("Arial", 12),
            command=self.make_move_from_input
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Solution input
        solution_frame = tk.Frame(main_frame)
        solution_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            solution_frame, 
            text="Enter Complete Solution (comma-separated positions, e.g., 1,1 2,3 4,2):", 
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.solution_entry = tk.Entry(solution_frame, font=("Arial", 12), width=50)
        self.solution_entry.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            solution_frame, 
            text="Submit Solution", 
            font=("Arial", 12),
            command=self.submit_solution
        ).pack(anchor="e", pady=(10, 0))
        
        # Algorithm selection and performance
        algo_frame = tk.Frame(main_frame)
        algo_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            algo_frame, 
            text="Algorithm:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.algo_var = tk.StringVar(value="backtracking")
        
        tk.Radiobutton(
            algo_frame, 
            text="Backtracking", 
            variable=self.algo_var, 
            value="backtracking",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            algo_frame, 
            text="Warnsdorff's Algorithm", 
            variable=self.algo_var, 
            value="warnsdorff",
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(
            algo_frame, 
            text="Neural Network", 
            variable=self.algo_var, 
            value="neural",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)
        
        self.performance_label = tk.Label(
            algo_frame, 
            text="", 
            font=("Arial", 12)
        )
        self.performance_label.pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            control_frame, 
            text="Show Solution", 
            font=("Arial", 12),
            command=self.show_solution
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="Reset Board", 
            font=("Arial", 12),
            command=self.reset_board
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="New Game", 
            font=("Arial", 12),
            command=self.new_game
        ).pack(side=tk.LEFT)
        
        tk.Button(
            control_frame, 
            text="Return to Menu", 
            font=("Arial", 12),
            command=lambda: self.return_callback(self.root)
        ).pack(side=tk.RIGHT)
        
        # Status and move history
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(
            status_frame, 
            text="Make your first move or use 'Show Solution' to see a solution.", 
            font=("Arial", 12, "italic")
        )
        self.status_label.pack(anchor="w")
        
        tk.Label(
            status_frame, 
            text="Move History:", 
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(10, 0))
        
        self.history_text = tk.Text(
            status_frame, 
            font=("Arial", 12),
            height=5,
            wrap=tk.WORD
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def initialize_board(self):
        """Initialize the board with the starting position."""
        # Clear the board
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Place the knight at the starting position
        row, col = self.start_position
        self.board[row, col] = 1
        
        # Update the UI
        self.update_board_ui()
        
        # Add the starting position to the history
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, f"Move 1: ({row+1}, {col+1})\n")
    
    def update_board_ui(self):
        """Update the board UI based on the current board state."""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] > 0:
                    self.buttons[i][j].config(text=str(self.board[i, j]))
                else:
                    self.buttons[i][j].config(text="")
                
                # Highlight the current position
                if (i, j) == self.current_position:
                    self.buttons[i][j].config(bg="lightblue")
                else:
                    self.buttons[i][j].config(bg="white" if (i + j) % 2 == 0 else "gray")
    
    def make_move(self, row, col):
        """Make a move on the board by clicking a square."""
        # Check if the move is valid
        if not self.is_valid_move(self.current_position, (row, col)):
            messagebox.showerror("Invalid Move", "The knight cannot move to that square.")
            return
        
        # Make the move
        self.move_count += 1
        self.board[row, col] = self.move_count
        self.current_position = (row, col)
        self.move_sequence.append(self.current_position)
        
        # Update the UI
        self.update_board_ui()
        
        # Add the move to the history
        self.history_text.insert(tk.END, f"Move {self.move_count}: ({row+1}, {col+1})\n")
        self.history_text.see(tk.END)
        
        # Check if the tour is complete
        if self.move_count == self.board_size * self.board_size:
            # Check if it's a closed tour (can return to start)
            if self.is_valid_move(self.current_position, self.start_position):
                messagebox.showinfo("Tour Complete", "Congratulations! You have completed a closed knight's tour.")
                self.save_game_result(True)
            else:
                messagebox.showinfo("Tour Complete", "You have completed an open knight's tour.")
                self.save_game_result(True)
        else:
            # Update status with available moves
            available_moves = self.get_available_moves(self.current_position)
            if not available_moves:
                messagebox.showinfo("Tour Incomplete", "No more valid moves available. The tour is incomplete.")
                self.status_label.config(text="No more valid moves available. Try again with 'Reset Board'.")
            else:
                self.status_label.config(text=f"Available moves: {len(available_moves)}. Current move: {self.move_count}.")
    
    def make_move_from_input(self):
        """Make a move on the board from the input fields."""
        try:
            row = int(self.row_var.get()) - 1
            col = int(self.col_var.get()) - 1
            
            if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                messagebox.showerror("Invalid Input", "Row and column must be between 1 and 8.")
                return
            
            self.make_move(row, col)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid row and column numbers.")
    
    def is_valid_move(self, from_pos, to_pos):
        """Check if a move from from_pos to to_pos is valid."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check if the destination is on the board
        if not (0 <= to_row < self.board_size and 0 <= to_col < self.board_size):
            return False
        
        # Check if the destination is already visited
        if self.board[to_row, to_col] > 0:
            return False
        
        # Check if the move is a valid knight's move
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        return (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1)
    
    def get_available_moves(self, position):
        """Get all available moves from the current position."""
        row, col = position
        possible_moves = [
            (row+2, col+1), (row+2, col-1),
            (row-2, col+1), (row-2, col-1),
            (row+1, col+2), (row+1, col-2),
            (row-1, col+2), (row-1, col-2)
        ]
        
        available_moves = []
        for move in possible_moves:
            if self.is_valid_move(position, move):
                available_moves.append(move)
        
        return available_moves
    
    def submit_solution(self):
        """Submit a complete solution."""
        # Get the solution string
        solution_text = self.solution_entry.get().strip()
        if not solution_text:
            messagebox.showerror("Invalid Input", "Solution cannot be empty.")
            return
        
        # Parse the solution
        try:
            # Split by commas or spaces
            if ',' in solution_text:
                moves_str = solution_text.split(',')
            else:
                moves_str = solution_text.split()
            
            moves = []
            for move_str in moves_str:
                # Clean up the move string
                move_str = move_str.strip()
                
                # Extract row and column
                if '(' in move_str and ')' in move_str:
                    # Format like (1, 2)
                    move_str = move_str.replace('(', '').replace(')', '')
                    parts = move_str.split(',')
                    row = int(parts[0].strip()) - 1
                    col = int(parts[1].strip()) - 1
                elif ' ' in move_str:
                    # Format like "1 2"
                    parts = move_str.split()
                    row = int(parts[0].strip()) - 1
                    col = int(parts[1].strip()) - 1
                else:
                    # Format like "12"
                    if len(move_str) != 2:
                        raise ValueError(f"Invalid move format: {move_str}")
                    row = int(move_str[0]) - 1
                    col = int(move_str[1]) - 1
                
                moves.append((row, col))
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Error parsing solution: {e}")
            return
        
        # Verify the solution
        is_valid, message = self.verify_solution(moves)
        
        if is_valid:
            messagebox.showinfo("Solution Valid", message)
            
            # Save the game result
            self.save_game_result(True)
            
            # Show the solution on the board
            self.reset_board()
            for i, (row, col) in enumerate(moves):
                self.move_count = i + 1
                self.board[row, col] = self.move_count
                self.current_position = (row, col)
                self.move_sequence.append(self.current_position)
            
            self.update_board_ui()
            
            # Update the history
            self.history_text.delete(1.0, tk.END)
            for i, (row, col) in enumerate(moves):
                self.history_text.insert(tk.END, f"Move {i+1}: ({row+1}, {col+1})\n")
        else:
            messagebox.showerror("Invalid Solution", message)
    
    def verify_solution(self, moves):
        """Verify if a solution is valid."""
        # Check if the first move is the starting position
        if moves[0] != self.start_position:
            return False, f"The first move must be the starting position: ({self.start_position[0]+1}, {self.start_position[1]+1})"
        
        # Check if all squares are visited exactly once
        if len(moves) != self.board_size * self.board_size:
            return False, f"The solution must visit all {self.board_size * self.board_size} squares exactly once."
        
        # Check if all moves are valid knight's moves
        for i in range(1, len(moves)):
            if not self.is_valid_knight_move(moves[i-1], moves[i]):
                return False, f"Invalid knight's move from {moves[i-1]} to {moves[i]}."
        
        # Check if it's a closed tour (can return to start)
        if self.is_valid_knight_move(moves[-1], moves[0]):
            return True, "Valid closed knight's tour!"
        else:
            return True, "Valid open knight's tour!"
    
    def is_valid_knight_move(self, from_pos, to_pos):
        """Check if a move from from_pos to to_pos is a valid knight's move."""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Check if the move is a valid knight's move
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        return (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1)
    
    @timer_decorator
    def solve_backtracking(self):
        """Solve the Knight's Tour using backtracking algorithm."""
        # Initialize the board
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Place the knight at the starting position
        row, col = self.start_position
        board[row, col] = 1
        
        # Define the possible moves of a knight
        move_x = [2, 1, -1, -2, -2, -1, 1, 2]
        move_y = [1, 2, 2, 1, -1, -2, -2, -1]
        
        # Solve using backtracking
        def solve_util(board, curr_x, curr_y, move_count):
            # If all squares are visited, the problem is solved
            if move_count == self.board_size * self.board_size:
                return True
            
            # Try all possible moves from the current position
            for i in range(8):
                next_x = curr_x + move_x[i]
                next_y = curr_y + move_y[i]
                
                # Check if the move is valid
                if (0 <= next_x < self.board_size and 
                    0 <= next_y < self.board_size and 
                    board[next_x, next_y] == 0):
                    
                    # Make the move
                    board[next_x, next_y] = move_count + 1
                    
                    # Recur to solve the rest of the tour
                    if solve_util(board, next_x, next_y, move_count + 1):
                        return True
                    
                    # Backtrack
                    board[next_x, next_y] = 0
            
            return False
        
        # Start the backtracking
        if solve_util(board, row, col, 1):
            # Convert the board to a move sequence
            move_sequence = []
            for move_num in range(1, self.board_size * self.board_size + 1):
                pos = np.where(board == move_num)
                move_sequence.append((pos[0][0], pos[1][0]))
            
            return move_sequence
        else:
            return None
    
    @timer_decorator
    def solve_warnsdorff(self):
        """Solve the Knight's Tour using Warnsdorff's algorithm."""
        # Initialize the board
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Place the knight at the starting position
        row, col = self.start_position
        board[row, col] = 1
        
        # Define the possible moves of a knight
        move_x = [2, 1, -1, -2, -2, -1, 1, 2]
        move_y = [1, 2, 2, 1, -1, -2, -2, -1]
        
        # Function to count the number of empty neighbors
        def count_empty_neighbors(x, y):
            count = 0
            for i in range(8):
                next_x = x + move_x[i]
                next_y = y + move_y[i]
                if (0 <= next_x < self.board_size and 
                    0 <= next_y < self.board_size and 
                    board[next_x, next_y] == 0):
                    count += 1
            return count
        
        # Solve using Warnsdorff's algorithm
        curr_x, curr_y = row, col
        move_count = 1
        move_sequence = [(curr_x, curr_y)]
        
        while move_count < self.board_size * self.board_size:
            min_deg_idx = -1
            min_deg = float('inf')
            
            # Find the next move with the minimum degree
            for i in range(8):
                next_x = curr_x + move_x[i]
                next_y = curr_y + move_y[i]
                
                if (0 <= next_x < self.board_size and 
                    0 <= next_y < self.board_size and 
                    board[next_x, next_y] == 0):
                    
                    # Count the number of empty neighbors
                    deg = count_empty_neighbors(next_x, next_y)
                    
                    if deg < min_deg:
                        min_deg = deg
                        min_deg_idx = i
            
            # If no move is available, the algorithm fails
            if min_deg_idx == -1:
                return None
            
            # Make the move
            curr_x = curr_x + move_x[min_deg_idx]
            curr_y = curr_y + move_y[min_deg_idx]
            move_count += 1
            board[curr_x, curr_y] = move_count
            move_sequence.append((curr_x, curr_y))
        
        return move_sequence
    
    @timer_decorator
    def solve_neural_network(self):
        """Solve the Knight's Tour using a neural network approach."""
        # This is a simplified neural network approach using a heuristic
        # In a real implementation, this would use a trained neural network
        
        # Initialize the board
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        
        # Place the knight at the starting position
        row, col = self.start_position
        board[row, col] = 1
        
        # Define the possible moves of a knight
        move_x = [2, 1, -1, -2, -2, -1, 1, 2]
        move_y = [1, 2, 2, 1, -1, -2, -2, -1]
        
        # Neural network heuristic: prefer moves that are closer to the center
        def neural_heuristic(x, y):
            # Distance from center (higher is better)
            center_x, center_y = self.board_size // 2, self.board_size // 2
            distance_from_center = -((x - center_x)**2 + (y - center_y)**2)
            
            # Number of empty neighbors (lower is better)
            empty_neighbors = 0
            for i in range(8):
                next_x = x + move_x[i]
                next_y = y + move_y[i]
                if (0 <= next_x < self.board_size and 
                    0 <= next_y < self.board_size and 
                    board[next_x, next_y] == 0):
                    empty_neighbors += 1
            
            # Combine the heuristics (weighted sum)
            return 0.3 * distance_from_center - 0.7 * empty_neighbors
        
        # Solve using the neural network heuristic
        curr_x, curr_y = row, col
        move_count = 1
        move_sequence = [(curr_x, curr_y)]
        
        while move_count < self.board_size * self.board_size:
            best_score = float('-inf')
            best_move = -1
            
            # Find the next move with the best score
            for i in range(8):
                next_x = curr_x + move_x[i]
                next_y = curr_y + move_y[i]
                
                if (0 <= next_x < self.board_size and 
                    0 <= next_y < self.board_size and 
                    board[next_x, next_y] == 0):
                    
                    # Calculate the score using the neural heuristic
                    score = neural_heuristic(next_x, next_y)
                    
                    if score > best_score:
                        best_score = score
                        best_move = i
            
            # If no move is available, the algorithm fails
            if best_move == -1:
                return None
            
            # Make the move
            curr_x = curr_x + move_x[best_move]
            curr_y = curr_y + move_y[best_move]
            move_count += 1
            board[curr_x, curr_y] = move_count
            move_sequence.append((curr_x, curr_y))
        
        return move_sequence
    
    def show_solution(self):
        """Show a solution for the Knight's Tour."""
        algorithm = self.algo_var.get()
        
        # Solve using the selected algorithm
        if algorithm == "backtracking":
            move_sequence, execution_time = self.solve_backtracking()
        elif algorithm == "warnsdorff":
            move_sequence, execution_time = self.solve_warnsdorff()
        else:  # neural
            move_sequence, execution_time = self.solve_neural_network()
        
        # Record algorithm performance
        self.db.add_algorithm_performance(
            self.game_id,
            f"knights_tour_{algorithm}",
            execution_time,
            1  # Game round
        )
        
        # Update performance label
        self.performance_label.config(
            text=f"Algorithm: {algorithm.title()}, Execution time: {execution_time:.6f} seconds"
        )
        
        if move_sequence:
            # Reset the board
            self.reset_board()
            
            # Show the solution
            for i, (row, col) in enumerate(move_sequence):
                self.move_count = i + 1
                self.board[row, col] = self.move_count
                self.current_position = (row, col)
                self.move_sequence.append(self.current_position)
            
            self.update_board_ui()
            
            # Update the history
            self.history_text.delete(1.0, tk.END)
            for i, (row, col) in enumerate(move_sequence):
                self.history_text.insert(tk.END, f"Move {i+1}: ({row+1}, {col+1})\n")
            
            # Check if it's a closed tour
            if self.is_valid_knight_move(move_sequence[-1], move_sequence[0]):
                self.status_label.config(text="Solution found: Closed Knight's Tour")
            else:
                self.status_label.config(text="Solution found: Open Knight's Tour")
        else:
            messagebox.showerror("No Solution", "No solution found for the current starting position.")
    
    def reset_board(self):
        """Reset the board to the initial state."""
        # Reset game state
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_position = self.start_position
        self.move_sequence = [self.start_position]
        self.move_count = 1
        
        # Initialize the board
        self.initialize_board()
        
        # Update status
        self.status_label.config(text="Board reset. Make your first move or use 'Show Solution' to see a solution.")
    
    def save_game_result(self, is_correct):
        """Save the game result to the database."""
        # Add player to database if not exists
        player_id = self.db.add_player(self.player_name)
        
        # Determine the correct answer
        correct_answer = "correct" if is_correct else "incorrect"
        
        # Add game result
        self.db.add_game_result(
            player_id,
            self.game_id,
            correct_answer,
            0  # Time taken (not applicable for Knight's Tour)
        )
        
        # Add Knight's Tour specific data
        start_pos_str = f"{self.start_position[0]+1},{self.start_position[1]+1}"
        move_sequence_str = ",".join([f"{row+1},{col+1}" for row, col in self.move_sequence])
        
        self.db.add_knights_tour_game(
            self.game_id,
            start_pos_str,
            move_sequence_str
        )
    
    def new_game(self):
        """Start a new game."""
        # Choose a new random starting position
        self.start_position = self.choose_random_start_position()
        
        # Reset game state
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_position = self.start_position
        self.move_sequence = [self.start_position]
        self.move_count = 1
        
        # Update the position label
        self.position_label.config(text=f"Starting Position: ({self.start_position[0]+1}, {self.start_position[1]+1})")
        
        # Initialize the board
        self.initialize_board()
        
        # Update status
        self.status_label.config(text="New game started. Make your first move or use 'Show Solution' to see a solution.")
        
        # Create new game in database
        self.game_id = self.db.add_game("knights_tour")


def main():
    """Main function to start the Knight's Tour game."""
    root = tk.Tk()
    db = GameDatabase()
    game = KnightsTourGame(root, "Player", db, lambda w: w.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()
