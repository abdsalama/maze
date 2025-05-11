from graphics import *
from config import GameConfig, CellType
from drawing_utils import MidpointCircle
import random
import time
import math

class Maze:
    def __init__(self):
        self.width = GameConfig.WINDOW_WIDTH
        self.height = GameConfig.WINDOW_HEIGHT
        self.cell_size = GameConfig.CELL_SIZE
        self.window = None
        self.coins = []
        self.coin_objects = []  # Store coin graphical objects
        self.score = 0
        self.start_time = time.time()
        self.maze_array = self._create_maze()

    def initialize_window(self):
        """Create the game window"""
        self.window = GraphWin(GameConfig.TITLE, self.width, self.height)
        self.window.setBackground(GameConfig.COLORS["path"])
        self._create_score_display()

    def _create_score_display(self):
        """Create score and time display"""
        # Score display
        self.score_text = Text(Point(80, 20), f"Score: {self.score}")
        self.score_text.setStyle("bold")
        self.score_text.setSize(12)
        self.score_text.draw(self.window)

        # Coin counter display
        self.coin_counter = Text(Point(200, 20), f"Coins: {self.score // GameConfig.POINTS_PER_COIN}/{GameConfig.COIN_COUNT}")
        self.coin_counter.setStyle("bold")
        self.coin_counter.setSize(12)
        self.coin_counter.draw(self.window)

        # Time display
        self.time_text = Text(Point(320, 20), "Time: 0 sec")
        self.time_text.setStyle("bold")
        self.time_text.setSize(12)
        self.time_text.draw(self.window)

    def update_display(self):
        """Update score and time display"""
        self.score_text.setText(f"Score: {self.score}")
        self.coin_counter.setText(f"Coins: {self.score // GameConfig.POINTS_PER_COIN}/{GameConfig.COIN_COUNT}")
        elapsed = int(time.time() - self.start_time)
        self.time_text.setText(f"Time: {elapsed} sec")

    def _create_maze(self):
        """Create random maze using Recursive Backtracking algorithm."""
        # Calculate maze dimensions based on cell size
        rows = (self.height - 50) // self.cell_size
        cols = self.width // self.cell_size

        # Get complexity factor based on difficulty
        difficulty = GameConfig.DIFFICULTY
        complexity = GameConfig.DIFFICULTY_SETTINGS[difficulty]["maze_complexity"]

        # Initialize maze with walls
        maze = [[1 for _ in range(cols)] for _ in range(rows)]

        def carve_path(x, y):
            maze[y][x] = 0

            # Define directions: right, down, left, up
            directions = [(2,0), (0,2), (-2,0), (0,-2)]
            random.shuffle(directions)


            if random.random() < complexity:
                random.shuffle(directions)

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < cols and 0 <= new_y < rows and
                    maze[new_y][new_x] == 1):
                    maze[y + dy//2][x + dx//2] = 0
                    carve_path(new_x, new_y)

        # Start from a random point
        start_x = random.randrange(1, cols-1, 2)
        start_y = random.randrange(1, rows-1, 2)
        carve_path(start_x, start_y)

        # Add start and end positions
        # Place start near top left
        start_positions = [(x,y) for y in range(min(5, rows//2))
                         for x in range(min(5, cols//2))
                         if maze[y][x] == 0]
        if start_positions:
            start_pos = random.choice(start_positions)
            maze[start_pos[1]][start_pos[0]] = CellType.START.value
        else:
            maze[1][1] = CellType.START.value

        # Place end near bottom right
        end_positions = [(x,y) for y in range(max(rows-5, rows//2), rows)
                       for x in range(max(cols-5, cols//2), cols)
                       if maze[y][x] == 0]
        if end_positions:
            end_pos = random.choice(end_positions)
            maze[end_pos[1]][end_pos[0]] = CellType.END.value
        else:
            maze[rows-2][cols-2] = CellType.END.value

        # Add coins
        self._add_coins(maze)

        return maze

    def _add_coins(self, maze):
        """Add coins to the maze"""
        # Get coin count from config
        coin_count = GameConfig.COIN_COUNT

        # Find all empty cells
        empty_cells = [(x,y) for y in range(len(maze))
                    for x in range(len(maze[0]))
                    if maze[y][x] == 0]

        # Select random positions for coins
        if empty_cells:
            coin_positions = random.sample(empty_cells, min(coin_count, len(empty_cells)))
            for x, y in coin_positions:
                maze[y][x] = CellType.COIN.value
                self.coins.append((x,y))

    def draw_maze(self):
        """Draw the maze with visual effects"""
        # Clear any existing coin objects
        self.coin_objects = []

        for row in range(len(self.maze_array)):
            for col in range(len(self.maze_array[0])):
                x1 = col * self.cell_size
                y1 = row * self.cell_size + 40
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell = Rectangle(Point(x1, y1), Point(x2, y2))
                cell_type = self.maze_array[row][col]

                if cell_type == CellType.WALL.value:
                    cell.setFill(GameConfig.COLORS["wall"])
                elif cell_type == CellType.START.value:
                    cell.setFill(GameConfig.COLORS["start"])
                elif cell_type == CellType.END.value:
                    cell.setFill(GameConfig.COLORS["end"])
                elif cell_type == CellType.COIN.value:
                    cell.setFill(GameConfig.COLORS["path"])
                    # Add yellow circle inside the cell for coin
                    self._add_coin_effect(x1, y1, x2, y2)
                else:
                    cell.setFill(GameConfig.COLORS["path"])

                cell.setOutline(GameConfig.COLORS["grid"])
                cell.draw(self.window)

                # Add progressive drawing effect
                if random.random() < 0.1:
                    time.sleep(0.01)
                    self.window.update()

    def _add_coin_effect(self, x1, y1, x2, y2):
        """Add shiny coin using midpoint circle algorithm."""
        # Create square background first
        square = Rectangle(Point(x1, y1), Point(x2, y2))
        square.setFill(GameConfig.COLORS["path"])
        square.setOutline(GameConfig.COLORS["grid"])
        square.draw(self.window)

        # Calculate center and radius
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        radius = self.cell_size / 3

        # Create circle for coin using midpoint circle algorithm
        coin = MidpointCircle(Point(center_x, center_y), radius)
        coin.setFill(GameConfig.COLORS["coin"])
        coin.setOutline("gold")
        coin.draw(self.window)

        # Store coin object for animation
        self.coin_objects.append(coin)

        return coin

    def collect_coin(self, x, y):
        """Collect coin and increase score"""
        if (x, y) in self.coins:
            self.coins.remove((x, y))
            self.maze_array[y][x] = CellType.PATH.value
            self.score += GameConfig.POINTS_PER_COIN
            self.update_display()
            return True
        return False

    def is_game_won(self, x, y):
        """Check if player has won"""
        return self.maze_array[y][x] == CellType.END.value

    def get_ui_offset(self):
        """Get the Y offset for UI elements"""
        return 40

    def animate_coins(self):
        """Animate coins with pulsing effect using sine wave."""
        for coin in self.coin_objects:
            # Skip if coin was already collected
            if not coin.canvas:
                continue

            # Get current radius
            current_radius = coin.getRadius()

            # Calculate new radius with sine wave
            t = time.time() * 3
            scale_factor = 0.1 * math.sin(t) + 1

            # Apply new radius
            coin.undraw()
            coin_center = coin.getCenter()
            coin = MidpointCircle(coin_center, current_radius * scale_factor)
            coin.setFill(GameConfig.COLORS["coin"])
            coin.setOutline("gold")
            coin.draw(self.window)