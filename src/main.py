from graphics import *
from maze import Maze
from player import Player
from config import GameConfig
from drawing_utils import BresenhamRectangle
import time
import random



class Button:
    def __init__(self, win, center, width, height, label, use_bresenham=True):
        self.win = win
        self.center = center
        self.width = width
        self.height = height

        self.x1 = center.getX() - width / 2
        self.x2 = center.getX() + width / 2
        self.y1 = center.getY() - height / 2
        self.y2 = center.getY() + height / 2

        # Use Bresenham algorithm for rectangle border if specified
        if use_bresenham:
            self.rect = BresenhamRectangle(Point(self.x1, self.y1), Point(self.x2, self.y2))
            self.rect.setFill("lightgray")
            self.rect.setOutline("black")
            self.rect.setWidth(2)  # Make the border more visible
        else:
            self.rect = Rectangle(Point(self.x1, self.y1), Point(self.x2, self.y2))
            self.rect.setFill("lightgray")
            self.rect.setOutline("black")

        self.label = Text(center, label)
        self.label.setSize(12)

        # Store whether we're using Bresenham
        self.use_bresenham = use_bresenham

        # Track if this button is selected
        self.is_selected = False

        # Highlight border (will be created when needed)
        self.highlight_border = None

    def draw(self):
        self.rect.draw(self.win)
        self.label.draw(self.win)

    def undraw(self):
        self.rect.undraw()
        self.label.undraw()
        if self.highlight_border:
            self.highlight_border.undraw()

    def clicked(self, p):
        return self.x1 <= p.getX() <= self.x2 and self.y1 <= p.getY() <= self.y2

    def setFill(self, color):
        self.rect.setFill(color)

    def setWidth(self, width):
        self.rect.setWidth(width)

    def setOutline(self, color):
        self.rect.setOutline(color)

    def setSelected(self, selected=True):
        """Highlight the button as selected with a distinctive border"""
        self.is_selected = selected

        # Remove existing highlight if any
        if self.highlight_border:
            self.highlight_border.undraw()
            self.highlight_border = None

        if selected and self.win:
            # Create a new rectangle slightly larger than the button for the highlight
            highlight_x1 = self.x1 - 3
            highlight_y1 = self.y1 - 3
            highlight_x2 = self.x2 + 3
            highlight_y2 = self.y2 + 3

            # Create a visible highlight border
            self.highlight_border = Rectangle(
                Point(highlight_x1, highlight_y1),
                Point(highlight_x2, highlight_y2)
            )
            self.highlight_border.setOutline("#FFD700")  # Gold color
            self.highlight_border.setWidth(3)
            self.highlight_border.draw(self.win)


