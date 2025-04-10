"""
Unit tests for the Tic-Tac-Toe game.
"""
import unittest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame, MCTSNode

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.players = {}
        self.games = {}
        self.game_results = {}
        self.algorithm_performance = {}
        self.tic_tac_toe_games = {}
    
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
    
    def add_tic_tac_toe_game(self, game_id, board_state, winner):
        """Record a Tic-Tac-Toe game."""
        game_record_id = len(self.tic_tac_toe_games) + 1
        self.tic_tac_toe_games[game_record_id] = {
            'game_id': game_id,
            'board_state': board_state,
            'winner': winner
        }
        return game_record_id


class TestTicTacToeGame(unittest.TestCase):
    """Test cases for the Tic-Tac-Toe game."""
    
    def setUp(self):
        """Set up test environment."""
        self.db = MockDatabase()
        # Create a headless game instance for testing
        self.game = TicTacToeGame(None, "TestPlayer", self.db, lambda w: None)
        # Override UI-related methods
        self.game.update_board_ui = lambda: None
        self.game.update_status = lambda: None
    
    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertEqual(self.game.board_size, 5)
        self.assertEqual(self.game.current_player, 1)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertEqual(np.count_nonzero(self.game.board == 0), 25)  # All cells empty
    
    def test_make_move(self):
        """Test making a move on the board."""
        # Make a move
        self.game.make_move(0, 0)
        
        # Check that the move was made
        self.assertEqual(self.game.board[0, 0], 1)
        
        # Check that the player switched
        self.assertEqual(self.game.current_player, -1)
        
        # Try to make a move on an occupied cell
        self.game.current_player = 1  # Switch back to human for testing
        self.game.make_move(0, 0)
        
        # Check that the move was not made (cell still has value 1)
        self.assertEqual(self.game.board[0, 0], 1)
    
    def test_check_win_horizontal(self):
        """Test win detection for horizontal lines."""
        # Create a horizontal line of 4 X's
        self.game.board[0, 0:4] = 1
        
        # Check for win
        self.assertTrue(self.game.check_win())
        
        # Reset board
        self.game.board = np.zeros((5, 5), dtype=int)
        
        # Create a horizontal line of 4 O's
        self.game.board[1, 1:5] = -1
        
        # Check for win
        self.assertTrue(self.game.check_win())
    
    def test_check_win_vertical(self):
        """Test win detection for vertical lines."""
        # Create a vertical line of 4 X's
        self.game.board[0:4, 0] = 1
        
        # Check for win
        self.assertTrue(self.game.check_win())
        
        # Reset board
        self.game.board = np.zeros((5, 5), dtype=int)
        
        # Create a vertical line of 4 O's
        self.game.board[1:5, 1] = -1
        
        # Check for win
        self.assertTrue(self.game.check_win())
    
    def test_check_win_diagonal(self):
        """Test win detection for diagonal lines."""
        # Create a diagonal line of 4 X's (top-left to bottom-right)
        for i in range(4):
            self.game.board[i, i] = 1
        
        # Check for win
        self.assertTrue(self.game.check_win())
        
        # Reset board
        self.game.board = np.zeros((5, 5), dtype=int)
        
        # Create a diagonal line of 4 O's (bottom-left to top-right)
        for i in range(4):
            self.game.board[4-i, i] = -1
        
        # Check for win
        self.assertTrue(self.game.check_win())
    
    def test_check_draw(self):
        """Test draw detection."""
        # Fill the board with alternating X's and O's (no win)
        for i in range(5):
            for j in range(5):
                self.game.board[i, j] = 1 if (i + j) % 2 == 0 else -1
        
        # Check for draw
        self.assertTrue(self.game.check_draw())
        
        # Reset board
        self.game.board = np.zeros((5, 5), dtype=int)
        
        # Leave one cell empty
        for i in range(5):
            for j in range(5):
                if i != 4 or j != 4:
                    self.game.board[i, j] = 1 if (i + j) % 2 == 0 else -1
        
        # Check for draw (should be false)
        self.assertFalse(self.game.check_draw())
    
    def test_minimax_move(self):
        """Test that minimax algorithm returns a valid move."""
        # Set up a board state
        self.game.board[0, 0] = 1  # Human
        self.game.board[1, 1] = -1  # Computer
        
        # Get minimax move
        move, _ = self.game.minimax_move()
        
        # Check that the move is valid
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        row, col = move
        self.assertTrue(0 <= row < 5 and 0 <= col < 5)
        self.assertEqual(self.game.board[row, col], 0)  # Cell should be empty
    
    def test_mcts_move(self):
        """Test that MCTS algorithm returns a valid move."""
        # Set up a board state
        self.game.board[0, 0] = 1  # Human
        self.game.board[1, 1] = -1  # Computer
        
        # Get MCTS move
        move, _ = self.game.mcts_move()
        
        # Check that the move is valid
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        row, col = move
        self.assertTrue(0 <= row < 5 and 0 <= col < 5)
        self.assertEqual(self.game.board[row, col], 0)  # Cell should be empty
    
    def test_blocking_move(self):
        """Test that the AI makes a blocking move when necessary."""
        # Set up a board state where human is about to win
        self.game.board[0, 0:3] = 1  # Human has 3 in a row
        
        # Set algorithm to minimax
        self.game.algorithm = "minimax"
        
        # Get minimax move
        move, _ = self.game.minimax_move()
        
        # Check that the move blocks the win
        self.assertEqual(move, (0, 3))
    
    def test_winning_move(self):
        """Test that the AI makes a winning move when possible."""
        # Set up a board state where computer is about to win
        self.game.board[0, 0:3] = -1  # Computer has 3 in a row
        
        # Set algorithm to minimax
        self.game.algorithm = "minimax"
        
        # Get minimax move
        move, _ = self.game.minimax_move()
        
        # Check that the move completes the win
        self.assertEqual(move, (0, 3))
    
    def test_new_game(self):
        """Test starting a new game."""
        # Make some moves
        self.game.make_move(0, 0)
        self.game.board[1, 1] = -1  # Simulate computer move
        
        # Start a new game
        self.game.new_game()
        
        # Check that the board is reset
        self.assertEqual(np.count_nonzero(self.game.board == 0), 25)  # All cells empty
        self.assertEqual(self.game.current_player, 1)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
    
    def test_save_game_result(self):
        """Test saving game results to the database."""
        # Set up a win for the human player
        self.game.game_over = True
        self.game.winner = 1
        
        # Save the game result
        self.game.save_game_result()
        
        # Check that the result was saved
        self.assertEqual(len(self.db.game_results), 1)
        result = list(self.db.game_results.values())[0]
        self.assertEqual(result['correct_answer'], "win")
        
        # Check that the Tic-Tac-Toe specific data was saved
        self.assertEqual(len(self.db.tic_tac_toe_games), 1)
        game_data = list(self.db.tic_tac_toe_games.values())[0]
        self.assertEqual(game_data['winner'], "X")


