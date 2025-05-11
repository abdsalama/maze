import time
import random
import math
from graphics import *
from config import GameConfig
from drawing_utils import MidpointCircle, BresenhamLine

class Effects:
    def __init__(self):
        self.window = None

    def victory_effect(self):
        """Show victory animation with graphics library"""
        self._draw_graphics_victory()

    def _draw_graphics_victory(self):
        """Show victory message using graphics library"""
        self.window = GraphWin("Victory!", 400, 300)
        self.window.setBackground("black")

        # Victory message
        msg = Text(Point(200, 150), "YOU WIN!")
        msg.setTextColor("gold")
        msg.setSize(36)
        msg.setStyle("bold")
        msg.draw(self.window)

        # Add some graphical effects using our custom algorithms
        self._add_victory_effects(self.window)

        # Wait and close
        time.sleep(3)
        self.window.close()

    def _add_victory_effects(self, window):
        """Add graphical effects to victory screen using graphics library"""
        # Create sparkles around the text
        for i in range(8):
            angle = 2 * math.pi * i / 8
            x = 200 + 100 * math.cos(angle)
            y = 150 + 80 * math.sin(angle)

            # Create sparkle using MidpointCircle
            sparkle = MidpointCircle(Point(x, y), 5)
            sparkle.setFill("yellow")
            sparkle.setOutline("gold")
            sparkle.draw(window)

            # Create rays using BresenhamLine
            for j in range(4):
                ray_angle = angle + j * math.pi/4
                end_x = x + 15 * math.cos(ray_angle)
                end_y = y + 15 * math.sin(ray_angle)

                ray = BresenhamLine(Point(x, y), Point(end_x, end_y))
                ray.color = "gold"
                ray.draw(window)

    def create_fireworks(self, window, num_fireworks=10):
        """Make colorful fireworks for victory screen using Bresenham lines."""
        fireworks = []

        for _ in range(num_fireworks):
            # Random position
            x = random.randint(50, GameConfig.WINDOW_WIDTH-50)
            y = random.randint(50, GameConfig.WINDOW_HEIGHT-50)

            # Random color
            r = random.random()
            g = random.random()
            b = random.random()

            # Create firework using Bresenham lines
            firework = self._create_single_firework(window, x, y, (r, g, b))
            fireworks.append(firework)

        return fireworks

    def _create_single_firework(self, window, x, y, color):
        """Make one firework explosion using Bresenham algorithm"""
        particles = []
        num_particles = random.randint(8, 16)

        for i in range(num_particles):
            angle = 2 * math.pi * i / num_particles
            length = random.randint(20, 50)

            # Calculate end points
            end_x = x + length * math.cos(angle)
            end_y = y + length * math.sin(angle)

            # Create line for explosion using Bresenham algorithm
            line = BresenhamLine(Point(x, y), Point(end_x, end_y))
            line.color = color_rgb(int(color[0]*255), int(color[1]*255), int(color[2]*255))
            line.width = 2
            line.draw(window)

            particles.append(line)

        return particles

    def animate_fireworks(self, window, fireworks, duration=3):
        """Make fireworks change colors"""
        start_time = time.time()

        while time.time() - start_time < duration:
            # Update fireworks
            for particle_set in fireworks:
                for particle in particle_set:
                    # Random color change
                    r = random.random()
                    g = random.random()
                    b = random.random()

                    # Undraw and redraw with new color (since Bresenham lines need to be redrawn to change color)
                    particle.undraw()
                    particle.color = color_rgb(int(r*255), int(g*255), int(b*255))
                    particle.draw(window)

            # Small delay for animation
            time.sleep(0.1)
            window.update()

    def coin_collect_effect(self, x, y, window):
        """Create sparkle effect when collecting a coin."""
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
        for _ in range(5):  # Loop 5 times for animation steps
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
        """Make fancy text with sparkles"""
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
        """Make text change colors"""
        colors = ["gold", "orange", "yellow", "red", "purple", "blue"]
        start_time = time.time()

        while time.time() - start_time < duration:
            # Cycle through colors
            color = colors[int(time.time() * 3) % len(colors)]
            text_obj.setTextColor(color)

            # Small delay
            time.sleep(0.1)

    def create_sparkle_effect(self, window, x, y):
        """Make a sparkle at a position using MidpointCircle algorithm"""
        sparkles = []

        # Create a central circle
        center_circle = MidpointCircle(Point(x, y), 5)
        center_circle.setFill("gold")
        center_circle.setOutline("yellow")
        center_circle.draw(window)
        sparkles.append(center_circle)

        # Create rays using Bresenham lines
        for i in range(8):
            angle = 2 * math.pi * i / 8
            end_x = x + 10 * math.cos(angle)
            end_y = y + 10 * math.sin(angle)

            ray = BresenhamLine(Point(x, y), Point(end_x, end_y))
            ray.color = "gold"
            ray.draw(window)
            sparkles.append(ray)

        # Animate sparkle
        for i in range(5):
            # Pulse color
            color = "gold" if i % 2 == 0 else "yellow"

            # Update central circle
            center_circle.undraw()
            center_circle.setFill(color)
            center_circle.draw(window)

            # Update rays
            for j in range(1, len(sparkles)):
                sparkles[j].undraw()
                sparkles[j].color = color
                sparkles[j].draw(window)

            time.sleep(0.1)
            window.update()

        # Return all sparkle elements
        return sparkles