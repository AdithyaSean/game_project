"""
Eight Queens Puzzle game implementation with backtracking and genetic algorithms.
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

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.utils import timer_decorator, GameException, InvalidMoveException
from database.db_schema import GameDatabase

class EightQueensPuzzleGame:
    """Eight Queens Puzzle game with backtracking and genetic algorithms."""
    
    def __init__(self, root, player_name, db, return_callback):
        """Initialize the Eight Queens Puzzle game."""
        self.root = root
        self.player_name = player_name
        self.db = db
        self.return_callback = return_callback
        
        # Game state
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.solutions = []
        self.current_solution_index = 0
        self.max_solutions = 92  # Total number of solutions for 8 queens
        self.recognized_solutions = set()
        
        # Game ID for database
        self.game_id = self.db.add_game("eight_queens")
        
        # Set up the UI
        self.setup_ui()
        
        # Find all solutions
        self.find_all_solutions()
    
    def setup_ui(self):
        """Set up the game UI."""
        self.root.title("Eight Queens Puzzle")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Eight Queens Puzzle", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Player info
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_frame, 
            text=f"Player: {self.player_name}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        self.solutions_label = tk.Label(
            info_frame, 
            text=f"Solutions Found: 0/{self.max_solutions}", 
            font=("Arial", 12, "bold")
        )
        self.solutions_label.pack(side=tk.RIGHT)
        
        # Game rules
        rules_frame = tk.Frame(main_frame)
        rules_frame.pack(fill=tk.X, pady=(0, 20))
        
        rules_text = (
            "Rules:\n"
            "1. Place 8 queens on the chessboard so that no queen can attack another.\n"
            "2. Queens can move any number of squares horizontally, vertically, or diagonally.\n"
            "3. Find as many different solutions as possible.\n"
            "4. There are 92 distinct solutions in total."
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
                    command=partial(self.toggle_queen, i, j),
                    bg="white" if (i + j) % 2 == 0 else "gray"
                )
                button.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        # Control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            control_frame, 
            text="Clear Board", 
            font=("Arial", 12),
            command=self.clear_board
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="Check Solution", 
            font=("Arial", 12),
            command=self.check_solution
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="Show a Solution", 
            font=("Arial", 12),
            command=self.show_solution
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
            text="Genetic Algorithm", 
            variable=self.algo_var, 
            value="genetic",
            font=("Arial", 12)
        ).pack(side=tk.LEFT)
        
        self.performance_label = tk.Label(
            algo_frame, 
            text="", 
            font=("Arial", 12)
        )
        self.performance_label.pack(side=tk.RIGHT)
        
        # Solution list
        solution_frame = tk.Frame(main_frame)
        solution_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        tk.Label(
            solution_frame, 
            text="Found Solutions:", 
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.solution_listbox = tk.Listbox(
            solution_frame,
            font=("Arial", 12),
            height=5
        )
        self.solution_listbox.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.solution_listbox.bind('<<ListboxSelect>>', self.on_solution_select)
    
    def toggle_queen(self, row, col):
        """Toggle a queen on the board."""
        if self.board[row, col] == 1:
            self.board[row, col] = 0
            self.buttons[row][col].config(text="")
        else:
            self.board[row, col] = 1
            self.buttons[row][col].config(text="♛")
    
    def clear_board(self):
        """Clear the board."""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(text="")
    
    def check_solution(self):
        """Check if the current board configuration is a valid solution."""
        # Check if there are exactly 8 queens
        if np.sum(self.board) != 8:
            messagebox.showerror("Invalid Solution", "There must be exactly 8 queens on the board.")
            return
        
        # Check if any queen can attack another
        if not self.is_valid_solution(self.board):
            messagebox.showerror("Invalid Solution", "Some queens can attack each other.")
            return
        
        # Convert board to solution string
        solution_str = self.board_to_solution_string(self.board)
        
        # Check if this solution has already been recognized
        if solution_str in self.recognized_solutions:
            messagebox.showinfo("Solution Already Found", "This solution has already been recognized. Try to find a different one!")
            return
        
        # Check if this is a valid solution
        if solution_str in [self.board_to_solution_string(sol) for sol in self.solutions]:
            messagebox.showinfo("Valid Solution", "Congratulations! You found a valid solution.")
            
            # Add to recognized solutions
            self.recognized_solutions.add(solution_str)
            
            # Update solutions label
            self.solutions_label.config(text=f"Solutions Found: {len(self.recognized_solutions)}/{self.max_solutions}")
            
            # Add to solution listbox
            self.solution_listbox.insert(tk.END, f"Solution {len(self.recognized_solutions)}: {solution_str}")
            
            # Save to database
            self.save_solution(solution_str)
            
            # Check if all solutions have been found
            if len(self.recognized_solutions) == self.max_solutions:
                messagebox.showinfo("All Solutions Found", "Congratulations! You have found all 92 solutions!")
                
                # Clear recognition flags in database
                self.db.clear_eight_queens_recognition_flags()
                
                # Clear recognized solutions
                self.recognized_solutions = set()
        else:
            messagebox.showerror("Invalid Solution", "This is not a valid solution. Try again!")
    
    def is_valid_solution(self, board):
        """Check if a board configuration is valid (no queens can attack each other)."""
        # Check rows
        for i in range(self.board_size):
            if np.sum(board[i, :]) > 1:
                return False
        
        # Check columns
        for j in range(self.board_size):
            if np.sum(board[:, j]) > 1:
                return False
        
        # Check diagonals
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i, j] == 1:
                    # Check diagonal (top-left to bottom-right)
                    for k in range(1, min(self.board_size - i, self.board_size - j)):
                        if board[i + k, j + k] == 1:
                            return False
                    
                    # Check diagonal (top-right to bottom-left)
                    for k in range(1, min(self.board_size - i, j + 1)):
                        if board[i + k, j - k] == 1:
                            return False
                    
                    # Check diagonal (bottom-left to top-right)
                    for k in range(1, min(i + 1, self.board_size - j)):
                        if board[i - k, j + k] == 1:
                            return False
                    
                    # Check diagonal (bottom-right to top-left)
                    for k in range(1, min(i + 1, j + 1)):
                        if board[i - k, j - k] == 1:
                            return False
        
        return True
    
    def board_to_solution_string(self, board):
        """Convert a board configuration to a solution string."""
        solution = []
        for j in range(self.board_size):
            for i in range(self.board_size):
                if board[i, j] == 1:
                    solution.append(str(i + 1))
                    break
        return "".join(solution)
    
    def solution_string_to_board(self, solution_str):
        """Convert a solution string to a board configuration."""
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        for j, row in enumerate(solution_str):
            i = int(row) - 1
            board[i, j] = 1
        return board
    
    @timer_decorator
    def find_all_solutions_backtracking(self):
        """Find all solutions using backtracking algorithm."""
        solutions = []
        
        def backtrack(board, col):
            # If all queens are placed, add the solution
            if col >= self.board_size:
                solutions.append(board.copy())
                return
            
            # Try placing a queen in each row of the current column
            for row in range(self.board_size):
                if self.is_safe(board, row, col):
                    # Place the queen
                    board[row, col] = 1
                    
                    # Recur to place the rest of the queens
                    backtrack(board, col + 1)
                    
                    # Backtrack
                    board[row, col] = 0
        
        # Start with an empty board
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        backtrack(board, 0)
        
        return solutions
    
    def is_safe(self, board, row, col):
        """Check if it's safe to place a queen at board[row][col]."""
        # Check row on left side
        for j in range(col):
            if board[row, j] == 1:
                return False
        
        # Check upper diagonal on left side
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i, j] == 1:
                return False
        
        # Check lower diagonal on left side
        for i, j in zip(range(row, self.board_size), range(col, -1, -1)):
            if board[i, j] == 1:
                return False
        
        return True
    
    @timer_decorator
    def find_all_solutions_genetic(self):
        """Find solutions using genetic algorithm."""
        # Parameters
        population_size = 100
        generations = 1000
        mutation_rate = 0.1
        
        # Create initial population
        population = []
        for _ in range(population_size):
            # Each individual is a permutation of [0, 1, ..., 7]
            # representing the row index of the queen in each column
            individual = list(range(self.board_size))
            random.shuffle(individual)
            population.append(individual)
        
        # Best solutions found
        best_solutions = []
        best_fitness = 0
        
        # Evolution
        for _ in range(generations):
            # Calculate fitness for each individual
            fitness_scores = []
            for individual in population:
                fitness = self.calculate_fitness(individual)
                fitness_scores.append(fitness)
                
                # If this is a valid solution (no conflicts), add it to best solutions
                if fitness == 28:  # Maximum fitness for 8 queens (28 pairs that don't attack each other)
                    # Convert to board representation
                    board = np.zeros((self.board_size, self.board_size), dtype=int)
                    for j, i in enumerate(individual):
                        board[i, j] = 1
                    
                    # Check if this solution is already in best_solutions
                    solution_str = self.board_to_solution_string(board)
                    if solution_str not in [self.board_to_solution_string(sol) for sol in best_solutions]:
                        best_solutions.append(board)
                        
                        # If we found enough solutions, stop
                        if len(best_solutions) >= 10:  # Limit to 10 solutions for performance
                            return best_solutions
            
            # Create new population
            new_population = []
            
            # Elitism: keep the best individuals
            elite_count = 10
            elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:elite_count]
            for i in elite_indices:
                new_population.append(population[i])
            
            # Create rest of the new population
            while len(new_population) < population_size:
                # Selection (tournament selection)
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)
                
                # Crossover (ordered crossover)
                if random.random() < 0.7:  # Crossover rate
                    child = self.ordered_crossover(parent1, parent2)
                else:
                    child = parent1.copy()
                
                # Mutation
                if random.random() < mutation_rate:
                    self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        # Convert best individuals to board representation
        for individual in population:
            fitness = self.calculate_fitness(individual)
            if fitness > best_fitness:
                best_fitness = fitness
                
                # Convert to board representation
                board = np.zeros((self.board_size, self.board_size), dtype=int)
                for j, i in enumerate(individual):
                    board[i, j] = 1
                
                best_solutions = [board]
            elif fitness == best_fitness:
                # Convert to board representation
                board = np.zeros((self.board_size, self.board_size), dtype=int)
                for j, i in enumerate(individual):
                    board[i, j] = 1
                
                # Check if this solution is already in best_solutions
                solution_str = self.board_to_solution_string(board)
                if solution_str not in [self.board_to_solution_string(sol) for sol in best_solutions]:
                    best_solutions.append(board)
        
        return best_solutions
    
    def calculate_fitness(self, individual):
        """Calculate fitness of an individual (higher is better)."""
        # Count the number of non-attacking pairs of queens
        # Maximum is 28 for 8 queens (8 choose 2 = 28 pairs)
        conflicts = 0
        
        # Check diagonals
        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                # Queens are in the same diagonal if the difference in row indices
                # equals the difference in column indices
                if abs(individual[i] - individual[j]) == abs(i - j):
                    conflicts += 1
        
        # No need to check rows and columns as each queen is in a different column
        # by construction, and individual[i] gives the row of the queen in column i
        
        return 28 - conflicts  # 28 is the maximum number of pairs
    
    def tournament_selection(self, population, fitness_scores, tournament_size=3):
        """Tournament selection for genetic algorithm."""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_idx]
    
    def ordered_crossover(self, parent1, parent2):
        """Ordered crossover for genetic algorithm."""
        size = len(parent1)
        child = [None] * size
        
        # Select a random subset of parent1
        start, end = sorted(random.sample(range(size), 2))
        
        # Copy the subset from parent1 to child
        for i in range(start, end + 1):
            child[i] = parent1[i]
        
        # Fill the remaining positions with values from parent2 in order
        parent2_idx = 0
        for i in range(size):
            if child[i] is None:
                while parent2[parent2_idx] in child:
                    parent2_idx += 1
                child[i] = parent2[parent2_idx]
                parent2_idx += 1
        
        return child
    
    def mutate(self, individual):
        """Mutation for genetic algorithm (swap mutation)."""
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    
    def find_all_solutions(self):
        """Find all solutions using the selected algorithm."""
        algorithm = self.algo_var.get()
        
        if algorithm == "backtracking":
            self.solutions, execution_time = self.find_all_solutions_backtracking()
        else:  # genetic
            self.solutions, execution_time = self.find_all_solutions_genetic()
        
        # Record algorithm performance
        self.db.add_algorithm_performance(
            self.game_id,
            f"eight_queens_{algorithm}",
            execution_time,
            1  # Game round
        )
        
        # Update performance label
        self.performance_label.config(
            text=f"Algorithm: {algorithm.title()}, Execution time: {execution_time:.6f} seconds"
        )
        
        # Update solutions label
        self.solutions_label.config(text=f"Solutions Found: {len(self.recognized_solutions)}/{self.max_solutions}")
    
    def show_solution(self):
        """Show a solution on the board."""
        if not self.solutions:
            messagebox.showerror("No Solutions", "No solutions found. Try running the algorithm first.")
            return
        
        # Get the next solution
        solution = self.solutions[self.current_solution_index]
        self.current_solution_index = (self.current_solution_index + 1) % len(self.solutions)
        
        # Display the solution
        self.clear_board()
        self.board = solution.copy()
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == 1:
                    self.buttons[i][j].config(text="♛")
    
    def on_solution_select(self, event):
        """Handle selection of a solution from the listbox."""
        selection = self.solution_listbox.curselection()
        if not selection:
            return
        
        # Get the selected solution string
        solution_text = self.solution_listbox.get(selection[0])
        solution_str = solution_text.split(": ")[1]
        
        # Convert to board and display
        self.clear_board()
        self.board = self.solution_string_to_board(solution_str)
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i, j] == 1:
                    self.buttons[i][j].config(text="♛")
    
    def save_solution(self, solution_str):
        """Save a solution to the database."""
        # Add player to database if not exists
        player_id = self.db.add_player(self.player_name)
        
        # Add game result
        self.db.add_game_result(
            player_id,
            self.game_id,
            "correct",
            0  # Time taken (not applicable for Eight Queens)
        )
        
        # Add Eight Queens specific data
        self.db.add_eight_queens_game(
            self.game_id,
            solution_str,
            True  # is_recognized
        )
    
    def new_game(self):
        """Start a new game."""
        # Clear the board
        self.clear_board()
        
        # Clear recognized solutions
        self.recognized_solutions = set()
        
        # Reset solution index
        self.current_solution_index = 0
        
        # Clear solution listbox
        self.solution_listbox.delete(0, tk.END)
        
        # Update solutions label
        self.solutions_label.config(text=f"Solutions Found: 0/{self.max_solutions}")
        
        # Create new game in database
        self.game_id = self.db.add_game("eight_queens")
        
        # Find all solutions again
        self.find_all_solutions()


def main():
    """Main function to start the Eight Queens Puzzle game."""
    root = tk.Tk()
    db = GameDatabase()
    game = EightQueensPuzzleGame(root, "Player", db, lambda w: w.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()
