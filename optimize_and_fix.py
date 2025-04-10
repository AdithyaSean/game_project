"""
Bug fixes and optimizations for the game collection.
"""
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_schema import GameDatabase

def optimize_database():
    """Optimize the database by adding indices and vacuum."""
    print("Optimizing database...")
    
    # Connect to the database
    db = GameDatabase()
    
    # Get the database connection
    conn = db._conn
    
    # Create indices for frequently queried columns
    print("Creating indices...")
    
    # Index for players table
    conn.execute("CREATE INDEX IF NOT EXISTS idx_players_name ON players(name)")
    
    # Index for games table
    conn.execute("CREATE INDEX IF NOT EXISTS idx_games_game_type ON games(game_type)")
    
    # Index for game_results table
    conn.execute("CREATE INDEX IF NOT EXISTS idx_game_results_player_id ON game_results(player_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_game_results_game_id ON game_results(game_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_game_results_correct_answer ON game_results(correct_answer)")
    
    # Index for algorithm_performance table
    conn.execute("CREATE INDEX IF NOT EXISTS idx_algorithm_performance_game_id ON algorithm_performance(game_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_algorithm_performance_algorithm_name ON algorithm_performance(algorithm_name)")
    
    # Vacuum the database to optimize storage
    print("Vacuuming database...")
    conn.execute("VACUUM")
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    db.close()
    
    print("Database optimization completed.")

def fix_known_bugs():
    """Fix known bugs in the game collection."""
    print("Fixing known bugs...")
    
    # Fix bug in database schema
    fix_database_schema_bug()
    
    # Fix bug in main menu
    fix_main_menu_bug()
    
    print("Bug fixes completed.")

def fix_database_schema_bug():
    """Fix bug in database schema where some tables might not be created."""
    print("Fixing database schema bug...")
    
    # Connect to the database
    db = GameDatabase()
    
    # Get the database connection
    conn = db._conn
    
    # Check if all tables exist and create them if they don't
    tables = [
        "players",
        "games",
        "game_results",
        "algorithm_performance",
        "tic_tac_toe_games",
        "traveling_salesman_games",
        "tower_of_hanoi_games",
        "eight_queens_games",
        "knights_tour_games"
    ]
    
    for table in tables:
        result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchone()
        if not result:
            print(f"Table {table} does not exist. Creating...")
            
            # Create the missing table
            if table == "players":
                conn.execute("""
                CREATE TABLE players (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
                """)
            elif table == "games":
                conn.execute("""
                CREATE TABLE games (
                    id INTEGER PRIMARY KEY,
                    game_type TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """)
            elif table == "game_results":
                conn.execute("""
                CREATE TABLE game_results (
                    id INTEGER PRIMARY KEY,
                    player_id INTEGER NOT NULL,
                    game_id INTEGER NOT NULL,
                    correct_answer TEXT NOT NULL,
                    time_taken REAL,
                    FOREIGN KEY (player_id) REFERENCES players (id),
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "algorithm_performance":
                conn.execute("""
                CREATE TABLE algorithm_performance (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    algorithm_name TEXT NOT NULL,
                    execution_time REAL NOT NULL,
                    game_round INTEGER NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "tic_tac_toe_games":
                conn.execute("""
                CREATE TABLE tic_tac_toe_games (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    board_size INTEGER NOT NULL,
                    algorithm_used TEXT NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "traveling_salesman_games":
                conn.execute("""
                CREATE TABLE traveling_salesman_games (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    num_cities INTEGER NOT NULL,
                    city_sequence TEXT NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "tower_of_hanoi_games":
                conn.execute("""
                CREATE TABLE tower_of_hanoi_games (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    num_disks INTEGER NOT NULL,
                    move_sequence TEXT,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "eight_queens_games":
                conn.execute("""
                CREATE TABLE eight_queens_games (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    solution_config TEXT NOT NULL,
                    is_recognized BOOLEAN NOT NULL,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
            elif table == "knights_tour_games":
                conn.execute("""
                CREATE TABLE knights_tour_games (
                    id INTEGER PRIMARY KEY,
                    game_id INTEGER NOT NULL,
                    start_position TEXT NOT NULL,
                    move_sequence TEXT,
                    FOREIGN KEY (game_id) REFERENCES games (id)
                )
                """)
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    db.close()
    
    print("Database schema bug fixed.")

def fix_main_menu_bug():
    """Fix bug in main menu where player name might not be validated properly."""
    print("Fixing main menu bug...")
    
    # Read the main.py file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py"), "r") as f:
        content = f.read()
    
    # Check if the bug exists
    if "if not player_name:" in content:
        # Bug already fixed
        print("Main menu bug already fixed.")
        return
    
    # Fix the bug by adding proper validation
    for game_func in ["start_tic_tac_toe", "start_traveling_salesman", "start_tower_of_hanoi", "start_eight_queens", "start_knights_tour"]:
        old_code = f"def {game_func}(self):\n        \"\"\"Start the"
        new_code = f"def {game_func}(self):\n        \"\"\"Start the"
        
        old_code_2 = f"player_name = self.player_name_var.get()"
        new_code_2 = f"player_name = self.player_name_var.get()\n        if not player_name:\n            messagebox.showerror(\"Error\", \"Please enter a player name.\")\n            return"
        
        content = content.replace(old_code, new_code)
        content = content.replace(old_code_2, new_code_2)
    
    # Write the fixed content back to the file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py"), "w") as f:
        f.write(content)
    
    print("Main menu bug fixed.")

def main():
    """Main function to run optimizations and bug fixes."""
    print("Running optimizations and bug fixes...")
    
    # Optimize the database
    optimize_database()
    
    # Fix known bugs
    fix_known_bugs()
    
    print("Optimizations and bug fixes completed.")

if __name__ == "__main__":
    main()