def welcome_screen():
    # Create welcome window
    win = GraphWin(GameConfig.TITLE, GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
    win.setBackground("white")

    # Game title
    title = Text(Point(GameConfig.WINDOW_WIDTH / 2, 100), "MAZE ADVENTURE")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("darkblue")
    title.draw(win)

    # Welcome message
    welcome = Text(
        Point(GameConfig.WINDOW_WIDTH / 2, 170),
        "Welcome to Maze Adventure! Navigate through the maze,\ncollect coins, and find the exit to win!",
    )
    welcome.setSize(14)
    welcome.draw(win)

    # Start button with Bresenham rectangle border
    start_btn = Button(
        win, Point(GameConfig.WINDOW_WIDTH / 2, 250), 150, 50, "Start Game", use_bresenham=True
    )
    start_btn.rect.setFill("lightgreen")
    start_btn.draw()

    # Settings button with Bresenham rectangle border
    settings_btn = Button(
        win, Point(GameConfig.WINDOW_WIDTH / 2, 320), 150, 50, "Settings", use_bresenham=True
    )
    settings_btn.rect.setFill("lightblue")
    settings_btn.draw()

    # Exit button with Bresenham rectangle border
    exit_btn = Button(win, Point(GameConfig.WINDOW_WIDTH / 2, 390), 150, 50, "Exit", use_bresenham=True)
    exit_btn.rect.setFill("salmon")
    exit_btn.draw()

    # Wait for click
    while True:
        pt = win.getMouse()

        if start_btn.clicked(pt):
            win.close()
            return "start"
        elif settings_btn.clicked(pt):
            win.close()
            return "settings"
        elif exit_btn.clicked(pt):
            win.close()
            return "exit"


def settings_screen():
    # Create settings window
    win = GraphWin("Game Settings", GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
    win.setBackground("white")

    # Title
    title = Text(Point(GameConfig.WINDOW_WIDTH / 2, 70), "Game Settings")
    title.setSize(24)
    title.setStyle("bold")
    title.draw(win)

    # Difficulty settings
    diff_text = Text(Point(GameConfig.WINDOW_WIDTH / 2, 130), "Difficulty Level:")
    diff_text.setSize(16)
    diff_text.draw(win)

    # Create buttons with Bresenham rectangle borders
    easy_btn = Button(win, Point(GameConfig.WINDOW_WIDTH / 4, 180), 120, 40, "Easy", use_bresenham=True)
    easy_btn.rect.setFill("lightgreen")
    easy_btn.draw()

    medium_btn = Button(win, Point(GameConfig.WINDOW_WIDTH / 2, 180), 120, 40, "Medium", use_bresenham=True)
    medium_btn.rect.setFill("yellow")
    medium_btn.draw()

    hard_btn = Button(win, Point(3 * GameConfig.WINDOW_WIDTH / 4, 180), 120, 40, "Hard", use_bresenham=True)
    hard_btn.rect.setFill("salmon")
    hard_btn.draw()

    # Player color selection
    color_text = Text(Point(GameConfig.WINDOW_WIDTH / 2, 250), "Player Color:")
    color_text.setSize(16)
    color_text.draw(win)

    colors = ["red", "green", "blue", "gray", "pink"]
    color_buttons = []

    for i, color in enumerate(colors):
        x_pos = (i + 1) * GameConfig.WINDOW_WIDTH / (len(colors) + 1)
        color_btn = Button(win, Point(x_pos, 300), 80, 40, "", use_bresenham=True)
        color_btn.rect.setFill(color)
        color_btn.draw()
        color_buttons.append((color_btn, color))

    # Back button with Bresenham rectangle border
    back_btn = Button(win, Point(GameConfig.WINDOW_WIDTH / 2, 400), 150, 50, "Back", use_bresenham=True)
    back_btn.draw()

    # Set initial selections based on current settings
    if GameConfig.DIFFICULTY == "easy":
        easy_btn.setSelected(True)
    elif GameConfig.DIFFICULTY == "medium":
        medium_btn.setSelected(True)
    elif GameConfig.DIFFICULTY == "hard":
        hard_btn.setSelected(True)

    # Set initial color selection
    for btn, color in color_buttons:
        if color == GameConfig.PLAYER_COLOR:
            btn.setSelected(True)
            break

    # Wait for clicks
    while True:
        pt = win.getMouse()

        if easy_btn.clicked(pt):
            easy_btn.setSelected()
            medium_btn.setSelected(False)
            hard_btn.setSelected(False)
            GameConfig.DIFFICULTY = "easy"
            GameConfig.CELL_SIZE = 50  # Larger cells for easy mode
            GameConfig.COIN_COUNT = 5

        elif medium_btn.clicked(pt):
            easy_btn.setSelected(False)
            medium_btn.setSelected()
            hard_btn.setSelected(False)
            GameConfig.DIFFICULTY = "medium"
            GameConfig.CELL_SIZE = 40  # Default size
            GameConfig.COIN_COUNT = 10

        elif hard_btn.clicked(pt):
            easy_btn.setSelected(False)
            medium_btn.setSelected(False)
            hard_btn.setSelected()
            GameConfig.DIFFICULTY = "hard"
            GameConfig.CELL_SIZE = 30  # Smaller cells for hard mode
            GameConfig.COIN_COUNT = 15

        for btn, color in color_buttons:
            if btn.clicked(pt):
                GameConfig.PLAYER_COLOR = color

                # Highlight selected color button
                for b, _ in color_buttons:
                    b.setSelected(False)
                btn.setSelected()

        if back_btn.clicked(pt):
            win.close()
            return


def win_screen(score, elapsed_time):
    # Create win window
    win = GraphWin("You Won!", GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
    win.setBackground("#E8F6F3")  # Light teal background for a fresh look

    # Win message
    win_text = Text(Point(GameConfig.WINDOW_WIDTH / 2, 100), "🎉 YOU WIN! 🎉")
    win_text.setSize(36)
    win_text.setStyle("bold")
    win_text.setTextColor("#2E8B57")  # Sea green color
    win_text.draw(win)

    # Score and time display with Bresenham rectangle border
    stats_bg = BresenhamRectangle(
        Point(GameConfig.WINDOW_WIDTH / 2 - 200, 150),
        Point(GameConfig.WINDOW_WIDTH / 2 + 200, 250),
    )
    stats_bg.setFill("white")
    stats_bg.setOutline("#B0C4DE")  # Light steel blue border
    stats_bg.setWidth(2)
    stats_bg.draw(win)

    stats = Text(
        Point(GameConfig.WINDOW_WIDTH / 2, 200),
        f"Score: {score} points\nTime: {elapsed_time} seconds",
    )
    stats.setSize(18)
    stats.setStyle("bold")
    stats.setTextColor("#333333")  # Dark gray text
    stats.draw(win)

    # Buttons with Bresenham rectangle borders
    restart_btn = Button(
        win, Point(GameConfig.WINDOW_WIDTH / 3, 350), 180, 60, "🔄 Play Again", use_bresenham=True
    )
    restart_btn.rect.setFill("#90EE90")  # Light green
    restart_btn.label.setSize(14)
    restart_btn.label.setStyle("bold")
    restart_btn.draw()

    exit_btn = Button(
        win, Point(2 * GameConfig.WINDOW_WIDTH / 3, 350), 180, 60, "❌ Exit", use_bresenham=True
    )
    exit_btn.rect.setFill("#FF7F7F")  # Light red
    exit_btn.label.setSize(14)
    exit_btn.label.setStyle("bold")
    exit_btn.draw()

    # Footer message
    footer = Text(
        Point(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT - 50),
        "Thank you for playing Maze Adventure!",
    )
    footer.setSize(14)
    footer.setTextColor("#555555")  # Medium gray
    footer.draw(win)

    # Wait for click
    while True:
        pt = win.getMouse()

        if restart_btn.clicked(pt):
            win.close()
            return "restart"
        elif exit_btn.clicked(pt):
            win.close()
            return "exit"


def pause_screen(maze_window):
    # Create a semi-transparent overlay
    overlay = Rectangle(
        Point(0, 0), Point(GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
    )
    overlay.setFill("gray")
    overlay.setOutline("gray")
    overlay.setWidth(0)
    overlay.draw(maze_window)

    # Pause menu with Bresenham rectangle border
    menu_bg = BresenhamRectangle(
        Point(GameConfig.WINDOW_WIDTH / 2 - 150, GameConfig.WINDOW_HEIGHT / 2 - 150),
        Point(GameConfig.WINDOW_WIDTH / 2 + 150, GameConfig.WINDOW_HEIGHT / 2 + 150),
    )
    menu_bg.setFill("white")
    menu_bg.setOutline("black")
    menu_bg.setWidth(2)  # Make the border more visible
    menu_bg.draw(maze_window)

    # Title
    pause_text = Text(
        Point(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT / 2 - 100),
        "Game Paused",
    )
    pause_text.setSize(20)
    pause_text.setStyle("bold")
    pause_text.draw(maze_window)

    # Buttons with Bresenham rectangle borders
    resume_btn = Button(
        maze_window,
        Point(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT / 2 - 30),
        200,
        40,
        "Resume",
        use_bresenham=True
    )
    resume_btn.rect.setFill("lightgreen")
    resume_btn.draw()

    settings_btn = Button(
        maze_window,
        Point(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT / 2 + 30),
        200,
        40,
        "Settings",
        use_bresenham=True
    )
    settings_btn.rect.setFill("lightblue")
    settings_btn.draw()

    exit_btn = Button(
        maze_window,
        Point(GameConfig.WINDOW_WIDTH / 2, GameConfig.WINDOW_HEIGHT / 2 + 90),
        200,
        40,
        "Exit",
        use_bresenham=True
    )
    exit_btn.rect.setFill("salmon")
    exit_btn.draw()

    # Wait for click
    while True:
        pt = maze_window.getMouse()

        if resume_btn.clicked(pt):
            overlay.undraw()
            menu_bg.undraw()
            pause_text.undraw()
            resume_btn.undraw()
            settings_btn.undraw()
            exit_btn.undraw()
            return "resume"

        elif settings_btn.clicked(pt):
            # Close pause menu
            overlay.undraw()
            menu_bg.undraw()
            pause_text.undraw()
            resume_btn.undraw()
            settings_btn.undraw()
            exit_btn.undraw()

            # Open settings
            settings_screen()
            return "resume"

        elif exit_btn.clicked(pt):
            return "exit"


def main():
    # Initialize default settings
    GameConfig.DIFFICULTY = "medium"
    GameConfig.PLAYER_COLOR = "blue"
    GameConfig.COIN_COUNT = 10

    # Display welcome screen
    action = welcome_screen()

    while action != "exit":
        if action == "settings":
            settings_screen()
            action = welcome_screen()
            continue

        if action == "start" or action == "restart":
            # Initialize components
            maze = Maze()
            maze.initialize_window()
            maze.draw_maze()

            player = Player(maze)
            player.draw()

            # Exit button in game with Bresenham rectangle border
            exit_btn = Button(
                maze.window,
                Point(GameConfig.WINDOW_WIDTH - 60, 20),
                100,
                30,
                "Exit",
                use_bresenham=True
            )
            exit_btn.rect.setFill("salmon")  # Red color for exit button
            exit_btn.draw()

            # Game loop
            is_game_over = False
            start_time = time.time()

            while not is_game_over:
                # Check for mouse clicks
                pt = maze.window.checkMouse()
                if pt:
                    if exit_btn.clicked(pt):
                        # Exit directly to welcome screen
                        is_game_over = True
                        maze.window.close()
                        action = welcome_screen()
                        break

                # Check for key press
                key = maze.window.checkKey()

                if key == "Escape":
                    pause_result = pause_screen(maze.window)
                    if pause_result == "exit":
                        is_game_over = True
                        maze.window.close()
                        action = welcome_screen()
                        break

                # Update game state based on key press
                if key:
                    game_won = player.handle_key(key)

                    # Update display
                    maze.update_display()

                    # Check for win condition
                    if game_won:
                        is_game_over = True
                        elapsed_time = int(time.time() - start_time)
                        maze.window.close()
                        action = win_screen(maze.score, elapsed_time)
                        break

                # Small delay for smoother gameplay
                time.sleep(0.05)

                # Animate coins
                if (
                    random.random() < 0.1
                ):  # Only animate occasionally to save performance
                    maze.animate_coins()

            # Close window if not already closed
            try:
                if not is_game_over:
                    maze.window.close()
                    action = welcome_screen()
            except:
                action = welcome_screen()
        else:
            break


if __name__ == "__main__":
    try:
        main()
    except GraphicsError:
        # Handle graceful shutdown if window is closed
        pass
