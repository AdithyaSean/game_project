"""
Main menu system for the game collection.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sys
import os
import sqlite3

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_schema import GameDatabase
from games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from games.traveling_salesman.traveling_salesman_game import TravelingSalesmanGame
from games.tower_of_hanoi.tower_of_hanoi_game import TowerOfHanoiGame
from games.eight_queens.eight_queens_game import EightQueensPuzzleGame
from games.knights_tour.knights_tour_game import KnightsTourGame

class MainMenu:
    """Main menu system for the game collection."""
    
    def __init__(self, root):
        """Initialize the main menu."""
        self.root = root
        self.db = GameDatabase()
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main menu UI."""
        self.root.title("Game Collection")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Game Collection", 
            font=("Arial", 32, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Player name input
        player_frame = tk.Frame(main_frame)
        player_frame.pack(fill=tk.X, pady=(0, 30))
        
        tk.Label(
            player_frame, 
            text="Player Name:", 
            font=("Arial", 14)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.player_name_var = tk.StringVar(value="Player")
        player_entry = tk.Entry(
            player_frame, 
            textvariable=self.player_name_var,
            font=("Arial", 14),
            width=20
        )
        player_entry.pack(side=tk.LEFT)
        
        # Game selection
        games_frame = tk.Frame(main_frame)
        games_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 30))
        
        tk.Label(
            games_frame, 
            text="Select a Game:", 
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 20))
        
        # Game buttons
        games = [
            ("Tic-Tac-Toe", self.start_tic_tac_toe),
            ("Traveling Salesman Problem", self.start_traveling_salesman),
            ("Tower of Hanoi", self.start_tower_of_hanoi),
            ("Eight Queens Puzzle", self.start_eight_queens),
            ("Knight's Tour Problem", self.start_knights_tour)
        ]
        
        for game_name, game_func in games:
            game_button = tk.Button(
                games_frame,
                text=game_name,
                font=("Arial", 14),
                command=game_func,
                width=30,
                height=2
            )
            game_button.pack(pady=10)
        
        # Statistics button
        stats_button = tk.Button(
            main_frame,
            text="View Statistics",
            font=("Arial", 14),
            command=self.view_statistics,
            width=20
        )
        stats_button.pack(pady=(0, 10))
        
        # Exit button
        exit_button = tk.Button(
            main_frame,
            text="Exit",
            font=("Arial", 14),
            command=self.root.destroy,
            width=20
        )
        exit_button.pack()
    
    def start_tic_tac_toe(self):
        """Start the Tic-Tac-Toe game."""
        player_name = self.player_name_var.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        # Create a new window for the game
        game_window = tk.Toplevel(self.root)
        game = TicTacToeGame(game_window, player_name, self.db, self.return_to_menu)
    
    def start_traveling_salesman(self):
        """Start the Traveling Salesman Problem game."""
        player_name = self.player_name_var.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        # Create a new window for the game
        game_window = tk.Toplevel(self.root)
        game = TravelingSalesmanGame(game_window, player_name, self.db, self.return_to_menu)
    
    def start_tower_of_hanoi(self):
        """Start the Tower of Hanoi game."""
        player_name = self.player_name_var.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        # Create a new window for the game
        game_window = tk.Toplevel(self.root)
        game = TowerOfHanoiGame(game_window, player_name, self.db, self.return_to_menu)
    
    def start_eight_queens(self):
        """Start the Eight Queens Puzzle game."""
        player_name = self.player_name_var.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        # Create a new window for the game
        game_window = tk.Toplevel(self.root)
        game = EightQueensPuzzleGame(game_window, player_name, self.db, self.return_to_menu)
    
    def start_knights_tour(self):
        """Start the Knight's Tour Problem game."""
        player_name = self.player_name_var.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter a player name.")
            return
        
        # Create a new window for the game
        game_window = tk.Toplevel(self.root)
        game = KnightsTourGame(game_window, player_name, self.db, self.return_to_menu)
    
    def return_to_menu(self, game_window):
        """Return to the main menu."""
        game_window.destroy()
        self.root.deiconify()
    
    def view_statistics(self):
        """View game statistics."""
        # Create a new window for statistics
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")
        stats_window.geometry("800x600")
        stats_window.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(stats_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Game Statistics", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Notebook for different statistics
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Player statistics tab
        player_frame = tk.Frame(notebook)
        notebook.add(player_frame, text="Player Statistics")
        
        # Game statistics tab
        game_frame = tk.Frame(notebook)
        notebook.add(game_frame, text="Game Statistics")
        
        # Algorithm performance tab
        algo_frame = tk.Frame(notebook)
        notebook.add(algo_frame, text="Algorithm Performance")
        
        # Populate player statistics
        self.populate_player_statistics(player_frame)
        
        # Populate game statistics
        self.populate_game_statistics(game_frame)
        
        # Populate algorithm performance
        self.populate_algorithm_performance(algo_frame)
        
        # Close button
        close_button = tk.Button(
            main_frame,
            text="Close",
            font=("Arial", 14),
            command=stats_window.destroy,
            width=20
        )
        close_button.pack(pady=(20, 0))
    
    def populate_player_statistics(self, frame):
        """Populate player statistics."""
        # Title
        tk.Label(
            frame, 
            text="Player Performance", 
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))
        
        # Create a treeview for player statistics
        columns = ("Player", "Games Played", "Correct Answers", "Incorrect Answers", "Success Rate")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Get player statistics from database
        player_stats = self.db.get_player_statistics()
        
        # Add data to the treeview
        for player_id, name, games_played, correct, incorrect in player_stats:
            success_rate = f"{(correct / games_played * 100):.2f}%" if games_played > 0 else "0.00%"
            tree.insert("", "end", values=(name, games_played, correct, incorrect, success_rate))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def populate_game_statistics(self, frame):
        """Populate game statistics."""
        # Title
        tk.Label(
            frame, 
            text="Game Statistics", 
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))
        
        # Create a treeview for game statistics
        columns = ("Game Type", "Games Played", "Correct Answers", "Incorrect Answers", "Success Rate")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Get game statistics from database
        game_stats = self.db.get_game_statistics()
        
        # Add data to the treeview
        for game_type, games_played, correct, incorrect in game_stats:
            success_rate = f"{(correct / games_played * 100):.2f}%" if games_played > 0 else "0.00%"
            tree.insert("", "end", values=(game_type, games_played, correct, incorrect, success_rate))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def populate_algorithm_performance(self, frame):
        """Populate algorithm performance statistics."""
        # Title
        tk.Label(
            frame, 
            text="Algorithm Performance", 
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 20))
        
        # Create a treeview for algorithm performance
        columns = ("Algorithm", "Average Execution Time (s)", "Min Time (s)", "Max Time (s)", "Executions")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        # Get algorithm performance from database
        algo_stats = self.db.get_algorithm_performance()
        
        # Add data to the treeview
        for algorithm, avg_time, min_time, max_time, executions in algo_stats:
            tree.insert("", "end", values=(algorithm, f"{avg_time:.6f}", f"{min_time:.6f}", f"{max_time:.6f}", executions))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
