"""
Common utility functions for the game project.
"""
import time
import json
from functools import wraps

def timer_decorator(func):
    """Decorator to measure execution time of functions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper

class InputValidator:
    """Utility class for input validation."""
    
    @staticmethod
    def validate_integer(value, min_value=None, max_value=None, error_msg=None):
        """Validate that input is an integer within specified range."""
        try:
            int_value = int(value)
            if min_value is not None and int_value < min_value:
                raise ValueError(error_msg or f"Value must be at least {min_value}")
            if max_value is not None and int_value > max_value:
                raise ValueError(error_msg or f"Value must be at most {max_value}")
            return int_value
        except ValueError:
            if error_msg:
                raise ValueError(error_msg)
            raise ValueError("Input must be an integer")
    
    @staticmethod
    def validate_string(value, min_length=None, max_length=None, allowed_chars=None, error_msg=None):
        """Validate that input is a string with specified constraints."""
        if not isinstance(value, str):
            raise ValueError(error_msg or "Input must be a string")
        
        if min_length is not None and len(value) < min_length:
            raise ValueError(error_msg or f"Input must be at least {min_length} characters long")
        
        if max_length is not None and len(value) > max_length:
            raise ValueError(error_msg or f"Input must be at most {max_length} characters long")
        
        if allowed_chars is not None:
            for char in value:
                if char not in allowed_chars:
                    raise ValueError(error_msg or f"Input contains invalid character: {char}")
        
        return value
    
    @staticmethod
    def validate_coordinates(x, y, min_x=None, max_x=None, min_y=None, max_y=None, error_msg=None):
        """Validate that coordinates are within specified bounds."""
        try:
            x_val = int(x)
            y_val = int(y)
            
            if min_x is not None and x_val < min_x:
                raise ValueError(error_msg or f"X coordinate must be at least {min_x}")
            if max_x is not None and x_val > max_x:
                raise ValueError(error_msg or f"X coordinate must be at most {max_x}")
            if min_y is not None and y_val < min_y:
                raise ValueError(error_msg or f"Y coordinate must be at least {min_y}")
            if max_y is not None and y_val > max_y:
                raise ValueError(error_msg or f"Y coordinate must be at most {max_y}")
            
            return x_val, y_val
        except ValueError:
            if error_msg:
                raise ValueError(error_msg)
            raise ValueError("Coordinates must be integers")

class GameException(Exception):
    """Base exception class for game-related errors."""
    pass

class InvalidMoveException(GameException):
    """Exception raised when an invalid move is attempted."""
    pass

class GameStateException(GameException):
    """Exception raised when an operation is attempted in an invalid game state."""
    pass

class DataPersistence:
    """Utility class for data serialization and persistence."""
    
    @staticmethod
    def serialize_to_json(data, file_path=None):
        """Serialize data to JSON string or file."""
        try:
            json_data = json.dumps(data, indent=2)
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(json_data)
            return json_data
        except Exception as e:
            raise GameException(f"Error serializing data: {e}")
    
    @staticmethod
    def deserialize_from_json(json_str=None, file_path=None):
        """Deserialize data from JSON string or file."""
        try:
            if file_path:
                with open(file_path, 'r') as f:
                    return json.load(f)
            elif json_str:
                return json.loads(json_str)
            else:
                raise GameException("Either json_str or file_path must be provided")
        except Exception as e:
            raise GameException(f"Error deserializing data: {e}")
