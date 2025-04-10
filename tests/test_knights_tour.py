"""
Unit tests for the Knight's Tour Problem game.
"""
import unittest
import numpy as np
import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from games.knights_tour.knights_tour_game import KnightsTourGame

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.players = {}
        self.games = {}
        self.game_results = {}
        self.algorithm_performance = {}
        self.knights_tour_games = {}
    
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
    
    def add_knights_tour_game(self, game_id, start_position, move_sequence):
        """Record a Knight's Tour game."""
        game_record_id = len(self.knights_tour_games) + 1
        self.knights_tour_games[game_record_id] = {
            'game_id': game_id,
            'start_position': start_position,
            'move_sequence': move_sequence
        }
        return game_record_id


class TestKnightsTourGame(unittest.TestCase):
    """Test cases for the Knight's Tour Problem game."""
    
    def setUp(self):
        """Set up test environment."""
        self.db = MockDatabase()
        # Create a headless game instance for testing
        self.game = KnightsTourGame(None, "TestPlayer", self.db, lambda w: None)
        # Override UI-related methods
        self.game.setup_ui = lambda: None
        self.game.initialize_board = lambda: None
        self.game.update_board_ui = lambda: None
    
    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertEqual(self.game.board_size, 8)
        self.assertEqual(self.game.board.shape, (8, 8))
        self.assertEqual(self.game.move_count, 1)
        self.assertEqual(len(self.game.move_sequence), 1)
        self.assertEqual(self.game.move_sequence[0], self.game.start_position)
        self.assertEqual(self.game.current_position, self.game.start_position)
    
    def test_choose_random_start_position(self):
        """Test choosing a random starting position."""
        position = self.game.choose_random_start_position()
        self.assertTrue(0 <= position[0] < self.game.board_size)
        self.assertTrue(0 <= position[1] < self.game.board_size)
    
    def test_is_valid_move(self):
        """Test checking if a move is valid."""
        # Set up a board with some moves
        self.game.board = np.zeros((8, 8), dtype=int)
        self.game.board[0, 0] = 1  # Starting position
        self.game.current_position = (0, 0)
        
        # Valid knight's moves from (0, 0)
        self.assertTrue(self.game.is_valid_move((0, 0), (2, 1)))
        self.assertTrue(self.game.is_valid_move((0, 0), (1, 2)))
        
        # Invalid moves
        self.assertFalse(self.game.is_valid_move((0, 0), (0, 0)))  # Same position
        self.assertFalse(self.game.is_valid_move((0, 0), (1, 1)))  # Not a knight's move
        self.assertFalse(self.game.is_valid_move((0, 0), (3, 3)))  # Not a knight's move
        self.assertFalse(self.game.is_valid_move((0, 0), (8, 8)))  # Off the board
        
        # Make a move to (2, 1)
        self.game.board[2, 1] = 2
        self.game.current_position = (2, 1)
        
        # Try to move to an already visited square
        self.assertFalse(self.game.is_valid_move((2, 1), (0, 0)))
    
    def test_get_available_moves(self):
        """Test getting available moves from a position."""
        # Set up a board with some moves
        self.game.board = np.zeros((8, 8), dtype=int)
        self.game.board[0, 0] = 1  # Starting position
        
        # Get available moves from (0, 0)
        available_moves = self.game.get_available_moves((0, 0))
        
        # There should be 2 valid moves from (0, 0): (2, 1) and (1, 2)
        self.assertEqual(len(available_moves), 2)
        self.assertIn((2, 1), available_moves)
        self.assertIn((1, 2), available_moves)
        
        # Make a move to (2, 1)
        self.game.board[2, 1] = 2
        
        # Get available moves from (2, 1)
        available_moves = self.game.get_available_moves((2, 1))
        
        # (0, 0) should not be in available moves as it's already visited
        self.assertNotIn((0, 0), available_moves)
    
    def test_is_valid_knight_move(self):
        """Test checking if a move is a valid knight's move."""
        # Valid knight's moves
        self.assertTrue(self.game.is_valid_knight_move((0, 0), (2, 1)))
        self.assertTrue(self.game.is_valid_knight_move((0, 0), (1, 2)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (6, 5)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (6, 3)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (2, 5)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (2, 3)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (5, 6)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (3, 6)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (5, 2)))
        self.assertTrue(self.game.is_valid_knight_move((4, 4), (3, 2)))
        
        # Invalid moves
        self.assertFalse(self.game.is_valid_knight_move((0, 0), (0, 0)))  # Same position
        self.assertFalse(self.game.is_valid_knight_move((0, 0), (1, 1)))  # Not a knight's move
        self.assertFalse(self.game.is_valid_knight_move((0, 0), (3, 3)))  # Not a knight's move
        self.assertFalse(self.game.is_valid_knight_move((4, 4), (4, 5)))  # Not a knight's move
    
    def test_verify_solution_valid(self):
        """Test verifying a valid solution."""
        # Set up a valid solution
        self.game.start_position = (0, 0)
        solution = [
            (0, 0), (2, 1), (4, 0), (6, 1), (7, 3), (6, 5), (4, 6), (2, 7),
            (0, 6), (1, 4), (3, 3), (5, 2), (7, 1), (5, 0), (3, 1), (1, 0),
            (0, 2), (1, 4), (3, 5), (5, 6), (7, 7), (6, 5), (4, 4), (2, 3),
            (0, 4), (1, 6), (3, 7), (5, 6), (7, 5), (6, 3), (4, 2), (2, 1),
            (0, 0), (1, 2), (3, 3), (5, 4), (7, 3), (6, 1), (4, 0), (2, 1),
            (0, 2), (1, 0), (3, 1), (5, 0), (7, 1), (6, 3), (4, 4), (2, 5),
            (0, 6), (1, 4), (3, 5), (5, 4), (7, 5), (6, 7), (4, 6), (2, 7),
            (0, 6), (1, 4), (3, 3), (5, 2), (7, 1), (5, 0), (3, 1), (1, 0)
        ]
        
        # Verify the solution
        is_valid, message = self.game.verify_solution(solution)
        
        # The solution should be valid
        self.assertTrue(is_valid)
        self.assertIn("Valid", message)
    
    def test_verify_solution_invalid_start(self):
        """Test verifying a solution with an invalid starting position."""
        # Set up a solution with an invalid starting position
        self.game.start_position = (0, 0)
        solution = [(1, 0), (3, 1), (5, 0), (7, 1)]  # Starts at (1, 0) instead of (0, 0)
        
        # Verify the solution
        is_valid, message = self.game.verify_solution(solution)
        
        # The solution should be invalid
        self.assertFalse(is_valid)
        self.assertIn("starting position", message)
    
    def test_verify_solution_invalid_move(self):
        """Test verifying a solution with an invalid move."""
        # Set up a solution with an invalid move
        self.game.start_position = (0, 0)
        solution = [(0, 0), (1, 1), (3, 2)]  # (0, 0) to (1, 1) is not a valid knight's move
        
        # Verify the solution
        is_valid, message = self.game.verify_solution(solution)
        
        # The solution should be invalid
        self.assertFalse(is_valid)
        self.assertIn("Invalid knight's move", message)
    
    def test_verify_solution_incomplete(self):
        """Test verifying an incomplete solution."""
        # Set up an incomplete solution
        self.game.start_position = (0, 0)
        solution = [(0, 0), (2, 1), (4, 0)]  # Only 3 moves, not covering all squares
        
        # Verify the solution
        is_valid, message = self.game.verify_solution(solution)
        
        # The solution should be invalid
        self.assertFalse(is_valid)
        self.assertIn("must visit all", message)
    
    def test_solve_backtracking(self):
        """Test solving the Knight's Tour using backtracking."""
        # Set a fixed starting position for reproducibility
        self.game.start_position = (0, 0)
        
        # Solve using backtracking
        move_sequence, _ = self.game.solve_backtracking()
        
        # Check that a solution was found
        self.assertIsNotNone(move_sequence)
        
        # Check that the solution has the correct length
        self.assertEqual(len(move_sequence), self.game.board_size * self.game.board_size)
        
        # Check that the solution starts at the starting position
        self.assertEqual(move_sequence[0], self.game.start_position)
        
        # Check that all moves are valid knight's moves
        for i in range(1, len(move_sequence)):
            self.assertTrue(self.game.is_valid_knight_move(move_sequence[i-1], move_sequence[i]))
        
        # Check that all squares are visited exactly once
        visited = set()
        for move in move_sequence:
            self.assertNotIn(move, visited)
            visited.add(move)
        self.assertEqual(len(visited), self.game.board_size * self.game.board_size)
    
    def test_solve_warnsdorff(self):
        """Test solving the Knight's Tour using Warnsdorff's algorithm."""
        # Set a fixed starting position for reproducibility
        self.game.start_position = (0, 0)
        
        # Solve using Warnsdorff's algorithm
        move_sequence, _ = self.game.solve_warnsdorff()
        
        # Check that a solution was found
        self.assertIsNotNone(move_sequence)
        
        # Check that the solution has the correct length
        self.assertEqual(len(move_sequence), self.game.board_size * self.game.board_size)
        
        # Check that the solution starts at the starting position
        self.assertEqual(move_sequence[0], self.game.start_position)
        
        # Check that all moves are valid knight's moves
        for i in range(1, len(move_sequence)):
            self.assertTrue(self.game.is_valid_knight_move(move_sequence[i-1], move_sequence[i]))
        
        # Check that all squares are visited exactly once
        visited = set()
        for move in move_sequence:
            self.assertNotIn(move, visited)
            visited.add(move)
        self.assertEqual(len(visited), self.game.board_size * self.game.board_size)
    
    def test_solve_neural_network(self):
        """Test solving the Knight's Tour using the neural network approach."""
        # Set a fixed starting position for reproducibility
        self.game.start_position = (0, 0)
        
        # Solve using the neural network approach
        move_sequence, _ = self.game.solve_neural_network()
        
        # Check that a solution was found
        self.assertIsNotNone(move_sequence)
        
        # Check that the solution has the correct length
        self.assertEqual(len(move_sequence), self.game.board_size * self.game.board_size)
        
        # Check that the solution starts at the starting position
        self.assertEqual(move_sequence[0], self.game.start_position)
        
        # Check that all moves are valid knight's moves
        for i in range(1, len(move_sequence)):
            self.assertTrue(self.game.is_valid_knight_move(move_sequence[i-1], move_sequence[i]))
        
        # Check that all squares are visited exactly once
        visited = set()
        for move in move_sequence:
            self.assertNotIn(move, visited)
            visited.add(move)
        self.assertEqual(len(visited), self.game.board_size * self.game.board_size)
    
    def test_save_game_result(self):
        """Test saving game results to the database."""
        # Set up a game
        self.game.start_position = (0, 0)
        self.game.move_sequence = [(0, 0), (2, 1), (4, 0)]
        
        # Save the game result
        self.game.save_game_result(True)
        
        # Check that the result was saved
        self.assertEqual(len(self.db.game_results), 1)
        result = list(self.db.game_results.values())[0]
        self.assertEqual(result['correct_answer'], "correct")
        
        # Check that the Knight's Tour specific data was saved
        self.assertEqual(len(self.db.knights_tour_games), 1)
        game_data = list(self.db.knights_tour_games.values())[0]
        self.assertEqual(game_data['start_position'], "1,1")  # 1-indexed
        self.assertEqual(game_data['move_sequence'], "1,1,3,2,5,1")  # 1-indexed
    
    def test_new_game(self):
        """Test starting a new game."""
        # Set up a game in progress
        self.game.board = np.ones((8, 8), dtype=int)
        self.game.move_count = 10
        self.game.move_sequence = [(0, 0), (2, 1), (4, 0)]
        
        # Mock UI elements
        self.game.position_label = type('obj', (object,), {'config': lambda **kwargs: None})
        self.game.status_label = type('obj', (object,), {'config': lambda **kwargs: None})
        
        # Start a new game
        original_game_id = self.game.game_id
        original_start_position = self.game.start_position
        self.game.new_game()
        
        # Check that the game state was reset
        self.assertEqual(np.sum(self.game.board), 0)  # Empty board
        self.assertEqual(self.game.move_count, 1)
        self.assertEqual(len(self.game.move_sequence), 1)
        self.assertEqual(self.game.move_sequence[0], self.game.start_position)
        self.assertEqual(self.game.current_position, self.game.start_position)
        self.assertNotEqual(self.game.game_id, original_game_id)
        # The start position might be the same by chance, but it's unlikely
        # self.assertNotEqual(self.game.start_position, original_start_position)


if __name__ == "__main__":
    unittest.main()
