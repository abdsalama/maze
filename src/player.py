from graphics import *
from config import GameConfig, CellType
from drawing_utils import MidpointCircle

class Player:
    def __init__(self, maze):
        self.maze = maze
        self.cell_size = GameConfig.CELL_SIZE
        self.position = self._find_start_position()
        self.x, self.y = self.position
        self.character = None
        self.highlight = None
        self.color = GameConfig.PLAYER_COLOR
        self.ui_offset = self.maze.get_ui_offset()

    def _find_start_position(self):
        """Find the starting position in the maze"""
        for y in range(len(self.maze.maze_array)):
            for x in range(len(self.maze.maze_array[0])):
                if self.maze.maze_array[y][x] == CellType.START.value:
                    return (x, y)
        # Fallback to position (1,1) if no start is found
        return (1, 1)

    def draw(self):
        """Draw player using midpoint circle with 3D highlight."""
        x1 = self.x * self.cell_size
        y1 = self.y * self.cell_size + self.ui_offset
        center_x = x1 + self.cell_size / 2
        center_y = y1 + self.cell_size / 2

        # Only create and draw the character if it doesn't exist yet
        if self.character is None:

            self.character = MidpointCircle(Point(center_x, center_y), self.cell_size / 3)
            self.character.setFill(self.color)

            # Set outline to a darker shade
            if self.color == "red":
                outline = "darkred"
            elif self.color == "green":
                outline = "darkgreen"
            elif self.color == "blue":
                outline = "darkblue"
            elif self.color == "gray":
                outline = "dimgray"
            elif self.color == "pink":
                outline = "deeppink"
            else:
                outline = "black"

            self.character.setOutline(outline)
            self.character.draw(self.maze.window)


            self.highlight = MidpointCircle(Point(center_x - self.cell_size/8, center_y - self.cell_size/8),
                            self.cell_size/8)
            self.highlight.setFill("white")
            self.highlight.setOutline("white")
            self.highlight.setWidth(0)
            self.highlight.draw(self.maze.window)
        else:

            self.move_character(center_x, center_y)

    def move_character(self, new_center_x, new_center_y):
        """Move player to new position without redrawing"""
        if self.character and self.highlight:
            # Calculate the movement delta
            current_center = self.character.getCenter()
            dx = new_center_x - current_center.getX()
            dy = new_center_y - current_center.getY()

            # Move the character and highlight
            self.character.move(dx, dy)
            self.highlight.move(dx, dy)

    def move(self, dx, dy):
        """Move player if the target cell is valid"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the move is valid (not a wall)
        if (0 <= new_x < len(self.maze.maze_array[0]) and
            0 <= new_y < len(self.maze.maze_array) and
            self.maze.maze_array[new_y][new_x] != CellType.WALL.value):

            # Restore the color of the cell we're leaving
            old_cell_x1 = self.x * self.cell_size
            old_cell_y1 = self.y * self.cell_size + self.ui_offset
            old_cell_x2 = old_cell_x1 + self.cell_size
            old_cell_y2 = old_cell_y1 + self.cell_size

            # Determine correct color based on cell type
            old_cell_type = self.maze.maze_array[self.y][self.x]
            if old_cell_type == CellType.START.value:
                color = GameConfig.COLORS["start"]
            elif old_cell_type == CellType.END.value:
                color = GameConfig.COLORS["end"]
            else:
                color = GameConfig.COLORS["path"]

            # Draw rectangle with correct color
            old_cell = Rectangle(Point(old_cell_x1, old_cell_y1), Point(old_cell_x2, old_cell_y2))
            old_cell.setFill(color)
            old_cell.setOutline(GameConfig.COLORS["grid"])
            old_cell.draw(self.maze.window)

            # Update position
            self.x, self.y = new_x, new_y

            # Check for coin collection
            if self.maze.maze_array[self.y][self.x] == CellType.COIN.value:
                self.maze.collect_coin(self.x, self.y)

            # Calculate new center position
            new_cell_x1 = self.x * self.cell_size
            new_cell_y1 = self.y * self.cell_size + self.ui_offset
            new_center_x = new_cell_x1 + self.cell_size / 2
            new_center_y = new_cell_y1 + self.cell_size / 2

            # Move the player character to the new position
            self.move_character(new_center_x, new_center_y)

            # Check for win condition
            if self.maze.is_game_won(self.x, self.y):
                return True

        return False

    def handle_key(self, key):
        """Process keyboard input for movement"""
        if key == "Up" or key == "w":
            return self.move(0, -1)
        elif key == "Down" or key == "s":
            return self.move(0, 1)
        elif key == "Left" or key == "a":
            return self.move(-1, 0)
        elif key == "Right" or key == "d":
            return self.move(1, 0)
        return False

    def set_color(self, color):
        """Change the player's color"""
        if color in GameConfig.PLAYER_COLORS:
            self.color = color
            GameConfig.PLAYER_COLOR = color

            # If character exists, update its color
            if self.character:
                self.character.undraw()
                self.highlight.undraw()
                self.character = None
                self.highlight = None
                self.draw()
            return True
        return False