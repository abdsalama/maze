from enum import Enum
import json

class CellType(Enum):
    WALL = 1
    PATH = 0
    START = 2
    END = 3
    COIN = 4

class GameConfig:
    # Window settings
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    TITLE = "Maze Adventure"

    # Maze settings
    CELL_SIZE = 40
    DIFFICULTY = "medium"
    COIN_COUNT = 10
    PLAYER_COLOR = "blue"

    # Points per coin
    POINTS_PER_COIN = 10

    # Colors
    COLORS = {
        "wall": "#2C3E50",
        "path": "#ECF0F1",
        "start": "#27AE60",
        "end": "#E74C3C",
        "coin": "#F1C40F",
        "grid": "#BDC3C7"
    }

    # Difficulty presets
    DIFFICULTY_SETTINGS = {
        "easy": {
            "cell_size": 50,
            "coin_count": 5,
            "maze_complexity": 0.5
        },
        "medium": {
            "cell_size": 40,
            "coin_count": 10,
            "maze_complexity": 0.7
        },
        "hard": {
            "cell_size": 30,
            "coin_count": 15,
            "maze_complexity": 0.9
        }
    }

    # Player color options
    PLAYER_COLORS = ["red", "green", "blue", "gray", "pink"]

    # Save and load settings
    @classmethod
    def save_config(cls, filename="config.json"):
        config_dict = {
            "window_width": cls.WINDOW_WIDTH,
            "window_height": cls.WINDOW_HEIGHT,
            "cell_size": cls.CELL_SIZE,
            "difficulty": cls.DIFFICULTY,
            "player_color": cls.PLAYER_COLOR,
            "colors": cls.COLORS
        }
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=4)

    @classmethod
    def load_config(cls, filename="config.json"):
        try:
            with open(filename, 'r') as f:
                config = json.load(f)
                cls.WINDOW_WIDTH = config["window_width"]
                cls.WINDOW_HEIGHT = config["window_height"]
                cls.CELL_SIZE = config["cell_size"]
                if "difficulty" in config:
                    cls.DIFFICULTY = config["difficulty"]
                if "player_color" in config:
                    cls.PLAYER_COLOR = config["player_color"]
                cls.COLORS = config["colors"]
        except FileNotFoundError:
            print("Config file not found, using default settings")

    @classmethod
    def apply_difficulty(cls, difficulty):
        """Update settings for selected difficulty"""
        if difficulty in cls.DIFFICULTY_SETTINGS:
            settings = cls.DIFFICULTY_SETTINGS[difficulty]
            cls.CELL_SIZE = settings["cell_size"]
            cls.COIN_COUNT = settings["coin_count"]
            cls.DIFFICULTY = difficulty
            return True
        return False