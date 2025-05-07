import turtle
import time
import random
import math
from graphics import *
from config import GameConfig
from drawing_utils import MidpointCircle

class Effects:
    def __init__(self):
        self.screen = None
        self.window = None

    def init_turtle(self):
        """Initialize turtle for effect animations"""
        self.screen = turtle.Screen()
        self.screen.setup(GameConfig.WINDOW_WIDTH, GameConfig.WINDOW_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Game Victory!")

        # Create turtle for drawing
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)

    def victory_effect(self):
        """Display a victory animation using Turtle - kept for compatibility"""
        # This is no longer the primary victory screen
        # The main.py win_screen function handles the victory display
        self._draw_simple_victory()

    def _draw_simple_victory(self):
        """Simple victory message for backward compatibility"""
        self.window = GraphWin("Victory!", 400, 300)
        self.window.setBackground("black")

        # Victory message
        msg = Text(Point(200, 150), "YOU WIN!")
        msg.setTextColor("gold")
        msg.setSize(36)
        msg.setStyle("bold")
        msg.draw(self.window)

        # Wait and close
        time.sleep(3)
        self.window.close()

    def create_fireworks(self, window, num_fireworks=10):
        """Create firework decorations for the victory screen"""
        fireworks = []

        for _ in range(num_fireworks):
            # Random position
            x = random.randint(50, GameConfig.WINDOW_WIDTH-50)
            y = random.randint(50, GameConfig.WINDOW_HEIGHT-50)

            # Random color
            r = random.random()
            g = random.random()
            b = random.random()

            # Create firework
            firework = self._create_single_firework(window, x, y, (r, g, b))
            fireworks.append(firework)

        return fireworks

    def _create_single_firework(self, window, x, y, color):
        """Create a single firework explosion effect"""
        particles = []
        num_particles = random.randint(8, 16)

        for i in range(num_particles):
            angle = 2 * math.pi * i / num_particles
            length = random.randint(20, 50)

            # Calculate end points
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)

            # Create line for explosion
            line = Line(Point(x, y), Point(end_x, end_y))
            line.setFill(color_rgb(int(color[0]*255), int(color[1]*255), int(color[2]*255)))
            line.setWidth(2)
            line.draw(window)

            particles.append(line)

        return particles

    def animate_fireworks(self, window, fireworks, duration=3):
        """Animate fireworks by changing their colors"""
        start_time = time.time()

        while time.time() - start_time < duration:
            # Update fireworks
            for particle_set in fireworks:
                for particle in particle_set:
                    # Random color change
                    r = random.random()
                    g = random.random()
                    b = random.random()
                    particle.setFill(color_rgb(int(r*255), int(g*255), int(b*255)))

            # Small delay for animation
            time.sleep(0.1)
            window.update()

    def coin_collect_effect(self, x, y, window):
        """Create a sparkle effect when collecting a coin using midpoint circle algorithm"""
        # Create particles that expand and fade
        particles = []
        num_particles = 8

        for i in range(num_particles):
            angle = 2 * math.pi * i / num_particles

            # Create particle using midpoint circle algorithm
            particle = MidpointCircle(Point(x, y), 2)
            particle.setFill("gold")
            particle.setOutline("yellow")
            particle.draw(window)

            # Store particle with its angle
            particles.append((particle, angle))

        # Animate particles
        for size in range(5):
            # Update particles
            for particle, angle in particles:
                # Move outward
                dx = 3 * math.cos(angle)
                dy = 3 * math.sin(angle)
                particle.move(dx, dy)

                # Increase size slightly
                current_radius = particle.getRadius()
                particle.undraw()
                particle = MidpointCircle(particle.getCenter(), current_radius + 0.5)
                particle.setFill("gold")
                particle.setOutline("yellow")
                particle.draw(window)

            # Wait briefly
            time.sleep(0.05)
            window.update()

        # Clean up
        for particle, _ in particles:
            particle.undraw()

    def create_ui_decoration(self, window, text, position, color="gold"):
        """Create a decorated text with sparkles"""
        # Create main text
        main_text = Text(position, text)
        main_text.setStyle("bold")
        main_text.setSize(24)
        main_text.setTextColor(color)
        main_text.draw(window)

        # Create decorative elements around text
        decorations = []

        # Add stars around text
        for i in range(8):
            angle = 2 * math.pi * i / 8
            offset_x = 40 * math.cos(angle)
            offset_y = 40 * math.sin(angle)

            star = Text(Point(position.getX() + offset_x, position.getY() + offset_y), "★")
            star.setSize(18)
            star.setTextColor(color)
            star.draw(window)

            decorations.append(star)

        return main_text, decorations

    def animate_text(self, text_obj, duration=3):
        """Animate text with color cycling"""
        colors = ["gold", "orange", "yellow", "red", "purple", "blue"]
        start_time = time.time()

        while time.time() - start_time < duration:
            # Cycle through colors
            color = colors[int(time.time() * 3) % len(colors)]
            text_obj.setTextColor(color)

            # Small delay
            time.sleep(0.1)

    def create_sparkle_effect(self, window, x, y):
        """Create a sparkle effect at a position"""
        sparkle = Text(Point(x, y), "✨")
        sparkle.setSize(20)
        sparkle.setTextColor("gold")
        sparkle.draw(window)

        # Animate sparkle
        for i in range(5):
            # Pulse size
            size = 16 + i * 2
            sparkle.setSize(size)

            # Pulse color
            if i % 2 == 0:
                sparkle.setTextColor("gold")
            else:
                sparkle.setTextColor("yellow")

            time.sleep(0.1)

        return sparkle