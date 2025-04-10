"""
Tower of Hanoi game implementation with recursive and iterative solution algorithms.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import sys
import os
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.utils import timer_decorator, GameException, InvalidMoveException
from database.db_schema import GameDatabase

class TowerOfHanoiGame:
    """Tower of Hanoi game with recursive and iterative solution algorithms."""
    
    def __init__(self, root, player_name, db, return_callback):
        """Initialize the Tower of Hanoi game."""
        self.root = root
        self.player_name = player_name
        self.db = db
        self.return_callback = return_callback
        
        # Game state
        self.num_disks = random.randint(5, 10)
        self.pegs = [list(range(self.num_disks, 0, -1)), [], []]  # A, B, C pegs
        self.moves = []
        self.optimal_moves = []
        self.optimal_move_count = 2**self.num_disks - 1
        
        # Game ID for database
        self.game_id = self.db.add_game("tower_of_hanoi")
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the game UI."""
        self.root.title("Tower of Hanoi")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Tower of Hanoi", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Player info and disk count
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_frame, 
            text=f"Player: {self.player_name}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_frame, 
            text=f"Number of Disks: {self.num_disks}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.RIGHT)
        
        # Game rules
        rules_frame = tk.Frame(main_frame)
        rules_frame.pack(fill=tk.X, pady=(0, 20))
        
        rules_text = (
            "Rules:\n"
            "1. Only one disk can be moved at a time.\n"
            "2. A larger disk cannot be placed on a smaller disk.\n"
            "3. You can use the auxiliary peg to help move the disks.\n"
            f"Goal: Move all {self.num_disks} disks from Source (A) to Destination (C) in the minimum number of moves."
        )
        
        tk.Label(
            rules_frame, 
            text=rules_text, 
            font=("Arial", 12),
            justify=tk.LEFT
        ).pack(anchor="w")
        
        # Tower visualization
        self.tower_frame = tk.Frame(main_frame)
        self.tower_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create a figure for the visualization
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tower_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Draw the initial state
        self.draw_towers()
        
        # Move input
        move_frame = tk.Frame(main_frame)
        move_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            move_frame, 
            text="Enter Move (e.g., A to C):", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # Source peg dropdown
        tk.Label(
            move_frame, 
            text="From:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.source_var = tk.StringVar(value="A")
        source_dropdown = ttk.Combobox(
            move_frame, 
            textvariable=self.source_var,
            values=["A", "B", "C"],
            width=5,
            state="readonly"
        )
        source_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        
        # Destination peg dropdown
        tk.Label(
            move_frame, 
            text="To:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.dest_var = tk.StringVar(value="C")
        dest_dropdown = ttk.Combobox(
            move_frame, 
            textvariable=self.dest_var,
            values=["A", "B", "C"],
            width=5,
            state="readonly"
        )
        dest_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            move_frame, 
            text="Make Move", 
            font=("Arial", 12),
            command=self.make_move
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Solution input
        solution_frame = tk.Frame(main_frame)
        solution_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            solution_frame, 
            text=f"Enter your solution (number of moves and sequence):", 
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        # Number of moves entry
        num_moves_frame = tk.Frame(solution_frame)
        num_moves_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            num_moves_frame, 
            text="Number of Moves:", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.num_moves_entry = tk.Entry(num_moves_frame, font=("Arial", 12), width=10)
        self.num_moves_entry.pack(side=tk.LEFT)
        
        # Move sequence entry
        seq_frame = tk.Frame(solution_frame)
        seq_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            seq_frame, 
            text="Move Sequence (e.g., A->C, A->B, C->B):", 
            font=("Arial", 12)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.sequence_entry = tk.Entry(seq_frame, font=("Arial", 12), width=40)
        self.sequence_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(
            solution_frame, 
            text="Submit Solution", 
            font=("Arial", 12),
            command=self.submit_solution
        ).pack(anchor="e", pady=(10, 0))
        
        # Status and algorithm performance
        status_frame = tk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame, 
            text=f"Minimum number of moves required: {self.optimal_move_count}", 
            font=("Arial", 12, "italic")
        )
        self.status_label.pack(anchor="w")
        
        self.performance_label = tk.Label(
            status_frame, 
            text="", 
            font=("Arial", 12)
        )
        self.performance_label.pack(anchor="w", pady=(5, 0))
        
        # Control buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            control_frame, 
            text="Show Solution (Recursive)", 
            font=("Arial", 12),
            command=lambda: self.show_solution("recursive")
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            control_frame, 
            text="Show Solution (Iterative)", 
            font=("Arial", 12),
            command=lambda: self.show_solution("iterative")
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
        
        # Move history
        history_frame = tk.Frame(main_frame)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            history_frame, 
            text="Move History:", 
            font=("Arial", 12, "bold")
        ).pack(anchor="w")
        
        self.history_text = tk.Text(
            history_frame, 
            font=("Arial", 12),
            height=5,
            wrap=tk.WORD
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def draw_towers(self):
        """Draw the current state of the towers."""
        self.ax.clear()
        
        # Set up the plot
        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, self.num_disks + 1)
        self.ax.set_xticks([0.5, 1.5, 2.5])
        self.ax.set_xticklabels(['A (Source)', 'B (Auxiliary)', 'C (Destination)'])
        self.ax.set_yticks([])
        
        # Draw pegs
        for i in range(3):
            self.ax.plot([i + 0.5, i + 0.5], [0, self.num_disks], 'k-', linewidth=3)
        
        # Draw disks
        max_width = 0.4
        min_width = 0.1
        width_step = (max_width - min_width) / self.num_disks
        
        for peg_idx, peg in enumerate(self.pegs):
            for disk_idx, disk in enumerate(peg):
                width = min_width + (disk - 1) * width_step
                self.ax.add_patch(plt.Rectangle(
                    (peg_idx + 0.5 - width / 2, disk_idx),
                    width, 0.8,
                    facecolor=f'C{disk-1}',
                    edgecolor='black'
                ))
                self.ax.text(
                    peg_idx + 0.5, disk_idx + 0.4,
                    str(disk),
                    ha='center', va='center',
                    color='white', fontweight='bold'
                )
        
        self.canvas.draw()
    
    def make_move(self):
        """Make a move in the game."""
        source = self.source_var.get()
        dest = self.dest_var.get()
        
        if source == dest:
            messagebox.showerror("Invalid Move", "Source and destination pegs must be different")
            return
        
        # Convert peg letters to indices
        source_idx = ord(source) - ord('A')
        dest_idx = ord(dest) - ord('A')
        
        # Check if source peg is empty
        if not self.pegs[source_idx]:
            messagebox.showerror("Invalid Move", f"Peg {source} is empty")
            return
        
        # Check if move is valid (smaller disk on larger disk)
        if self.pegs[dest_idx] and self.pegs[source_idx][-1] > self.pegs[dest_idx][-1]:
            messagebox.showerror("Invalid Move", "A larger disk cannot be placed on a smaller disk")
            return
        
        # Make the move
        disk = self.pegs[source_idx].pop()
        self.pegs[dest_idx].append(disk)
        
        # Record the move
        self.moves.append((source, dest))
        
        # Update the history text
        move_text = f"Move {len(self.moves)}: {source} to {dest}\n"
        self.history_text.insert(tk.END, move_text)
        self.history_text.see(tk.END)
        
        # Update the visualization
        self.draw_towers()
        
        # Check if the game is solved
        if len(self.pegs[2]) == self.num_disks:
            messagebox.showinfo("Congratulations", f"You solved the Tower of Hanoi in {len(self.moves)} moves!")
            
            # Check if the solution is optimal
            if len(self.moves) == self.optimal_move_count:
                messagebox.showinfo("Perfect!", "You found the optimal solution!")
            else:
                messagebox.showinfo("Good Job", f"The optimal solution takes {self.optimal_move_count} moves.")
            
            # Save the game result
            self.save_game_result(True)
    
    def submit_solution(self):
        """Submit a complete solution."""
        # Get the number of moves
        try:
            num_moves = int(self.num_moves_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of moves must be an integer")
            return
        
        # Get the move sequence
        sequence_text = self.sequence_entry.get().strip()
        if not sequence_text:
            messagebox.showerror("Invalid Input", "Move sequence cannot be empty")
            return
        
        # Parse the move sequence
        try:
            # Split by commas or spaces
            if ',' in sequence_text:
                moves_str = sequence_text.split(',')
            else:
                moves_str = sequence_text.split()
            
            moves = []
            for move_str in moves_str:
                # Clean up the move string
                move_str = move_str.strip().upper()
                
                # Extract source and destination
                if '->' in move_str:
                    source, dest = move_str.split('->')
                elif 'TO' in move_str:
                    source, dest = move_str.split('TO')
                elif '-' in move_str:
                    source, dest = move_str.split('-')
                else:
                    # Assume format like "AC" for A to C
                    if len(move_str) != 2:
                        raise ValueError(f"Invalid move format: {move_str}")
                    source, dest = move_str[0], move_str[1]
                
                source = source.strip()
                dest = dest.strip()
                
                # Validate source and destination
                if source not in ['A', 'B', 'C'] or dest not in ['A', 'B', 'C']:
                    raise ValueError(f"Invalid peg: {source} or {dest}")
                
                if source == dest:
                    raise ValueError(f"Source and destination cannot be the same: {source} to {dest}")
                
                moves.append((source, dest))
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Error parsing move sequence: {e}")
            return
        
        # Check if the number of moves matches the sequence
        if num_moves != len(moves):
            messagebox.showerror("Invalid Input", f"Number of moves ({num_moves}) does not match the sequence length ({len(moves)})")
            return
        
        # Verify the solution
        is_valid, message = self.verify_solution(moves)
        
        if is_valid:
            messagebox.showinfo("Solution Valid", message)
            
            # Check if the solution is optimal
            if len(moves) == self.optimal_move_count:
                messagebox.showinfo("Perfect!", "You found the optimal solution!")
            else:
                messagebox.showinfo("Good Job", f"The optimal solution takes {self.optimal_move_count} moves.")
            
            # Save the game result
            self.save_game_result(True)
        else:
            messagebox.showerror("Invalid Solution", message)
    
    def verify_solution(self, moves):
        """Verify if a solution is valid."""
        # Create a copy of the initial state
        pegs = [list(range(self.num_disks, 0, -1)), [], []]
        
        # Apply each move
        for i, (source, dest) in enumerate(moves):
            source_idx = ord(source) - ord('A')
            dest_idx = ord(dest) - ord('A')
            
            # Check if source peg is empty
            if not pegs[source_idx]:
                return False, f"Move {i+1}: Peg {source} is empty"
            
            # Check if move is valid (smaller disk on larger disk)
            if pegs[dest_idx] and pegs[source_idx][-1] > pegs[dest_idx][-1]:
                return False, f"Move {i+1}: A larger disk cannot be placed on a smaller disk"
            
            # Make the move
            disk = pegs[source_idx].pop()
            pegs[dest_idx].append(disk)
        
        # Check if all disks are on the destination peg
        if len(pegs[2]) == self.num_disks:
            return True, f"Solution is valid! You solved the Tower of Hanoi in {len(moves)} moves."
        else:
            return False, "Not all disks are on the destination peg at the end"
    
    @timer_decorator
    def solve_recursive(self):
        """Solve the Tower of Hanoi using recursive algorithm."""
        moves = []
        
        def hanoi(n, source, auxiliary, destination):
            if n > 0:
                # Move n-1 disks from source to auxiliary
                hanoi(n-1, source, destination, auxiliary)
                
                # Move the nth disk from source to destination
                moves.append((source, destination))
                
                # Move n-1 disks from auxiliary to destination
                hanoi(n-1, auxiliary, source, destination)
        
        # Solve for all disks from A to C using B as auxiliary
        hanoi(self.num_disks, 'A', 'B', 'C')
        
        return moves
    
    @timer_decorator
    def solve_iterative(self):
        """Solve the Tower of Hanoi using iterative algorithm."""
        moves = []
        
        # For even number of disks, the first move is from A to B
        # For odd number of disks, the first move is from A to C
        if self.num_disks % 2 == 0:
            pegs = ['A', 'B', 'C']
        else:
            pegs = ['A', 'C', 'B']
        
        # Initialize the state
        state = [list(range(self.num_disks, 0, -1)), [], []]
        
        # Total number of moves required
        total_moves = 2**self.num_disks - 1
        
        for i in range(total_moves):
            # Determine which disk to move
            # The smallest disk moves every other step
            if i % 2 == 0:
                # Move the smallest disk
                # It cycles through the pegs in order
                source_idx = state.index(next(s for s in state if s and s[-1] == 1))
                dest_idx = (source_idx + 1) % 3
                
                source = pegs[source_idx]
                dest = pegs[dest_idx]
            else:
                # Find the smallest disk that can be moved (not the smallest disk)
                # This is either the second smallest disk visible, or any disk if the smallest is not visible
                smallest_visible = []
                for j, peg in enumerate(state):
                    if peg:
                        smallest_visible.append((peg[-1], j))
                
                smallest_visible.sort()
                
                if len(smallest_visible) > 1:
                    # Move the second smallest disk
                    _, source_idx = smallest_visible[1]
                    
                    # Determine the destination
                    # It can't go to where the smallest disk is
                    smallest_disk_idx = next(j for j, peg in enumerate(state) if peg and peg[-1] == 1)
                    
                    # Find the other peg where it can legally go
                    for dest_idx in range(3):
                        if dest_idx != source_idx and dest_idx != smallest_disk_idx:
                            # Check if the move is legal
                            if not state[dest_idx] or state[source_idx][-1] < state[dest_idx][-1]:
                                break
                    
                    source = pegs[source_idx]
                    dest = pegs[dest_idx]
                else:
                    # Only one disk is visible, move it
                    source_idx = smallest_visible[0][1]
                    
                    # Find a legal destination
                    for dest_idx in range(3):
                        if dest_idx != source_idx:
                            # Check if the move is legal
                            if not state[dest_idx] or state[source_idx][-1] < state[dest_idx][-1]:
                                break
                    
                    source = pegs[source_idx]
                    dest = pegs[dest_idx]
            
            # Make the move
            disk = state[source_idx].pop()
            state[dest_idx].append(disk)
            moves.append((source, dest))
        
        return moves
    
    def show_solution(self, algorithm):
        """Show the solution using the specified algorithm."""
        # Reset the game
        self.pegs = [list(range(self.num_disks, 0, -1)), [], []]
        self.moves = []
        self.history_text.delete(1.0, tk.END)
        self.draw_towers()
        
        # Solve using the specified algorithm
        if algorithm == "recursive":
            self.optimal_moves, execution_time = self.solve_recursive()
        else:  # iterative
            self.optimal_moves, execution_time = self.solve_iterative()
        
        # Record algorithm performance
        self.db.add_algorithm_performance(
            self.game_id,
            f"tower_of_hanoi_{algorithm}",
            execution_time,
            1  # Game round
        )
        
        # Update performance label
        self.performance_label.config(
            text=f"Algorithm: {algorithm.title()}, Execution time: {execution_time:.6f} seconds"
        )
        
        # Display the solution
        solution_text = "Solution:\n"
        for i, (source, dest) in enumerate(self.optimal_moves):
            solution_text += f"Move {i+1}: {source} to {dest}\n"
        
        # Show the solution in a new window
        solution_window = tk.Toplevel(self.root)
        solution_window.title(f"Tower of Hanoi Solution ({algorithm.title()})")
        solution_window.geometry("400x600")
        
        tk.Label(
            solution_window, 
            text=f"Optimal Solution ({len(self.optimal_moves)} moves):", 
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 10))
        
        solution_text_widget = tk.Text(
            solution_window, 
            font=("Arial", 12),
            wrap=tk.WORD
        )
        solution_text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        solution_text_widget.insert(tk.END, solution_text)
        
        tk.Button(
            solution_window, 
            text="Close", 
            font=("Arial", 12),
            command=solution_window.destroy
        ).pack(pady=(0, 20))
        
        # Also show the solution in the history text
        self.history_text.insert(tk.END, f"Optimal solution ({algorithm.title()}):\n")
        for i, (source, dest) in enumerate(self.optimal_moves):
            self.history_text.insert(tk.END, f"Move {i+1}: {source} to {dest}\n")
        
        self.history_text.see(tk.END)
    
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
            0  # Time taken (not applicable for Tower of Hanoi)
        )
        
        # Add Tower of Hanoi specific data
        move_sequence = ",".join([f"{s}->{d}" for s, d in self.moves])
        self.db.add_tower_of_hanoi_game(
            self.game_id,
            self.num_disks,
            move_sequence
        )
    
    def new_game(self):
        """Start a new game."""
        # Generate a new random number of disks
        self.num_disks = random.randint(5, 10)
        
        # Reset the game state
        self.pegs = [list(range(self.num_disks, 0, -1)), [], []]
        self.moves = []
        self.optimal_moves = []
        self.optimal_move_count = 2**self.num_disks - 1
        
        # Clear the history text
        self.history_text.delete(1.0, tk.END)
        
        # Clear the solution entries
        self.num_moves_entry.delete(0, tk.END)
        self.sequence_entry.delete(0, tk.END)
        
        # Reset the performance label
        self.performance_label.config(text="")
        
        # Update the status label
        self.status_label.config(text=f"Minimum number of moves required: {self.optimal_move_count}")
        
        # Create new game in database
        self.game_id = self.db.add_game("tower_of_hanoi")
        
        # Update the UI
        self.draw_towers()
        
        # Update disk count label
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label) and "Number of Disks:" in grandchild.cget("text"):
                                grandchild.config(text=f"Number of Disks: {self.num_disks}")


def main():
    """Main function to start the Tower of Hanoi game."""
    root = tk.Tk()
    db = GameDatabase()
    game = TowerOfHanoiGame(root, "Player", db, lambda w: w.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()
