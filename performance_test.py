"""
Performance testing and optimization for the game collection.
"""
import time
import cProfile
import pstats
import io
import tkinter as tk
import sys
import os
import sqlite3

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import MainMenu
from database.db_schema import GameDatabase
from games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from games.traveling_salesman.traveling_salesman_game import TravelingSalesmanGame
from games.tower_of_hanoi.tower_of_hanoi_game import TowerOfHanoiGame
from games.eight_queens.eight_queens_game import EightQueensPuzzleGame
from games.knights_tour.knights_tour_game import KnightsTourGame

def profile_algorithm(algorithm_func, *args, **kwargs):
    """Profile an algorithm function."""
    # Create a profiler
    pr = cProfile.Profile()
    
    # Start profiling
    pr.enable()
    
    # Run the algorithm
    result = algorithm_func(*args, **kwargs)
    
    # Stop profiling
    pr.disable()
    
    # Get the stats
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    
    return result, s.getvalue()

def test_tic_tac_toe_performance():
    """Test the performance of the Tic-Tac-Toe algorithms."""
    print("Testing Tic-Tac-Toe performance...")
    
    # Create a root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a game window
    game_window = tk.Toplevel(root)
    
    # Create the game
    db = GameDatabase()
    game = TicTacToeGame(game_window, "TestPlayer", db, lambda w: w.destroy())
    
    # Test Minimax algorithm
    print("Testing Minimax algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.minimax_move)
    end_time = time.time()
    print(f"Minimax execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test Monte Carlo Tree Search algorithm
    print("Testing Monte Carlo Tree Search algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.mcts_move)
    end_time = time.time()
    print(f"MCTS execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Clean up
    game_window.destroy()
    root.destroy()

def test_traveling_salesman_performance():
    """Test the performance of the Traveling Salesman Problem algorithms."""
    print("Testing Traveling Salesman Problem performance...")
    
    # Create a root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a game window
    game_window = tk.Toplevel(root)
    
    # Create the game
    db = GameDatabase()
    game = TravelingSalesmanGame(game_window, "TestPlayer", db, lambda w: w.destroy())
    
    # Test Nearest Neighbor algorithm
    print("Testing Nearest Neighbor algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.nearest_neighbor_algorithm)
    end_time = time.time()
    print(f"Nearest Neighbor execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test Dynamic Programming algorithm
    print("Testing Dynamic Programming algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.dynamic_programming_algorithm)
    end_time = time.time()
    print(f"Dynamic Programming execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test Genetic Algorithm
    print("Testing Genetic Algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.genetic_algorithm)
    end_time = time.time()
    print(f"Genetic Algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Clean up
    game_window.destroy()
    root.destroy()

def test_tower_of_hanoi_performance():
    """Test the performance of the Tower of Hanoi algorithms."""
    print("Testing Tower of Hanoi performance...")
    
    # Create a root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a game window
    game_window = tk.Toplevel(root)
    
    # Create the game
    db = GameDatabase()
    game = TowerOfHanoiGame(game_window, "TestPlayer", db, lambda w: w.destroy())
    
    # Test recursive algorithm
    print("Testing recursive algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.solve_recursive)
    end_time = time.time()
    print(f"Recursive algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test iterative algorithm
    print("Testing iterative algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.solve_iterative)
    end_time = time.time()
    print(f"Iterative algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Clean up
    game_window.destroy()
    root.destroy()

def test_eight_queens_performance():
    """Test the performance of the Eight Queens Puzzle algorithms."""
    print("Testing Eight Queens Puzzle performance...")
    
    # Create a root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a game window
    game_window = tk.Toplevel(root)
    
    # Create the game
    db = GameDatabase()
    game = EightQueensPuzzleGame(game_window, "TestPlayer", db, lambda w: w.destroy())
    
    # Test backtracking algorithm
    print("Testing backtracking algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.find_all_solutions_backtracking)
    end_time = time.time()
    print(f"Backtracking algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test genetic algorithm
    print("Testing genetic algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.find_all_solutions_genetic)
    end_time = time.time()
    print(f"Genetic algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Clean up
    game_window.destroy()
    root.destroy()

def test_knights_tour_performance():
    """Test the performance of the Knight's Tour Problem algorithms."""
    print("Testing Knight's Tour Problem performance...")
    
    # Create a root window for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create a game window
    game_window = tk.Toplevel(root)
    
    # Create the game
    db = GameDatabase()
    game = KnightsTourGame(game_window, "TestPlayer", db, lambda w: w.destroy())
    
    # Test backtracking algorithm
    print("Testing backtracking algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.solve_backtracking)
    end_time = time.time()
    print(f"Backtracking algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test Warnsdorff's algorithm
    print("Testing Warnsdorff's algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.solve_warnsdorff)
    end_time = time.time()
    print(f"Warnsdorff's algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Test neural network algorithm
    print("Testing neural network algorithm...")
    start_time = time.time()
    _, profile_output = profile_algorithm(game.solve_neural_network)
    end_time = time.time()
    print(f"Neural network algorithm execution time: {end_time - start_time:.6f} seconds")
    print(profile_output)
    
    # Clean up
    game_window.destroy()
    root.destroy()

def test_database_performance():
    """Test the performance of database operations."""
    print("Testing database performance...")
    
    # Create a test database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_database.db")
    
    # Remove the test database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create a new test database
    db = GameDatabase(db_path)
    
    # Test adding players
    print("Testing adding players...")
    start_time = time.time()
    for i in range(100):
        db.add_player(f"TestPlayer{i}")
    end_time = time.time()
    print(f"Adding 100 players: {end_time - start_time:.6f} seconds")
    
    # Test adding games
    print("Testing adding games...")
    start_time = time.time()
    game_ids = []
    for i in range(100):
        game_id = db.add_game("tic_tac_toe")
        game_ids.append(game_id)
    end_time = time.time()
    print(f"Adding 100 games: {end_time - start_time:.6f} seconds")
    
    # Test adding game results
    print("Testing adding game results...")
    start_time = time.time()
    for i in range(100):
        db.add_game_result(i + 1, game_ids[i], "correct", 10.5)
    end_time = time.time()
    print(f"Adding 100 game results: {end_time - start_time:.6f} seconds")
    
    # Test adding algorithm performance
    print("Testing adding algorithm performance...")
    start_time = time.time()
    for i in range(100):
        db.add_algorithm_performance(game_ids[i], "minimax", 0.5, 1)
    end_time = time.time()
    print(f"Adding 100 algorithm performance records: {end_time - start_time:.6f} seconds")
    
    # Test getting player statistics
    print("Testing getting player statistics...")
    start_time = time.time()
    db.get_player_statistics()
    end_time = time.time()
    print(f"Getting player statistics: {end_time - start_time:.6f} seconds")
    
    # Test getting game statistics
    print("Testing getting game statistics...")
    start_time = time.time()
    db.get_game_statistics()
    end_time = time.time()
    print(f"Getting game statistics: {end_time - start_time:.6f} seconds")
    
    # Test getting algorithm performance
    print("Testing getting algorithm performance...")
    start_time = time.time()
    db.get_algorithm_performance()
    end_time = time.time()
    print(f"Getting algorithm performance: {end_time - start_time:.6f} seconds")
    
    # Close the database connection
    db.close()
    
    # Remove the test database
    if os.path.exists(db_path):
        os.remove(db_path)

def main():
    """Main function to run all performance tests."""
    print("Running performance tests...")
    
    # Test Tic-Tac-Toe performance
    test_tic_tac_toe_performance()
    
    # Test Traveling Salesman Problem performance
    test_traveling_salesman_performance()
    
    # Test Tower of Hanoi performance
    test_tower_of_hanoi_performance()
    
    # Test Eight Queens Puzzle performance
    test_eight_queens_performance()
    
    # Test Knight's Tour Problem performance
    test_knights_tour_performance()
    
    # Test database performance
    test_database_performance()
    
    print("Performance tests completed.")

if __name__ == "__main__":
    main()
