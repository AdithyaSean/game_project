"""
Unit tests for the Tower of Hanoi game.
"""
import unittest
import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from games.tower_of_hanoi.tower_of_hanoi_game import TowerOfHanoiGame

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.players = {}
        self.games = {}
        self.game_results = {}
        self.algorithm_performance = {}
        self.tower_of_hanoi_games = {}
    
    def add_player(self, name):
        """Add a new player or get existing player ID."""
        if name in self.players:
            return self.players[name]
        player_id = len(self.players) + 1
        self.players[name] = player_id
        return player_id
    
    def add_game(self, game_type):
        """Add a new game session."""
        game_id = len(self.games) + 1
        self.games[game_id] = game_type
        return game_id
    
    def add_game_result(self, player_id, game_id, correct_answer, time_taken):
        """Record a game result."""
        result_id = len(self.game_results) + 1
        self.game_results[result_id] = {
            'player_id': player_id,
            'game_id': game_id,
            'correct_answer': correct_answer,
            'time_taken': time_taken
        }
        return result_id
    
    def add_algorithm_performance(self, game_id, algorithm_name, execution_time, game_round):
        """Record algorithm performance metrics."""
        perf_id = len(self.algorithm_performance) + 1
        self.algorithm_performance[perf_id] = {
            'game_id': game_id,
            'algorithm_name': algorithm_name,
            'execution_time': execution_time,
            'game_round': game_round
        }
        return perf_id
    
    def add_tower_of_hanoi_game(self, game_id, num_disks, move_sequence):
        """Record a Tower of Hanoi game."""
        game_record_id = len(self.tower_of_hanoi_games) + 1
        self.tower_of_hanoi_games[game_record_id] = {
            'game_id': game_id,
            'num_disks': num_disks,
            'move_sequence': move_sequence
        }
        return game_record_id


