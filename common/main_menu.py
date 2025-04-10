"""
Main menu system for the game project.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_schema import GameDatabase

class MainMenu:
    """Main menu system for the game project."""
    
    def __init__(self, root):
        """Initialize the main menu."""
        self.root = root
        self.root.title("Game Collection")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize database
        self.db = GameDatabase()
        
        # Player name
        self.player_name = None
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main menu widgets."""
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            self.main_frame, 
            text="Game Collection", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 30))
        
        # Player name entry
        player_frame = tk.Frame(self.main_frame)
        player_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            player_frame, 
            text="Player Name:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.player_entry = tk.Entry(player_frame, font=("Arial", 12), width=20)
        self.player_entry.pack(side=tk.LEFT)
        
        tk.Button(
            player_frame, 
            text="Set Name", 
            font=("Arial", 12),
            command=self.set_player_name
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Game buttons
        games_frame = tk.Frame(self.main_frame)
        games_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Configure grid
        for i in range(5):
            games_frame.grid_rowconfigure(i, weight=1)
        games_frame.grid_columnconfigure(0, weight=1)
        
        # Game buttons with descriptions
        games = [
            ("Tic-Tac-Toe", "Play a 5x5 Tic-Tac-Toe game against the computer", self.start_tic_tac_toe),
            ("Traveling Salesman", "Find the shortest route between cities", self.start_traveling_salesman),
            ("Tower of Hanoi", "Solve the Tower of Hanoi puzzle", self.start_tower_of_hanoi),
            ("Eight Queens Puzzle", "Place 8 queens on a chessboard without threatening each other", self.start_eight_queens),
            ("Knight's Tour", "Move a knight to visit every square on a chessboard exactly once", self.start_knights_tour)
        ]
        
        for i, (game_name, description, command) in enumerate(games):
            game_frame = tk.Frame(games_frame, relief=tk.RAISED, borderwidth=2)
            game_frame.grid(row=i, column=0, sticky="ew", pady=5)
            
            tk.Label(
                game_frame, 
                text=game_name, 
                font=("Arial", 14, "bold")
            ).pack(anchor="w", padx=10, pady=(10, 5))
            
            tk.Label(
                game_frame, 
                text=description, 
                font=("Arial", 10),
                wraplength=600,
                justify=tk.LEFT
            ).pack(anchor="w", padx=10, pady=(0, 5))
            
            tk.Button(
                game_frame, 
                text="Start Game", 
                font=("Arial", 12),
                command=command
            ).pack(anchor="e", padx=10, pady=(0, 10))
        
        # Exit button
        tk.Button(
            self.main_frame, 
            text="Exit", 
            font=("Arial", 12),
            command=self.root.destroy
        ).pack(pady=(20, 0))
    
    def set_player_name(self):
        """Set the player name."""
        name = self.player_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        self.player_name = name
        messagebox.showinfo("Success", f"Player name set to: {name}")
    
    def check_player_name(self):
        """Check if player name is set."""
        if not self.player_name:
            messagebox.showerror("Error", "Please set your player name first")
            return False
        return True
    
    def start_tic_tac_toe(self):
        """Start the Tic-Tac-Toe game."""
        if not self.check_player_name():
            return
        
        # Import here to avoid circular imports
        from games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
        
        # Hide main window
        self.root.withdraw()
        
        # Create game window
        game_window = tk.Toplevel(self.root)
        game = TicTacToeGame(game_window, self.player_name, self.db, self.return_to_main_menu)
        
    def start_traveling_salesman(self):
        """Start the Traveling Salesman game."""
        if not self.check_player_name():
            return
        
        messagebox.showinfo("Coming Soon", "Traveling Salesman game is coming soon!")
    
    def start_tower_of_hanoi(self):
        """Start the Tower of Hanoi game."""
        if not self.check_player_name():
            return
        
        messagebox.showinfo("Coming Soon", "Tower of Hanoi game is coming soon!")
    
    def start_eight_queens(self):
        """Start the Eight Queens game."""
        if not self.check_player_name():
            return
        
        messagebox.showinfo("Coming Soon", "Eight Queens game is coming soon!")
    
    def start_knights_tour(self):
        """Start the Knight's Tour game."""
        if not self.check_player_name():
            return
        
        messagebox.showinfo("Coming Soon", "Knight's Tour game is coming soon!")
    
    def return_to_main_menu(self, game_window):
        """Return to the main menu."""
        game_window.destroy()
        self.root.deiconify()

def main():
    """Main function to start the application."""
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
