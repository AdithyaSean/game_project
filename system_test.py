"""
System testing for the game collection.
"""
import unittest
import tkinter as tk
import sys
import os
import time
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

class SystemTest(unittest.TestCase):
    """System tests for the game collection."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        # Create a test database
        cls.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_database.db")
        
        # Remove the test database if it exists
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        
        # Create a new test database
        cls.db = GameDatabase(cls.db_path)
        
        # Create a root window for testing
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        # Destroy the root window
        cls.root.destroy()
        
        # Close the database connection
        cls.db.close()
        
        # Remove the test database
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    def test_main_menu_creation(self):
        """Test creating the main menu."""
        # Create the main menu
        main_menu = MainMenu(self.root)
        
        # Check that the main menu was created
        self.assertIsNotNone(main_menu)
        self.assertEqual(main_menu.root, self.root)
        self.assertIsNotNone(main_menu.db)
    
    def test_tic_tac_toe_integration(self):
        """Test integration with Tic-Tac-Toe game."""
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Create the game
        game = TicTacToeGame(game_window, "TestPlayer", self.db, lambda w: w.destroy())
        
        # Check that the game was created
        self.assertIsNotNone(game)
        self.assertEqual(game.root, game_window)
        self.assertEqual(game.player_name, "TestPlayer")
        self.assertEqual(game.db, self.db)
        
        # Clean up
        game_window.destroy()
    
    def test_traveling_salesman_integration(self):
        """Test integration with Traveling Salesman Problem game."""
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Create the game
        game = TravelingSalesmanGame(game_window, "TestPlayer", self.db, lambda w: w.destroy())
        
        # Check that the game was created
        self.assertIsNotNone(game)
        self.assertEqual(game.root, game_window)
        self.assertEqual(game.player_name, "TestPlayer")
        self.assertEqual(game.db, self.db)
        
        # Clean up
        game_window.destroy()
    
    def test_tower_of_hanoi_integration(self):
        """Test integration with Tower of Hanoi game."""
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Create the game
        game = TowerOfHanoiGame(game_window, "TestPlayer", self.db, lambda w: w.destroy())
        
        # Check that the game was created
        self.assertIsNotNone(game)
        self.assertEqual(game.root, game_window)
        self.assertEqual(game.player_name, "TestPlayer")
        self.assertEqual(game.db, self.db)
        
        # Clean up
        game_window.destroy()
    
    def test_eight_queens_integration(self):
        """Test integration with Eight Queens Puzzle game."""
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Create the game
        game = EightQueensPuzzleGame(game_window, "TestPlayer", self.db, lambda w: w.destroy())
        
        # Check that the game was created
        self.assertIsNotNone(game)
        self.assertEqual(game.root, game_window)
        self.assertEqual(game.player_name, "TestPlayer")
        self.assertEqual(game.db, self.db)
        
        # Clean up
        game_window.destroy()
    
    def test_knights_tour_integration(self):
        """Test integration with Knight's Tour Problem game."""
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Create the game
        game = KnightsTourGame(game_window, "TestPlayer", self.db, lambda w: w.destroy())
        
        # Check that the game was created
        self.assertIsNotNone(game)
        self.assertEqual(game.root, game_window)
        self.assertEqual(game.player_name, "TestPlayer")
        self.assertEqual(game.db, self.db)
        
        # Clean up
        game_window.destroy()
    
    def test_database_integration(self):
        """Test database integration."""
        # Add a player
        player_id = self.db.add_player("TestPlayer")
        
        # Check that the player was added
        self.assertIsNotNone(player_id)
        
        # Add a game
        game_id = self.db.add_game("tic_tac_toe")
        
        # Check that the game was added
        self.assertIsNotNone(game_id)
        
        # Add a game result
        result_id = self.db.add_game_result(player_id, game_id, "correct", 10.5)
        
        # Check that the game result was added
        self.assertIsNotNone(result_id)
        
        # Add algorithm performance
        perf_id = self.db.add_algorithm_performance(game_id, "minimax", 0.5, 1)
        
        # Check that the algorithm performance was added
        self.assertIsNotNone(perf_id)
        
        # Get player statistics
        player_stats = self.db.get_player_statistics()
        
        # Check that the player statistics were retrieved
        self.assertIsNotNone(player_stats)
        self.assertGreater(len(player_stats), 0)
        
        # Get game statistics
        game_stats = self.db.get_game_statistics()
        
        # Check that the game statistics were retrieved
        self.assertIsNotNone(game_stats)
        self.assertGreater(len(game_stats), 0)
        
        # Get algorithm performance
        algo_stats = self.db.get_algorithm_performance()
        
        # Check that the algorithm performance was retrieved
        self.assertIsNotNone(algo_stats)
        self.assertGreater(len(algo_stats), 0)
    
    def test_return_to_menu(self):
        """Test returning to the main menu."""
        # Create the main menu
        main_menu = MainMenu(self.root)
        
        # Create a game window
        game_window = tk.Toplevel(self.root)
        
        # Test the return_to_menu function
        main_menu.return_to_menu(game_window)
        
        # Check that the game window was destroyed
        with self.assertRaises(tk.TclError):
            game_window.winfo_exists()
    
    def test_view_statistics(self):
        """Test viewing statistics."""
        # Create the main menu
        main_menu = MainMenu(self.root)
        
        # Add some test data
        player_id = self.db.add_player("TestPlayer")
        game_id = self.db.add_game("tic_tac_toe")
        self.db.add_game_result(player_id, game_id, "correct", 10.5)
        self.db.add_algorithm_performance(game_id, "minimax", 0.5, 1)
        
        # Test the view_statistics function
        main_menu.view_statistics()
        
        # Check that the statistics window was created
        stats_window = None
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel) and window.title() == "Game Statistics":
                stats_window = window
                break
        
        self.assertIsNotNone(stats_window)
        
        # Clean up
        stats_window.destroy()


if __name__ == "__main__":
    unittest.main()
