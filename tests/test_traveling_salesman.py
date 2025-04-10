"""
Unit tests for the Traveling Salesman Problem game.
"""
import unittest
import numpy as np
import sys
import os
import random

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from games.traveling_salesman.traveling_salesman_game import TravelingSalesmanGame

class MockDatabase:
    """Mock database for testing."""
    
    def __init__(self):
        self.players = {}
        self.games = {}
        self.game_results = {}
        self.algorithm_performance = {}
        self.tsp_games = {}
    
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
    
    def add_tsp_game(self, game_id, home_city, selected_cities, shortest_route):
        """Record a Traveling Salesman Problem game."""
        game_record_id = len(self.tsp_games) + 1
        self.tsp_games[game_record_id] = {
            'game_id': game_id,
            'home_city': home_city,
            'selected_cities': selected_cities,
            'shortest_route': shortest_route
        }
        return game_record_id


class TestTravelingSalesmanGame(unittest.TestCase):
    """Test cases for the Traveling Salesman Problem game."""
    
    def setUp(self):
        """Set up test environment."""
        self.db = MockDatabase()
        # Create a headless game instance for testing
        self.game = TravelingSalesmanGame(None, "TestPlayer", self.db, lambda w: None)
        # Override UI-related methods
        self.game.setup_ui = lambda: None
        self.game.display_results = lambda: None
        self.game.plot_cities = lambda route=None: None
    
    def test_initial_state(self):
        """Test the initial state of the game."""
        self.assertEqual(self.game.num_cities, 10)
        self.assertEqual(len(self.game.city_names), 10)
        self.assertEqual(self.game.distances.shape, (10, 10))
        self.assertTrue(0 <= self.game.home_city_index < 10)
        self.assertEqual(self.game.home_city, self.game.city_names[self.game.home_city_index])
        self.assertEqual(self.game.selected_cities, [])
        self.assertEqual(self.game.user_route, [])
    
    def test_distance_matrix_properties(self):
        """Test properties of the distance matrix."""
        # Check that distances are in the range 50-100
        for i in range(self.game.num_cities):
            for j in range(i + 1, self.game.num_cities):
                self.assertTrue(50 <= self.game.distances[i, j] <= 100)
                # Check symmetry
                self.assertEqual(self.game.distances[i, j], self.game.distances[j, i])
        
        # Check diagonal is zero
        for i in range(self.game.num_cities):
            self.assertEqual(self.game.distances[i, i], 0)
    
    def test_get_distance(self):
        """Test the get_distance method."""
        # Set up a known distance
        city1 = self.game.city_names[0]
        city2 = self.game.city_names[1]
        self.game.distances[0, 1] = 75
        self.game.distances[1, 0] = 75
        
        # Check that get_distance returns the correct value
        self.assertEqual(self.game.get_distance(city1, city2), 75)
        self.assertEqual(self.game.get_distance(city2, city1), 75)
    
    def test_calculate_route_distance(self):
        """Test the calculate_route_distance method."""
        # Set up known distances
        self.game.distances = np.zeros((self.game.num_cities, self.game.num_cities))
        for i in range(self.game.num_cities):
            for j in range(i + 1, self.game.num_cities):
                self.game.distances[i, j] = 50 + (i + j)
                self.game.distances[j, i] = 50 + (i + j)
        
        # Set home city
        self.game.home_city_index = 0
        self.game.home_city = self.game.city_names[0]
        
        # Calculate distance for a known route
        route = [self.game.city_names[1], self.game.city_names[2], self.game.city_names[3]]
        
        # Expected distance:
        # Home -> 1: distances[0, 1]
        # 1 -> 2: distances[1, 2]
        # 2 -> 3: distances[2, 3]
        # 3 -> Home: distances[3, 0]
        expected_distance = (
            self.game.distances[0, 1] +
            self.game.distances[1, 2] +
            self.game.distances[2, 3] +
            self.game.distances[3, 0]
        )
        
        self.assertEqual(self.game.calculate_route_distance(route), expected_distance)
    
    def test_nearest_neighbor_algorithm(self):
        """Test the Nearest Neighbor algorithm."""
        # Set up a simple test case
        self.game.selected_cities = [self.game.city_names[1], self.game.city_names[2], self.game.city_names[3]]
        
        # Run the algorithm
        route, distance = self.game.find_shortest_route_nearest_neighbor()[0]
        
        # Check that the route includes all selected cities
        self.assertEqual(set(route), set(self.game.selected_cities))
        
        # Check that the distance is calculated correctly
        expected_distance = self.game.calculate_route_distance(route)
        self.assertEqual(distance, expected_distance)
    
    def test_dynamic_programming_algorithm(self):
        """Test the Dynamic Programming algorithm."""
        # Use a small subset of cities for faster testing
        self.game.selected_cities = [self.game.city_names[1], self.game.city_names[2]]
        
        # Run the algorithm
        route, distance = self.game.find_shortest_route_dynamic_programming()[0]
        
        # Check that the route includes all selected cities
        self.assertEqual(set(route), set(self.game.selected_cities))
        
        # Check that the distance is calculated correctly
        expected_distance = self.game.calculate_route_distance(route)
        self.assertAlmostEqual(distance, expected_distance, places=5)
        
        # For small problems, we can verify optimality by checking all permutations
        min_distance = float('inf')
        for perm in [[self.game.city_names[1], self.game.city_names[2]], 
                     [self.game.city_names[2], self.game.city_names[1]]]:
            dist = self.game.calculate_route_distance(perm)
            if dist < min_distance:
                min_distance = dist
        
        self.assertAlmostEqual(distance, min_distance, places=5)
    
    def test_genetic_algorithm(self):
        """Test the Genetic Algorithm."""
        # Set up a test case
        self.game.selected_cities = [self.game.city_names[1], self.game.city_names[2], self.game.city_names[3]]
        
        # Run the algorithm
        route, distance = self.game.find_shortest_route_genetic_algorithm()[0]
        
        # Check that the route includes all selected cities
        self.assertEqual(set(route), set(self.game.selected_cities))
        
        # Check that the distance is calculated correctly
        expected_distance = self.game.calculate_route_distance(route)
        self.assertEqual(distance, expected_distance)
    
    def test_ordered_crossover(self):
        """Test the ordered crossover operator for the genetic algorithm."""
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['E', 'D', 'C', 'B', 'A']
        
        # Mock random selection of crossover points
        random.seed(42)  # For reproducibility
        
        child = self.game.ordered_crossover(parent1, parent2)
        
        # Check that the child has all cities exactly once
        self.assertEqual(len(child), len(parent1))
        self.assertEqual(set(child), set(parent1))
        
        # Check that the child has some elements from both parents
        # This is a probabilistic test, but with the seed it should be consistent
        self.assertTrue(any(child[i] == parent1[i] for i in range(len(child))))
        self.assertTrue(any(child[i] == parent2[i] for i in range(len(child))))
    
    def test_mutation(self):
        """Test the mutation operator for the genetic algorithm."""
        route = ['A', 'B', 'C', 'D', 'E']
        original_route = route.copy()
        
        # Mock random selection of mutation points
        random.seed(42)  # For reproducibility
        
        self.game.mutate(route)
        
        # Check that exactly two cities were swapped
        differences = sum(1 for i in range(len(route)) if route[i] != original_route[i])
        self.assertEqual(differences, 2)
        
        # Check that the route still has all cities
        self.assertEqual(set(route), set(original_route))
    
    def test_tournament_selection(self):
        """Test the tournament selection for the genetic algorithm."""
        population = [['A', 'B', 'C'], ['C', 'B', 'A'], ['B', 'A', 'C']]
        fitness_scores = [0.1, 0.3, 0.2]  # Second individual is the fittest
        
        # Mock random selection of tournament participants
        random.seed(42)  # For reproducibility
        
        selected = self.game.tournament_selection(population, fitness_scores)
        
        # With the given seed, the second individual should be selected
        self.assertEqual(selected, population[1])
    
    def test_new_game(self):
        """Test starting a new game."""
        # Store original values
        original_distances = self.game.distances.copy()
        original_home_city = self.game.home_city
        
        # Start a new game
        self.game.new_game()
        
        # Check that the game state was reset
        self.assertFalse(np.array_equal(self.game.distances, original_distances))
        # Home city might be the same by chance, but it's unlikely
        # self.assertNotEqual(self.game.home_city, original_home_city)
        self.assertEqual(self.game.selected_cities, [])
        self.assertEqual(self.game.user_route, [])
        self.assertEqual(self.game.shortest_routes, {})
        self.assertEqual(self.game.execution_times, {})
    
    def test_save_game_result(self):
        """Test saving game results to the database."""
        # Set up game state
        self.game.selected_cities = [self.game.city_names[1], self.game.city_names[2]]
        self.game.user_route = [self.game.city_names[1], self.game.city_names[2]]
        
        # Save the game result
        self.game.save_game_result(True)
        
        # Check that the result was saved
        self.assertEqual(len(self.db.game_results), 1)
        result = list(self.db.game_results.values())[0]
        self.assertEqual(result['correct_answer'], "correct")
        
        # Check that the TSP specific data was saved
        self.assertEqual(len(self.db.tsp_games), 1)
        game_data = list(self.db.tsp_games.values())[0]
        self.assertEqual(game_data['home_city'], self.game.home_city)
        self.assertEqual(game_data['selected_cities'], ",".join(self.game.selected_cities))
        self.assertEqual(game_data['shortest_route'], ",".join(self.game.user_route))


if __name__ == "__main__":
    unittest.main()
