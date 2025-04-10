"""
Database schema and utility functions for the game project.
"""
import sqlite3
import os
from datetime import datetime

class GameDatabase:
    def __init__(self, db_path='game_data.db'):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        try:
            # Players table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Games table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Game results table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                game_id INTEGER,
                correct_answer TEXT,
                time_taken REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id),
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Algorithm performance table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS algorithm_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                algorithm_name TEXT NOT NULL,
                execution_time REAL,
                game_round INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Tic-Tac-Toe specific table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tic_tac_toe_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                board_state TEXT,
                winner TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Traveling Salesman specific table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tsp_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                home_city TEXT,
                selected_cities TEXT,
                shortest_route TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Tower of Hanoi specific table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tower_of_hanoi_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                num_disks INTEGER,
                move_sequence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Eight Queens specific table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eight_queens_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                solution_config TEXT,
                is_recognized BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            # Knight's Tour specific table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS knights_tour_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                start_position TEXT,
                move_sequence TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES games (id)
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Table creation error: {e}")
    
    def add_player(self, name):
        """Add a new player or get existing player ID."""
        try:
            self.cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
            player = self.cursor.fetchone()
            
            if player:
                return player[0]
            else:
                self.cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
                self.conn.commit()
                return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding player: {e}")
            return None
    
    def add_game(self, game_type):
        """Add a new game session."""
        try:
            self.cursor.execute("INSERT INTO games (game_type) VALUES (?)", (game_type,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding game: {e}")
            return None
    
    def add_game_result(self, player_id, game_id, correct_answer, time_taken):
        """Record a game result."""
        try:
            self.cursor.execute(
                "INSERT INTO game_results (player_id, game_id, correct_answer, time_taken) VALUES (?, ?, ?, ?)",
                (player_id, game_id, correct_answer, time_taken)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding game result: {e}")
            return None
    
    def add_algorithm_performance(self, game_id, algorithm_name, execution_time, game_round):
        """Record algorithm performance metrics."""
        try:
            self.cursor.execute(
                "INSERT INTO algorithm_performance (game_id, algorithm_name, execution_time, game_round) VALUES (?, ?, ?, ?)",
                (game_id, algorithm_name, execution_time, game_round)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding algorithm performance: {e}")
            return None
    
    # Game-specific methods
    
    def add_tic_tac_toe_game(self, game_id, board_state, winner):
        """Record a Tic-Tac-Toe game."""
        try:
            self.cursor.execute(
                "INSERT INTO tic_tac_toe_games (game_id, board_state, winner) VALUES (?, ?, ?)",
                (game_id, board_state, winner)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Tic-Tac-Toe game: {e}")
            return None
    
    def add_tsp_game(self, game_id, home_city, selected_cities, shortest_route):
        """Record a Traveling Salesman Problem game."""
        try:
            self.cursor.execute(
                "INSERT INTO tsp_games (game_id, home_city, selected_cities, shortest_route) VALUES (?, ?, ?, ?)",
                (game_id, home_city, selected_cities, shortest_route)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding TSP game: {e}")
            return None
    
    def add_tower_of_hanoi_game(self, game_id, num_disks, move_sequence):
        """Record a Tower of Hanoi game."""
        try:
            self.cursor.execute(
                "INSERT INTO tower_of_hanoi_games (game_id, num_disks, move_sequence) VALUES (?, ?, ?)",
                (game_id, num_disks, move_sequence)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Tower of Hanoi game: {e}")
            return None
    
    def add_eight_queens_game(self, game_id, solution_config, is_recognized=False):
        """Record an Eight Queens game."""
        try:
            self.cursor.execute(
                "INSERT INTO eight_queens_games (game_id, solution_config, is_recognized) VALUES (?, ?, ?)",
                (game_id, solution_config, is_recognized)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Eight Queens game: {e}")
            return None
    
    def add_knights_tour_game(self, game_id, start_position, move_sequence):
        """Record a Knight's Tour game."""
        try:
            self.cursor.execute(
                "INSERT INTO knights_tour_games (game_id, start_position, move_sequence) VALUES (?, ?, ?)",
                (game_id, start_position, move_sequence)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding Knight's Tour game: {e}")
            return None
    
    def check_eight_queens_solution_exists(self, solution_config):
        """Check if a solution for Eight Queens puzzle has already been recognized."""
        try:
            self.cursor.execute(
                "SELECT id FROM eight_queens_games WHERE solution_config = ? AND is_recognized = 1",
                (solution_config,)
            )
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error checking Eight Queens solution: {e}")
            return False
    
    def clear_eight_queens_recognition_flags(self):
        """Clear the recognition flags for all Eight Queens solutions."""
        try:
            self.cursor.execute("UPDATE eight_queens_games SET is_recognized = 0")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error clearing Eight Queens recognition flags: {e}")
            return False
    
    def get_algorithm_performance_stats(self, game_type, algorithm_name=None):
        """Get performance statistics for algorithms."""
        try:
            if algorithm_name:
                self.cursor.execute(
                    """
                    SELECT algorithm_name, AVG(execution_time), MIN(execution_time), MAX(execution_time)
                    FROM algorithm_performance ap
                    JOIN games g ON ap.game_id = g.id
                    WHERE g.game_type = ? AND ap.algorithm_name = ?
                    GROUP BY algorithm_name
                    """,
                    (game_type, algorithm_name)
                )
            else:
                self.cursor.execute(
                    """
                    SELECT algorithm_name, AVG(execution_time), MIN(execution_time), MAX(execution_time)
                    FROM algorithm_performance ap
                    JOIN games g ON ap.game_id = g.id
                    WHERE g.game_type = ?
                    GROUP BY algorithm_name
                    """,
                    (game_type,)
                )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting algorithm performance stats: {e}")
            return []
