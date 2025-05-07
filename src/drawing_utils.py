from graphics import *
import math

def draw_midpoint_circle(window, center_x, center_y, radius, fill_color, outline_color=None, width=1):
    """
    Draw a circle using the midpoint circle algorithm.

    Args:
        window: The GraphWin window to draw on
        center_x, center_y: The center coordinates of the circle
        radius: The radius of the circle
        fill_color: The color to fill the circle with
        outline_color: The color of the outline (if None, uses fill_color)
        width: The width of the outline

    Returns:
        A list of all the points/pixels that make up the circle
    """
    # If no outline color specified, use the fill color
    if outline_color is None:
        outline_color = fill_color

    # Initialize lists to store all points
    points = []

    # Convert radius to integer for the algorithm
    radius_int = int(radius)
    if radius_int < 1:
        radius_int = 1

    # Initial point
    x = 0
    y = radius_int

    # Initial decision parameter
    p = 1 - radius_int

    # Store the 8-way symmetric points
    plot_circle_points(window, center_x, center_y, x, y, fill_color, outline_color, width, points)

    # Midpoint circle algorithm
    while x < y:
        x += 1

        # Update decision parameter
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

        # Plot the points in all octants
        plot_circle_points(window, center_x, center_y, x, y, fill_color, outline_color, width, points)

    # Fill the circle
    fill_circle(window, center_x, center_y, radius, fill_color, points)

    return points

def plot_circle_points(window, center_x, center_y, x, y, fill_color, outline_color, width, points_list):
    """
    Plot points in all 8 octants of the circle.

    Args:
        window: The GraphWin window to draw on
        center_x, center_y: The center coordinates of the circle
        x, y: The current point relative to the center
        fill_color: The color to fill the circle with
        outline_color: The color of the outline
        width: The width of the outline
        points_list: List to store all points
    """
    # Plot points in all 8 octants
    plot_point(window, center_x + x, center_y + y, outline_color, width, points_list)
    plot_point(window, center_x - x, center_y + y, outline_color, width, points_list)
    plot_point(window, center_x + x, center_y - y, outline_color, width, points_list)
    plot_point(window, center_x - x, center_y - y, outline_color, width, points_list)
    plot_point(window, center_x + y, center_y + x, outline_color, width, points_list)
    plot_point(window, center_x - y, center_y + x, outline_color, width, points_list)
    plot_point(window, center_x + y, center_y - x, outline_color, width, points_list)
    plot_point(window, center_x - y, center_y - x, outline_color, width, points_list)

def plot_point(window, x, y, color, width, points_list):
    """
    Plot a single point on the window.

    Args:
        window: The GraphWin window to draw on
        x, y: The coordinates of the point
        color: The color of the point
        width: The width of the point
        points_list: List to store all points
    """
    # Create a small rectangle to represent a pixel
    pixel = Rectangle(Point(x - width/2, y - width/2), Point(x + width/2, y + width/2))
    pixel.setFill(color)
    pixel.setOutline(color)
    pixel.draw(window)

    # Add the point to the list
    points_list.append(pixel)