class TestTowerOfHanoiGame(unittest.TestCase):
    """Test cases for the Tower of Hanoi game."""
    
    def setUp(self):
        """Set up test environment."""
        self.db = MockDatabase()
        # Create a headless game instance for testing
        self.game = TowerOfHanoiGame(None, "TestPlayer", self.db, lambda w: None)
        # Override UI-related methods
        self.game.setup_ui = lambda: None
        self.game.draw_towers = lambda: None
    
    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertTrue(5 <= self.game.num_disks <= 10)
        self.assertEqual(len(self.game.pegs), 3)
        self.assertEqual(len(self.game.pegs[0]), self.game.num_disks)
        self.assertEqual(len(self.game.pegs[1]), 0)
        self.assertEqual(len(self.game.pegs[2]), 0)
        self.assertEqual(self.game.moves, [])
        self.assertEqual(self.game.optimal_move_count, 2**self.game.num_disks - 1)
    
    def test_make_move_valid(self):
        """Test making a valid move."""
        # Set up a simple state
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # Make a valid move (smallest disk from A to C)
        self.game.source_var = type('obj', (object,), {'get': lambda: 'A'})
        self.game.dest_var = type('obj', (object,), {'get': lambda: 'C'})
        self.game.history_text = type('obj', (object,), {
            'insert': lambda *args: None,
            'see': lambda *args: None
        })
        
        # Mock messagebox
        original_messagebox = sys.modules.get('tkinter.messagebox', None)
        sys.modules['tkinter.messagebox'] = type('obj', (object,), {
            'showerror': lambda *args: None,
            'showinfo': lambda *args: None
        })
        
        try:
            self.game.make_move()
            
            # Check that the move was made
            self.assertEqual(self.game.pegs, [[3, 2], [], [1]])
            self.assertEqual(self.game.moves, [('A', 'C')])
        finally:
            # Restore messagebox
            if original_messagebox:
                sys.modules['tkinter.messagebox'] = original_messagebox
            else:
                del sys.modules['tkinter.messagebox']
    
    def test_make_move_invalid_same_peg(self):
        """Test making an invalid move to the same peg."""
        # Set up a simple state
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # Try to make an invalid move (A to A)
        self.game.source_var = type('obj', (object,), {'get': lambda: 'A'})
        self.game.dest_var = type('obj', (object,), {'get': lambda: 'A'})
        
        # Mock messagebox
        original_messagebox = sys.modules.get('tkinter.messagebox', None)
        error_message = None
        
        def mock_showerror(title, message):
            nonlocal error_message
            error_message = message
        
        sys.modules['tkinter.messagebox'] = type('obj', (object,), {
            'showerror': mock_showerror,
            'showinfo': lambda *args: None
        })
        
        try:
            self.game.make_move()
            
            # Check that the move was not made
            self.assertEqual(self.game.pegs, [[3, 2, 1], [], []])
            self.assertEqual(self.game.moves, [])
            self.assertEqual(error_message, "Source and destination pegs must be different")
        finally:
            # Restore messagebox
            if original_messagebox:
                sys.modules['tkinter.messagebox'] = original_messagebox
            else:
                del sys.modules['tkinter.messagebox']
    
    def test_make_move_invalid_empty_source(self):
        """Test making an invalid move from an empty peg."""
        # Set up a simple state
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # Try to make an invalid move (B to C)
        self.game.source_var = type('obj', (object,), {'get': lambda: 'B'})
        self.game.dest_var = type('obj', (object,), {'get': lambda: 'C'})
        
        # Mock messagebox
        original_messagebox = sys.modules.get('tkinter.messagebox', None)
        error_message = None
        
        def mock_showerror(title, message):
            nonlocal error_message
            error_message = message
        
        sys.modules['tkinter.messagebox'] = type('obj', (object,), {
            'showerror': mock_showerror,
            'showinfo': lambda *args: None
        })
        
        try:
            self.game.make_move()
            
            # Check that the move was not made
            self.assertEqual(self.game.pegs, [[3, 2, 1], [], []])
            self.assertEqual(self.game.moves, [])
            self.assertEqual(error_message, "Peg B is empty")
        finally:
            # Restore messagebox
            if original_messagebox:
                sys.modules['tkinter.messagebox'] = original_messagebox
            else:
                del sys.modules['tkinter.messagebox']
    
    def test_make_move_invalid_larger_on_smaller(self):
        """Test making an invalid move placing a larger disk on a smaller one."""
        # Set up a state where a larger disk would be placed on a smaller one
        self.game.num_disks = 3
        self.game.pegs = [[3, 2], [], [1]]
        
        # Try to make an invalid move (A to C)
        self.game.source_var = type('obj', (object,), {'get': lambda: 'A'})
        self.game.dest_var = type('obj', (object,), {'get': lambda: 'C'})
        
        # Mock messagebox
        original_messagebox = sys.modules.get('tkinter.messagebox', None)
        error_message = None
        
        def mock_showerror(title, message):
            nonlocal error_message
            error_message = message
        
        sys.modules['tkinter.messagebox'] = type('obj', (object,), {
            'showerror': mock_showerror,
            'showinfo': lambda *args: None
        })
        
        try:
            self.game.make_move()
            
            # Check that the move was not made
            self.assertEqual(self.game.pegs, [[3, 2], [], [1]])
            self.assertEqual(self.game.moves, [])
            self.assertEqual(error_message, "A larger disk cannot be placed on a smaller disk")
        finally:
            # Restore messagebox
            if original_messagebox:
                sys.modules['tkinter.messagebox'] = original_messagebox
            else:
                del sys.modules['tkinter.messagebox']
    
    def test_verify_solution_valid(self):
        """Test verifying a valid solution."""
        # Set up a simple game
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # A valid solution for 3 disks
        moves = [
            ('A', 'C'), ('A', 'B'), ('C', 'B'),
            ('A', 'C'), ('B', 'A'), ('B', 'C'),
            ('A', 'C')
        ]
        
        is_valid, message = self.game.verify_solution(moves)
        
        self.assertTrue(is_valid)
        self.assertIn("Solution is valid", message)
    
    def test_verify_solution_invalid_empty_source(self):
        """Test verifying an invalid solution with an empty source peg."""
        # Set up a simple game
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # An invalid solution (trying to move from an empty peg)
        moves = [
            ('A', 'C'), ('B', 'A')  # B is empty
        ]
        
        is_valid, message = self.game.verify_solution(moves)
        
        self.assertFalse(is_valid)
        self.assertIn("Peg B is empty", message)
    
    def test_verify_solution_invalid_larger_on_smaller(self):
        """Test verifying an invalid solution placing a larger disk on a smaller one."""
        # Set up a simple game
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # An invalid solution (trying to place a larger disk on a smaller one)
        moves = [
            ('A', 'C'),  # Move disk 1 to C
            ('A', 'C')   # Try to move disk 2 to C (invalid)
        ]
        
        is_valid, message = self.game.verify_solution(moves)
        
        self.assertFalse(is_valid)
        self.assertIn("A larger disk cannot be placed on a smaller disk", message)
    
    def test_verify_solution_incomplete(self):
        """Test verifying an incomplete solution."""
        # Set up a simple game
        self.game.num_disks = 3
        self.game.pegs = [[3, 2, 1], [], []]
        
        # An incomplete solution (not all disks end up on peg C)
        moves = [
            ('A', 'C'), ('A', 'B')  # Only moved 2 disks
        ]
        
        is_valid, message = self.game.verify_solution(moves)
        
        self.assertFalse(is_valid)
        self.assertIn("Not all disks are on the destination peg", message)
    
    def test_solve_recursive(self):
        """Test the recursive solution algorithm."""
        # Set up a simple game
        self.game.num_disks = 3
        
        # Get the solution
        moves, _ = self.game.solve_recursive()
        
        # Check that the solution is valid
        is_valid, _ = self.game.verify_solution(moves)
        self.assertTrue(is_valid)
        
        # Check that the solution has the optimal number of moves
        self.assertEqual(len(moves), 2**3 - 1)
    
    def test_solve_iterative(self):
        """Test the iterative solution algorithm."""
        # Set up a simple game
        self.game.num_disks = 3
        
        # Get the solution
        moves, _ = self.game.solve_iterative()
        
        # Check that the solution is valid
        is_valid, _ = self.game.verify_solution(moves)
        self.assertTrue(is_valid)
        
        # Check that the solution has the optimal number of moves
        self.assertEqual(len(moves), 2**3 - 1)
    
    def test_solutions_match(self):
        """Test that recursive and iterative solutions produce the same result."""
        # Set up a simple game
        self.game.num_disks = 3
        
        # Get both solutions
        recursive_moves, _ = self.game.solve_recursive()
        iterative_moves, _ = self.game.solve_iterative()
        
        # Check that both solutions have the same number of moves
        self.assertEqual(len(recursive_moves), len(iterative_moves))
        
        # Check that both solutions are valid
        is_valid_recursive, _ = self.game.verify_solution(recursive_moves)
        is_valid_iterative, _ = self.game.verify_solution(iterative_moves)
        
        self.assertTrue(is_valid_recursive)
        self.assertTrue(is_valid_iterative)
    
    def test_new_game(self):
        """Test starting a new game."""
        # Set up a game in progress
        self.game.num_disks = 3
        self.game.pegs = [[3], [2], [1]]
        self.game.moves = [('A', 'C'), ('A', 'B'), ('C', 'B')]
        
        # Mock UI elements
        self.game.history_text = type('obj', (object,), {'delete': lambda *args: None})
        self.game.num_moves_entry = type('obj', (object,), {'delete': lambda *args: None})
        self.game.sequence_entry = type('obj', (object,), {'delete': lambda *args: None})
        self.game.performance_label = type('obj', (object,), {'config': lambda **kwargs: None})
        self.game.status_label = type('obj', (object,), {'config': lambda **kwargs: None})
        self.game.root = type('obj', (object,), {'winfo_children': lambda: []})
        
        # Start a new game
        original_num_disks = self.game.num_disks
        self.game.new_game()
        
        # Check that the game state was reset
        self.assertTrue(5 <= self.game.num_disks <= 10)
        self.assertEqual(len(self.game.pegs[0]), self.game.num_disks)
        self.assertEqual(len(self.game.pegs[1]), 0)
        self.assertEqual(len(self.game.pegs[2]), 0)
        self.assertEqual(self.game.moves, [])
        self.assertEqual(self.game.optimal_move_count, 2**self.game.num_disks - 1)
    
    def test_save_game_result(self):
        """Test saving game results to the database."""
        # Set up a game
        self.game.num_disks = 3
        self.game.moves = [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C')]
        
        # Save the game result
        self.game.save_game_result(True)
        
        # Check that the result was saved
        self.assertEqual(len(self.db.game_results), 1)
        result = list(self.db.game_results.values())[0]
        self.assertEqual(result['correct_answer'], "correct")
        
        # Check that the Tower of Hanoi specific data was saved
        self.assertEqual(len(self.db.tower_of_hanoi_games), 1)
        game_data = list(self.db.tower_of_hanoi_games.values())[0]
        self.assertEqual(game_data['num_disks'], 3)
        self.assertEqual(game_data['move_sequence'], "A->C,A->B,C->B,A->C")


if __name__ == "__main__":
    unittest.main()
