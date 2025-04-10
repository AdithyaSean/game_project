"""
Unit tests for the Eight Queens Puzzle game.
"""
import unittest
import numpy as np
import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from games.eight_queens.eight_queens_game import EightQueensPuzzleGame

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.players = {}
        self.games = {}
        self.game_results = {}
        self.algorithm_performance = {}
        self.eight_queens_games = {}
    
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
    
    def add_eight_queens_game(self, game_id, solution_config, is_recognized):
        """Record an Eight Queens game."""
        game_record_id = len(self.eight_queens_games) + 1
        self.eight_queens_games[game_record_id] = {
            'game_id': game_id,
            'solution_config': solution_config,
            'is_recognized': is_recognized
        }
        return game_record_id
    
    def check_eight_queens_solution_exists(self, solution_config):
        """Check if a solution for Eight Queens puzzle has already been recognized."""
        for record in self.eight_queens_games.values():
            if record['solution_config'] == solution_config and record['is_recognized']:
                return True
        return False
    
    def clear_eight_queens_recognition_flags(self):
        """Clear the recognition flags for all Eight Queens solutions."""
        for record_id in self.eight_queens_games:
            self.eight_queens_games[record_id]['is_recognized'] = False
        return True


class TestEightQueensPuzzleGame(unittest.TestCase):
    """Test cases for the Eight Queens Puzzle game."""
    
    def setUp(self):
        """Set up test environment."""
        self.db = MockDatabase()
        # Create a headless game instance for testing
        self.game = EightQueensPuzzleGame(None, "TestPlayer", self.db, lambda w: None)
        # Override UI-related methods
        self.game.setup_ui = lambda: None
        self.game.find_all_solutions = lambda: None
        self.game.solutions = []  # Will be populated in tests
    
    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertEqual(self.game.board_size, 8)
        self.assertEqual(self.game.board.shape, (8, 8))
        self.assertEqual(np.sum(self.game.board), 0)  # Empty board
        self.assertEqual(self.game.recognized_solutions, set())
        self.assertEqual(self.game.max_solutions, 92)  # Total number of solutions for 8 queens
    
    def test_toggle_queen(self):
        """Test toggling a queen on the board."""
        # Mock the buttons
        self.game.buttons = [[type('obj', (object,), {'config': lambda **kwargs: None}) for _ in range(8)] for _ in range(8)]
        
        # Toggle a queen on
        self.game.toggle_queen(0, 0)
        self.assertEqual(self.game.board[0, 0], 1)
        
        # Toggle the same queen off
        self.game.toggle_queen(0, 0)
        self.assertEqual(self.game.board[0, 0], 0)
    
    def test_clear_board(self):
        """Test clearing the board."""
        # Set up a board with some queens
        self.game.board = np.zeros((8, 8), dtype=int)
        self.game.board[0, 0] = 1
        self.game.board[1, 2] = 1
        self.game.board[2, 4] = 1
        
        # Mock the buttons
        self.game.buttons = [[type('obj', (object,), {'config': lambda **kwargs: None}) for _ in range(8)] for _ in range(8)]
        
        # Clear the board
        self.game.clear_board()
        
        # Check that the board is empty
        self.assertEqual(np.sum(self.game.board), 0)
    
    def test_is_valid_solution_valid(self):
        """Test checking a valid solution."""
        # Set up a valid solution
        board = np.zeros((8, 8), dtype=int)
        # Place queens in a valid configuration
        # This is one of the 92 solutions
        board[0, 0] = 1
        board[1, 4] = 1
        board[2, 7] = 1
        board[3, 5] = 1
        board[4, 2] = 1
        board[5, 6] = 1
        board[6, 1] = 1
        board[7, 3] = 1
        
        self.assertTrue(self.game.is_valid_solution(board))
    
    def test_is_valid_solution_invalid_row(self):
        """Test checking an invalid solution with queens in the same row."""
        # Set up an invalid solution with queens in the same row
        board = np.zeros((8, 8), dtype=int)
        board[0, 0] = 1
        board[0, 1] = 1  # Same row as the first queen
        
        self.assertFalse(self.game.is_valid_solution(board))
    
    def test_is_valid_solution_invalid_column(self):
        """Test checking an invalid solution with queens in the same column."""
        # Set up an invalid solution with queens in the same column
        board = np.zeros((8, 8), dtype=int)
        board[0, 0] = 1
        board[1, 0] = 1  # Same column as the first queen
        
        self.assertFalse(self.game.is_valid_solution(board))
    
    def test_is_valid_solution_invalid_diagonal(self):
        """Test checking an invalid solution with queens in the same diagonal."""
        # Set up an invalid solution with queens in the same diagonal
        board = np.zeros((8, 8), dtype=int)
        board[0, 0] = 1
        board[1, 1] = 1  # Same diagonal as the first queen
        
        self.assertFalse(self.game.is_valid_solution(board))
    
    def test_board_to_solution_string(self):
        """Test converting a board to a solution string."""
        # Set up a board
        board = np.zeros((8, 8), dtype=int)
        board[0, 0] = 1
        board[1, 1] = 1
        board[2, 2] = 1
        board[3, 3] = 1
        board[4, 4] = 1
        board[5, 5] = 1
        board[6, 6] = 1
        board[7, 7] = 1
        
        # Expected solution string: row indices + 1 for each column
        expected = "12345678"
        
        self.assertEqual(self.game.board_to_solution_string(board), expected)
    
    def test_solution_string_to_board(self):
        """Test converting a solution string to a board."""
        # Set up a solution string
        solution_str = "12345678"
        
        # Expected board
        expected = np.zeros((8, 8), dtype=int)
        expected[0, 0] = 1
        expected[1, 1] = 1
        expected[2, 2] = 1
        expected[3, 3] = 1
        expected[4, 4] = 1
        expected[5, 5] = 1
        expected[6, 6] = 1
        expected[7, 7] = 1
        
        # Convert to board
        board = self.game.solution_string_to_board(solution_str)
        
        # Check that the board matches the expected board
        self.assertTrue(np.array_equal(board, expected))
    
    def test_is_safe(self):
        """Test checking if it's safe to place a queen."""
        # Set up a board
        board = np.zeros((8, 8), dtype=int)
        board[0, 0] = 1  # Queen at (0, 0)
        
        # Check safe positions
        self.assertTrue(self.game.is_safe(board, 2, 1))  # Safe position
        
        # Check unsafe positions
        self.assertFalse(self.game.is_safe(board, 0, 1))  # Same row
        self.assertFalse(self.game.is_safe(board, 1, 1))  # Same diagonal
    
    def test_find_all_solutions_backtracking(self):
        """Test finding all solutions using backtracking."""
        # Run the backtracking algorithm
        solutions, _ = self.game.find_all_solutions_backtracking()
        
        # Check that we found the correct number of solutions
        self.assertEqual(len(solutions), 92)
        
        # Check that all solutions are valid
        for solution in solutions:
            self.assertTrue(self.game.is_valid_solution(solution))
            self.assertEqual(np.sum(solution), 8)  # 8 queens
    
    def test_find_all_solutions_genetic(self):
        """Test finding solutions using genetic algorithm."""
        # Run the genetic algorithm
        solutions, _ = self.game.find_all_solutions_genetic()
        
        # Check that we found at least one solution
        self.assertGreater(len(solutions), 0)
        
        # Check that all solutions are valid
        for solution in solutions:
            self.assertTrue(self.game.is_valid_solution(solution))
            self.assertEqual(np.sum(solution), 8)  # 8 queens
    
    def test_calculate_fitness(self):
        """Test calculating fitness for genetic algorithm."""
        # Set up an individual with no conflicts (a valid solution)
        # This represents the row indices of queens in each column
        individual = [0, 4, 7, 5, 2, 6, 1, 3]
        
        # Calculate fitness
        fitness = self.game.calculate_fitness(individual)
        
        # Maximum fitness for 8 queens is 28 (no conflicts)
        self.assertEqual(fitness, 28)
        
        # Set up an individual with conflicts
        individual = [0, 1, 2, 3, 4, 5, 6, 7]  # All queens on the same diagonal
        
        # Calculate fitness
        fitness = self.game.calculate_fitness(individual)
        
        # Should be less than 28 due to conflicts
        self.assertLess(fitness, 28)
    
    def test_tournament_selection(self):
        """Test tournament selection for genetic algorithm."""
        # Set up a population and fitness scores
        population = [[0, 1, 2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2, 1, 0], [0, 4, 7, 5, 2, 6, 1, 3]]
        fitness_scores = [10, 15, 28]  # Third individual is the fittest
        
        # Mock random selection of tournament participants
        random.seed(42)  # For reproducibility
        
        # Run tournament selection
        selected = self.game.tournament_selection(population, fitness_scores)
        
        # Check that the selected individual is the fittest in the tournament
        # With the given seed, the third individual should be selected
        self.assertEqual(selected, population[2])
    
    def test_ordered_crossover(self):
        """Test ordered crossover for genetic algorithm."""
        # Set up two parents
        parent1 = [0, 1, 2, 3, 4, 5, 6, 7]
        parent2 = [7, 6, 5, 4, 3, 2, 1, 0]
        
        # Mock random selection of crossover points
        random.seed(42)  # For reproducibility
        
        # Run ordered crossover
        child = self.game.ordered_crossover(parent1, parent2)
        
        # Check that the child has all values from 0 to 7 exactly once
        self.assertEqual(sorted(child), list(range(8)))
        
        # Check that the child has some elements from both parents
        # This is a probabilistic test, but with the seed it should be consistent
        self.assertTrue(any(child[i] == parent1[i] for i in range(8)))
        self.assertTrue(any(child[i] == parent2[i] for i in range(8)))
    
    def test_mutate(self):
        """Test mutation for genetic algorithm."""
        # Set up an individual
        individual = [0, 1, 2, 3, 4, 5, 6, 7]
        original = individual.copy()
        
        # Mock random selection of mutation points
        random.seed(42)  # For reproducibility
        
        # Run mutation
        self.game.mutate(individual)
        
        # Check that exactly two values were swapped
        differences = sum(1 for i in range(8) if individual[i] != original[i])
        self.assertEqual(differences, 2)
        
        # Check that the individual still has all values from 0 to 7
        self.assertEqual(sorted(individual), list(range(8)))
    
    def test_save_solution(self):
        """Test saving a solution to the database."""
        # Set up a solution string
        solution_str = "12345678"
        
        # Save the solution
        self.game.save_solution(solution_str)
        
        # Check that the solution was saved
        self.assertEqual(len(self.db.game_results), 1)
        result = list(self.db.game_results.values())[0]
        self.assertEqual(result['correct_answer'], "correct")
        
        # Check that the Eight Queens specific data was saved
        self.assertEqual(len(self.db.eight_queens_games), 1)
        game_data = list(self.db.eight_queens_games.values())[0]
        self.assertEqual(game_data['solution_config'], solution_str)
        self.assertTrue(game_data['is_recognized'])
    
    def test_new_game(self):
        """Test starting a new game."""
        # Set up a game in progress
        self.game.board = np.ones((8, 8), dtype=int)
        self.game.recognized_solutions = {"12345678"}
        self.game.current_solution_index = 10
        
        # Mock UI elements
        self.game.solution_listbox = type('obj', (object,), {'delete': lambda *args: None})
        self.game.solutions_label = type('obj', (object,), {'config': lambda **kwargs: None})
        
        # Start a new game
        original_game_id = self.game.game_id
        self.game.new_game()
        
        # Check that the game state was reset
        self.assertEqual(np.sum(self.game.board), 0)  # Empty board
        self.assertEqual(self.game.recognized_solutions, set())
        self.assertEqual(self.game.current_solution_index, 0)
        self.assertNotEqual(self.game.game_id, original_game_id)


if __name__ == "__main__":
    unittest.main()