def fill_circle(window, center_x, center_y, radius, fill_color, outline_points):
    """
    Fill the circle with the specified color using an optimized approach.

    Args:
        window: The GraphWin window to draw on
        center_x, center_y: The center coordinates of the circle
        radius: The radius of the circle
        fill_color: The color to fill the circle with
        outline_points: List of points that make up the outline
    """
    # Convert to integers for range operations
    center_x_int = int(center_x)
    center_y_int = int(center_y)
    radius_int = int(radius)

    # Use fewer scan lines for better performance
    step = max(1, radius_int // 10)  # Adjust step size based on radius

    # Simple scan-line fill algorithm with optimization
    for y in range(center_y_int - radius_int + 1, center_y_int + radius_int, step):
        # Calculate x bounds for this y
        dy = y - center_y
        dx = int((radius**2 - dy**2)**0.5) if (radius**2 - dy**2) > 0 else 0

        # Draw horizontal lines with larger rectangles for efficiency
        left_x = center_x_int - dx + 1
        right_x = center_x_int + dx - 1

        if right_x > left_x:
            # Create a rectangle for the entire horizontal line
            fill_rect = Rectangle(Point(left_x, y), Point(right_x, y + step - 1))
            fill_rect.setFill(fill_color)
            fill_rect.setOutline(fill_color)
            fill_rect.draw(window)
            outline_points.append(fill_rect)

class MidpointCircle:
    """
    A class to represent a circle drawn using the midpoint circle algorithm.
    This class mimics the interface of the Circle class from graphics.py.
    """

    def __init__(self, center_point, radius):
        """
        Initialize a new MidpointCircle.

        Args:
            center_point: A Point object representing the center of the circle
            radius: The radius of the circle
        """
        self.center = center_point
        self.radius = radius
        self.fill_color = "white"
        self.outline_color = "black"
        self.width = 1
        self.canvas = None
        self.points = []

    def draw(self, window):
        """
        Draw the circle on the window.

        Args:
            window: The GraphWin window to draw on
        """
        self.canvas = window
        self.points = draw_midpoint_circle(
            window,
            self.center.getX(),
            self.center.getY(),
            self.radius,
            self.fill_color,
            self.outline_color,
            self.width
        )
        return self

    def undraw(self):
        """Remove the circle from the window."""
        if self.canvas:
            for point in self.points:
                point.undraw()
            self.canvas = None

    def setFill(self, color):
        """Set the fill color of the circle."""
        self.fill_color = color
        return self

    def setOutline(self, color):
        """Set the outline color of the circle."""
        self.outline_color = color
        return self

    def setWidth(self, width):
        """Set the width of the outline."""
        self.width = width
        return self

    def getCenter(self):
        """Return the center point of the circle."""
        return self.center

    def getRadius(self):
        """Return the radius of the circle."""
        return self.radius

    def move(self, dx, dy):
        """Move the circle by the given amount."""
        # Update the center point
        new_x = self.center.getX() + dx
        new_y = self.center.getY() + dy
        self.center = Point(new_x, new_y)

        # If the circle is drawn, redraw it at the new position
        if self.canvas:
            # Store the canvas before undrawing
            canvas = self.canvas
            self.undraw()
            # Use the stored canvas reference
            self.draw(canvas)

        return self


def draw_bresenham_line(window, x1, y1, x2, y2, color, width=1):
    """
    Draw a line using the Bresenham line algorithm.

    Args:
        window: The GraphWin window to draw on
        x1, y1: The starting point coordinates
        x2, y2: The ending point coordinates
        color: The color of the line
        width: The width of the line

    Returns:
        A list of all the points/pixels that make up the line
    """
    # Initialize list to store all points
    points = []

    # Calculate differences
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Determine direction of movement
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    # Initial error
    err = dx - dy

    # Current position
    x, y = x1, y1

    # Bresenham algorithm
    while True:
        # Plot the current point
        plot_point(window, x, y, color, width, points)

        # Check if we've reached the end point
        if x == x2 and y == y2:
            break

        # Calculate error for next step
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    return points


def draw_rectangle_border(window, x1, y1, x2, y2, color, width=1):
    """
    Draw a rectangle border using the Bresenham line algorithm.

    Args:
        window: The GraphWin window to draw on
        x1, y1: The top-left corner coordinates
        x2, y2: The bottom-right corner coordinates
        color: The color of the border
        width: The width of the border

    Returns:
        A list of all the points/pixels that make up the rectangle border
    """
    points = []

    # Draw the four sides of the rectangle
    points.extend(draw_bresenham_line(window, x1, y1, x2, y1, color, width))  # Top
    points.extend(draw_bresenham_line(window, x2, y1, x2, y2, color, width))  # Right
    points.extend(draw_bresenham_line(window, x2, y2, x1, y2, color, width))  # Bottom
    points.extend(draw_bresenham_line(window, x1, y2, x1, y1, color, width))  # Left

    return points


class BresenhamLine:
    """
    A class to represent a line drawn using the Bresenham line algorithm.
    This class mimics the interface of the Line class from graphics.py.
    """

    def __init__(self, point1, point2):
        """
        Initialize a new BresenhamLine.

        Args:
            point1: A Point object representing the start point of the line
            point2: A Point object representing the end point of the line
        """
        self.point1 = point1
        self.point2 = point2
        self.color = "black"
        self.width = 1
        self.canvas = None
        self.points = []

    def draw(self, window):
        """
        Draw the line on the window.

        Args:
            window: The GraphWin window to draw on
        """
        self.canvas = window
        self.points = draw_bresenham_line(
            window,
            self.point1.getX(),
            self.point1.getY(),
            self.point2.getX(),
            self.point2.getY(),
            self.color,
            self.width
        )
        return self

    def undraw(self):
        """Remove the line from the window."""
        if self.canvas:
            for point in self.points:
                point.undraw()
            self.canvas = None

    def setFill(self, color):
        """Set the color of the line."""
        self.color = color
        return self

    def setOutline(self, color):
        """Set the color of the line (alias for setFill)."""
        return self.setFill(color)

    def setWidth(self, width):
        """Set the width of the line."""
        self.width = width
        return self

    def getP1(self):
        """Return the start point of the line."""
        return self.point1

    def getP2(self):
        """Return the end point of the line."""
        return self.point2


class BresenhamRectangle:
    """
    A class to represent a rectangle drawn using the Bresenham line algorithm.
    This class mimics the interface of the Rectangle class from graphics.py.
    """

    def __init__(self, point1, point2):
        """
        Initialize a new BresenhamRectangle.

        Args:
            point1: A Point object representing the top-left corner of the rectangle
            point2: A Point object representing the bottom-right corner of the rectangle
        """
        self.point1 = point1
        self.point2 = point2
        self.fill_color = None
        self.outline_color = "black"
        self.width = 1
        self.canvas = None
        self.points = []
        self.fill_rectangle = None

    def draw(self, window):
        """
        Draw the rectangle on the window.

        Args:
            window: The GraphWin window to draw on
        """
        self.canvas = window

        # Draw fill if specified
        if self.fill_color:
            self.fill_rectangle = Rectangle(self.point1, self.point2)
            self.fill_rectangle.setFill(self.fill_color)
            self.fill_rectangle.setOutline(self.fill_color)
            self.fill_rectangle.draw(window)

        # Draw border using Bresenham lines
        self.points = draw_rectangle_border(
            window,
            self.point1.getX(),
            self.point1.getY(),
            self.point2.getX(),
            self.point2.getY(),
            self.outline_color,
            self.width
        )
        return self

    def undraw(self):
        """Remove the rectangle from the window."""
        if self.canvas:
            if self.fill_rectangle:
                self.fill_rectangle.undraw()
            for point in self.points:
                point.undraw()
            self.canvas = None

    def setFill(self, color):
        """Set the fill color of the rectangle."""
        self.fill_color = color
        return self

    def setOutline(self, color):
        """Set the outline color of the rectangle."""
        self.outline_color = color
        return self

    def setWidth(self, width):
        """Set the width of the outline."""
        self.width = width
        return self

    def getP1(self):
        """Return the top-left corner of the rectangle."""
        return self.point1

    def getP2(self):
        """Return the bottom-right corner of the rectangle."""
        return self.point2