class TestMCTSNode(unittest.TestCase):
    """Test cases for the MCTS node."""
    
    def setUp(self):
        """Set up test environment."""
        # Create an empty 5x5 board
        self.board = np.zeros((5, 5), dtype=int)
        # Create a root node
        self.root = MCTSNode(self.board.copy(), None, None, -1)
    
    def test_initial_state(self):
        """Test the initial state of the node."""
        self.assertIsNone(self.root.parent)
        self.assertIsNone(self.root.move)
        self.assertEqual(self.root.player, -1)
        self.assertEqual(len(self.root.children), 0)
        self.assertEqual(self.root.wins, 0)
        self.assertEqual(self.root.visits, 0)
        self.assertEqual(len(self.root.untried_moves), 25)  # All cells are untried
    
    def test_expand(self):
        """Test node expansion."""
        # Expand the root node
        child = self.root.expand()
        
        # Check that a child was created
        self.assertEqual(len(self.root.children), 1)
        self.assertEqual(self.root.children[0], child)
        
        # Check that the child has the correct properties
        self.assertEqual(child.parent, self.root)
        self.assertIsNotNone(child.move)
        self.assertEqual(child.player, 1)  # Switched from -1
        self.assertEqual(len(child.children), 0)
        self.assertEqual(child.wins, 0)
        self.assertEqual(child.visits, 0)
        self.assertEqual(len(child.untried_moves), 24)  # One move has been tried
        
        # Check that the move was made on the board
        row, col = child.move
        self.assertEqual(child.board[row, col], 1)
    
    def test_is_fully_expanded(self):
        """Test checking if a node is fully expanded."""
        # Initially, the root is not fully expanded
        self.assertFalse(self.root.is_fully_expanded())
        
        # Expand all possible moves
        for _ in range(25):
            self.root.expand()
        
        # Now the root should be fully expanded
        self.assertTrue(self.root.is_fully_expanded())
    
    def test_best_child(self):
        """Test selecting the best child."""
        # Create some children with different win rates
        for _ in range(3):
            child = self.root.expand()
            child.visits = 10
        
        # Set different win rates
        self.root.children[0].wins = 3  # 30% win rate
        self.root.children[1].wins = 5  # 50% win rate
        self.root.children[2].wins = 7  # 70% win rate
        
        # Set root visits
        self.root.visits = 30
        
        # Get the best child
        best = self.root.best_child(c_param=0)  # Ignore exploration term for this test
        
        # Check that the best child is the one with the highest win rate
        self.assertEqual(best, self.root.children[2])


if __name__ == "__main__":
    unittest.main()
