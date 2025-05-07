# Maze Adventure Game

A 2D maze game where you control a character to navigate through a randomly generated maze, collect coins, and reach the end point.

## Features

- Randomly generated maze using recursive backtracking algorithm
- Player movement with keyboard controls (arrow keys or WASD)
- Coin collection system with score tracking
- Timer to track completion time
- Victory celebration with Turtle graphics
- Smooth movement and visual effects

## Requirements

- Python 3.6 or higher
- graphics.py
- PyOpenGL
- turtle
- numpy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/maze-adventure.git
   cd maze-adventure
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```
   python src/main.py
   ```

2. Game Controls:
   - Use arrow keys or WASD to move the player
   - Collect coins to increase your score
   - Reach the red end point to win
   - Press Escape to exit the game

## Project Structure

- `src/main.py`: Main game entry point
- `src/maze.py`: Maze generation and rendering
- `src/player.py`: Player movement and interaction
- `src/effects.py`: Visual effects and animations
- `src/config.py`: Game configuration settings
- `assets/`: Game assets (if any)

## Customization

You can customize the game by editing the `config.py` file:
- Change window size
- Adjust cell size
- Modify colors
- Change difficulty by altering maze generation parameters

## License

This project is licensed under the MIT License - see the LICENSE file for details. 