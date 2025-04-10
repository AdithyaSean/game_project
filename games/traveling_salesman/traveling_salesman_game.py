"""
Traveling Salesman Problem game implementation with multiple algorithm approaches.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import numpy as np
import sys
import os
import math
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.utils import timer_decorator, GameException, InvalidMoveException
from database.db_schema import GameDatabase

class TravelingSalesmanGame:
    """Traveling Salesman Problem game with multiple algorithm approaches."""
    
    def __init__(self, root, player_name, db, return_callback):
        """Initialize the Traveling Salesman game."""
        self.root = root
        self.player_name = player_name
        self.db = db
        self.return_callback = return_callback
        
        # Game state
        self.num_cities = 10  # Cities A through J
        self.city_names = [chr(65 + i) for i in range(self.num_cities)]  # A to J
        self.distances = self.generate_random_distances()
        self.home_city_index = random.randint(0, self.num_cities - 1)
        self.home_city = self.city_names[self.home_city_index]
        self.selected_cities = []
        self.user_route = []
        self.shortest_routes = {}  # Algorithm name -> route
        self.execution_times = {}  # Algorithm name -> time
        
        # Game ID for database
        self.game_id = self.db.add_game("traveling_salesman")
        
        # Set up the UI
        self.setup_ui()
    
    def generate_random_distances(self):
        """Generate random distances between cities (50 to 100 km)."""
        distances = np.zeros((self.num_cities, self.num_cities))
        
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                distance = random.randint(50, 100)
                distances[i, j] = distance
                distances[j, i] = distance
        
        return distances
    
    def setup_ui(self):
        """Set up the game UI."""
        self.root.title("Traveling Salesman Problem")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Traveling Salesman Problem", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Player info and home city
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_frame, 
            text=f"Player: {self.player_name}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Label(
            info_frame, 
            text=f"Home City: {self.home_city}", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.RIGHT)
        
        # Distance matrix display
        matrix_frame = tk.Frame(main_frame)
        matrix_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        tk.Label(
            matrix_frame, 
            text="Distance Matrix (km):", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        # Create a table for the distance matrix
        table_frame = tk.Frame(matrix_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Header row with city names
        tk.Label(
            table_frame, 
            text="", 
            width=5, 
            font=("Arial", 10, "bold"),
            relief=tk.RIDGE
        ).grid(row=0, column=0, sticky="nsew")
        
        for j, city in enumerate(self.city_names):
            tk.Label(
                table_frame, 
                text=city, 
                width=5, 
                font=("Arial", 10, "bold"),
                relief=tk.RIDGE
            ).grid(row=0, column=j+1, sticky="nsew")
        
        # City names in first column and distances in cells
        for i, city in enumerate(self.city_names):
            tk.Label(
                table_frame, 
                text=city, 
                width=5, 
                font=("Arial", 10, "bold"),
                relief=tk.RIDGE
            ).grid(row=i+1, column=0, sticky="nsew")
            
            for j in range(self.num_cities):
                if i == j:
                    distance_text = "---"
                else:
                    distance_text = str(int(self.distances[i, j]))
                
                tk.Label(
                    table_frame, 
                    text=distance_text, 
                    width=5, 
                    font=("Arial", 10),
                    relief=tk.RIDGE
                ).grid(row=i+1, column=j+1, sticky="nsew")
        
        # City selection
        selection_frame = tk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            selection_frame, 
            text="Select Cities to Visit:", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        # Checkbuttons for city selection
        cities_frame = tk.Frame(selection_frame)
        cities_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.city_vars = []
        for i, city in enumerate(self.city_names):
            if i == self.home_city_index:
                # Skip home city as it's already included
                continue
            
            var = tk.BooleanVar()
            self.city_vars.append((city, var))
            
            tk.Checkbutton(
                cities_frame, 
                text=city, 
                variable=var, 
                font=("Arial", 12)
            ).pack(side=tk.LEFT, padx=10)
        
        # Route input
        route_frame = tk.Frame(main_frame)
        route_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            route_frame, 
            text="Enter Your Route (comma-separated cities, e.g., A,B,C):", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        self.route_entry = tk.Entry(route_frame, font=("Arial", 12), width=40)
        self.route_entry.pack(fill=tk.X, pady=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Button(
            button_frame, 
            text="Find Shortest Route", 
            font=("Arial", 12),
            command=self.find_shortest_route
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame, 
            text="Submit My Route", 
            font=("Arial", 12),
            command=self.submit_route
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            button_frame, 
            text="New Game", 
            font=("Arial", 12),
            command=self.new_game
        ).pack(side=tk.LEFT)
        
        tk.Button(
            button_frame, 
            text="Return to Menu", 
            font=("Arial", 12),
            command=lambda: self.return_callback(self.root)
        ).pack(side=tk.RIGHT)
        
        # Results display
        self.results_frame = tk.Frame(main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            self.results_frame, 
            text="Results:", 
            font=("Arial", 14, "bold")
        ).pack(anchor="w")
        
        self.results_text = tk.Text(
            self.results_frame, 
            font=("Arial", 12),
            height=10,
            wrap=tk.WORD
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create a frame for the graph
        self.graph_frame = tk.Frame(main_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Initialize the graph
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Plot the cities
        self.plot_cities()
    
    def plot_cities(self, route=None):
        """Plot the cities and optionally a route."""
        self.ax.clear()
        
        # Generate random positions for cities
        if not hasattr(self, 'city_positions'):
            self.city_positions = {}
            for i, city in enumerate(self.city_names):
                self.city_positions[city] = (random.random() * 10, random.random() * 10)
        
        # Plot cities
        for city, pos in self.city_positions.items():
            color = 'red' if city == self.home_city else 'blue'
            self.ax.scatter(pos[0], pos[1], color=color, s=100)
            self.ax.text(pos[0], pos[1], city, fontsize=12)
        
        # Plot route if provided
        if route:
            route_x = [self.city_positions[city][0] for city in route]
            route_y = [self.city_positions[city][1] for city in route]
            
            # Add home city at the beginning and end
            route_x = [self.city_positions[self.home_city][0]] + route_x + [self.city_positions[self.home_city][0]]
            route_y = [self.city_positions[self.home_city][1]] + route_y + [self.city_positions[self.home_city][1]]
            
            self.ax.plot(route_x, route_y, 'g-', linewidth=2)
        
        self.ax.set_title("City Map")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        
        self.canvas.draw()
    
    def get_selected_cities(self):
        """Get the list of selected cities."""
        selected = []
        for city, var in self.city_vars:
            if var.get():
                selected.append(city)
        return selected
    
    def find_shortest_route(self):
        """Find the shortest route using three different algorithms."""
        # Get selected cities
        self.selected_cities = self.get_selected_cities()
        
        if not self.selected_cities:
            messagebox.showerror("Error", "Please select at least one city to visit")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.shortest_routes = {}
        self.execution_times = {}
        
        # Find shortest route using three different algorithms
        self.find_shortest_route_nearest_neighbor()
        self.find_shortest_route_dynamic_programming()
        self.find_shortest_route_genetic_algorithm()
        
        # Display results
        self.display_results()
        
        # Save algorithm performance to database
        for algo_name, execution_time in self.execution_times.items():
            self.db.add_algorithm_performance(
                self.game_id,
                f"tsp_{algo_name}",
                execution_time,
                1  # Game round
            )
    
    @timer_decorator
    def find_shortest_route_nearest_neighbor(self):
        """Find shortest route using Nearest Neighbor algorithm."""
        cities = self.selected_cities.copy()
        route = []
        current_city = self.home_city
        total_distance = 0
        
        while cities:
            # Find the nearest unvisited city
            nearest_city = None
            min_distance = float('inf')
            
            for city in cities:
                distance = self.get_distance(current_city, city)
                if distance < min_distance:
                    min_distance = distance
                    nearest_city = city
            
            # Add the nearest city to the route
            route.append(nearest_city)
            total_distance += min_distance
            
            # Move to the nearest city
            current_city = nearest_city
            cities.remove(nearest_city)
        
        # Return to home city
        total_distance += self.get_distance(current_city, self.home_city)
        
        self.shortest_routes["nearest_neighbor"] = (route, total_distance)
        return route, total_distance
    
    @timer_decorator
    def find_shortest_route_dynamic_programming(self):
        """Find shortest route using Dynamic Programming approach."""
        # Include home city and selected cities
        cities = [self.home_city] + self.selected_cities
        n = len(cities)
        
        # Create a mapping of city names to indices
        city_to_index = {city: i for i, city in enumerate(cities)}
        
        # Create distance matrix for the selected cities
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist_matrix[i, j] = self.get_distance(cities[i], cities[j])
        
        # Initialize memoization table
        # dp[mask][i] = shortest path visiting all cities in mask and ending at city i
        dp = {}
        
        # Recursive function with memoization
        def tsp(mask, pos):
            if mask == ((1 << n) - 1):
                # All cities visited, return to home city
                return dist_matrix[pos][0]
            
            if (mask, pos) in dp:
                return dp[(mask, pos)]
            
            ans = float('inf')
            for city in range(n):
                if (mask & (1 << city)) == 0:  # If city is not visited
                    new_ans = dist_matrix[pos][city] + tsp(mask | (1 << city), city)
                    ans = min(ans, new_ans)
            
            dp[(mask, pos)] = ans
            return ans
        
        # Start from home city (index 0) with only home city visited
        min_distance = tsp(1, 0)
        
        # Reconstruct the path
        path = []
        mask = 1  # Home city is visited
        pos = 0   # Start at home city
        
        for _ in range(n - 1):
            best_city = -1
            best_dist = float('inf')
            
            for city in range(n):
                if (mask & (1 << city)) == 0:  # If city is not visited
                    if dist_matrix[pos][city] + dp.get((mask | (1 << city), city), float('inf')) < best_dist:
                        best_dist = dist_matrix[pos][city] + dp.get((mask | (1 << city), city), float('inf'))
                        best_city = city
            
            path.append(cities[best_city])
            mask |= (1 << best_city)
            pos = best_city
        
        self.shortest_routes["dynamic_programming"] = (path, min_distance)
        return path, min_distance
    
    @timer_decorator
    def find_shortest_route_genetic_algorithm(self):
        """Find shortest route using Genetic Algorithm."""
        # Parameters
        population_size = 50
        generations = 100
        mutation_rate = 0.01
        
        # Create initial population
        population = []
        for _ in range(population_size):
            route = self.selected_cities.copy()
            random.shuffle(route)
            population.append(route)
        
        # Evolution
        for _ in range(generations):
            # Calculate fitness for each individual
            fitness_scores = []
            for route in population:
                distance = self.calculate_route_distance(route)
                fitness_scores.append(1 / distance)  # Higher fitness for shorter routes
            
            # Create new population
            new_population = []
            
            # Elitism: keep the best individual
            best_idx = fitness_scores.index(max(fitness_scores))
            new_population.append(population[best_idx])
            
            # Create rest of the new population
            while len(new_population) < population_size:
                # Selection (tournament selection)
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)
                
                # Crossover (ordered crossover)
                if random.random() < 0.7:  # Crossover rate
                    child = self.ordered_crossover(parent1, parent2)
                else:
                    child = parent1.copy()
                
                # Mutation
                if random.random() < mutation_rate:
                    self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        # Find the best route in the final population
        best_route = None
        min_distance = float('inf')
        
        for route in population:
            distance = self.calculate_route_distance(route)
            if distance < min_distance:
                min_distance = distance
                best_route = route
        
        self.shortest_routes["genetic_algorithm"] = (best_route, min_distance)
        return best_route, min_distance
    
    def tournament_selection(self, population, fitness_scores, tournament_size=3):
        """Tournament selection for genetic algorithm."""
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_idx]
    
    def ordered_crossover(self, parent1, parent2):
        """Ordered crossover for genetic algorithm."""
        size = len(parent1)
        child = [None] * size
        
        # Select a random subset of parent1
        start, end = sorted(random.sample(range(size), 2))
        
        # Copy the subset from parent1 to child
        for i in range(start, end + 1):
            child[i] = parent1[i]
        
        # Fill the remaining positions with cities from parent2 in order
        parent2_idx = 0
        for i in range(size):
            if child[i] is None:
                while parent2[parent2_idx] in child:
                    parent2_idx += 1
                child[i] = parent2[parent2_idx]
                parent2_idx += 1
        
        return child
    
    def mutate(self, route):
        """Mutation for genetic algorithm (swap mutation)."""
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]
    
    def calculate_route_distance(self, route):
        """Calculate the total distance of a route."""
        total_distance = self.get_distance(self.home_city, route[0])
        
        for i in range(len(route) - 1):
            total_distance += self.get_distance(route[i], route[i + 1])
        
        total_distance += self.get_distance(route[-1], self.home_city)
        
        return total_distance
    
    def get_distance(self, city1, city2):
        """Get the distance between two cities."""
        idx1 = self.city_names.index(city1)
        idx2 = self.city_names.index(city2)
        return self.distances[idx1, idx2]
    
    def display_results(self):
        """Display the results of the algorithms."""
        self.results_text.delete(1.0, tk.END)
        
        for algo_name, (route, distance) in self.shortest_routes.items():
            algo_display_name = algo_name.replace("_", " ").title()
            route_str = f"{self.home_city} -> " + " -> ".join(route) + f" -> {self.home_city}"
            
            self.results_text.insert(tk.END, f"{algo_display_name}:\n")
            self.results_text.insert(tk.END, f"Route: {route_str}\n")
            self.results_text.insert(tk.END, f"Distance: {distance:.2f} km\n")
            self.results_text.insert(tk.END, f"Execution Time: {self.execution_times[algo_name]:.6f} seconds\n\n")
        
        # Plot the best route
        best_algo = min(self.shortest_routes.items(), key=lambda x: x[1][1])[0]
        best_route = self.shortest_routes[best_algo][0]
        self.plot_cities(best_route)
    
    def submit_route(self):
        """Submit the user's route."""
        # Get selected cities
        self.selected_cities = self.get_selected_cities()
        
        if not self.selected_cities:
            messagebox.showerror("Error", "Please select at least one city to visit")
            return
        
        # Get user's route
        route_str = self.route_entry.get().strip()
        if not route_str:
            messagebox.showerror("Error", "Please enter your route")
            return
        
        # Parse the route
        try:
            user_route = [city.strip() for city in route_str.split(",")]
            
            # Validate the route
            if len(user_route) != len(self.selected_cities):
                messagebox.showerror("Error", "Your route must include all selected cities exactly once")
                return
            
            for city in user_route:
                if city not in self.selected_cities:
                    messagebox.showerror("Error", f"City {city} is not in the selected cities")
                    return
            
            if len(set(user_route)) != len(user_route):
                messagebox.showerror("Error", "Your route contains duplicate cities")
                return
            
            self.user_route = user_route
            
            # Calculate the distance of the user's route
            user_distance = self.calculate_route_distance(self.user_route)
            
            # Find the shortest route if not already found
            if not self.shortest_routes:
                self.find_shortest_route()
            
            # Get the shortest route
            best_algo = min(self.shortest_routes.items(), key=lambda x: x[1][1])[0]
            best_route = self.shortest_routes[best_algo][0]
            best_distance = self.shortest_routes[best_algo][1]
            
            # Compare user's route with the shortest route
            if abs(user_distance - best_distance) < 0.01:  # Allow for floating point errors
                messagebox.showinfo("Result", "Congratulations! Your route is optimal!")
                self.save_game_result(True)
            else:
                messagebox.showinfo("Result", f"Your route distance is {user_distance:.2f} km. The optimal route distance is {best_distance:.2f} km.")
                self.save_game_result(False)
            
            # Plot the user's route
            self.plot_cities(self.user_route)
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid route format: {e}")
    
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
            0  # Time taken (not applicable for TSP)
        )
        
        # Add TSP specific data
        self.db.add_tsp_game(
            self.game_id,
            self.home_city,
            ",".join(self.selected_cities),
            ",".join(self.user_route)
        )
    
    def new_game(self):
        """Start a new game."""
        # Generate new random distances
        self.distances = self.generate_random_distances()
        
        # Select a new random home city
        self.home_city_index = random.randint(0, self.num_cities - 1)
        self.home_city = self.city_names[self.home_city_index]
        
        # Reset selected cities and user route
        self.selected_cities = []
        self.user_route = []
        
        # Reset city checkboxes
        for _, var in self.city_vars:
            var.set(False)
        
        # Clear route entry
        self.route_entry.delete(0, tk.END)
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Reset shortest routes and execution times
        self.shortest_routes = {}
        self.execution_times = {}
        
        # Create new game in database
        self.game_id = self.db.add_game("traveling_salesman")
        
        # Generate new city positions
        self.city_positions = {}
        for i, city in enumerate(self.city_names):
            self.city_positions[city] = (random.random() * 10, random.random() * 10)
        
        # Update the UI
        self.plot_cities()
        
        # Update home city label
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label) and "Home City:" in grandchild.cget("text"):
                                grandchild.config(text=f"Home City: {self.home_city}")
        
        # Rebuild the distance matrix display
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.winfo_children():
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.winfo_children():
                                for great_grandchild in grandchild.winfo_children():
                                    if isinstance(great_grandchild, tk.Label) and great_grandchild.grid_info():
                                        row = great_grandchild.grid_info()["row"]
                                        col = great_grandchild.grid_info()["column"]
                                        
                                        if row > 0 and col > 0:
                                            i = row - 1
                                            j = col - 1
                                            
                                            if i == j:
                                                distance_text = "---"
                                            else:
                                                distance_text = str(int(self.distances[i, j]))
                                            
                                            great_grandchild.config(text=distance_text)


def main():
    """Main function to start the Traveling Salesman game."""
    root = tk.Tk()
    db = GameDatabase()
    game = TravelingSalesmanGame(root, "Player", db, lambda w: w.destroy())
    root.mainloop()

if __name__ == "__main__":
    main()
