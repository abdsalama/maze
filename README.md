# Maze Adventure Game

A 2D maze game where you control a character to navigate through a randomly generated maze, collect coins, and reach the end point. This project implements various computer graphics algorithms including Bresenham's line algorithm and Midpoint Circle algorithm.

## Screenshots

![Game Welcome Screen](Screenshots/Screenshot%20(1).png)
![Gameplay](Screenshots/Screenshot%20(2).png)
![Victory Screen](Screenshots/Screenshot%20(3).png)

## Features

- Randomly generated maze using recursive backtracking algorithm
- Player movement with keyboard controls (arrow keys or WASD)
- Coin collection system with score tracking
- Timer to track completion time
- Victory celebration with custom graphics effects
- Implementation of computer graphics algorithms:
  - Bresenham's Line Algorithm for drawing lines
  - Midpoint Circle Algorithm for drawing circles
  - Scan-line fill algorithm for filling shapes
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

## Acknowledgments

This project was developed as part of the Computer Graphics course at Faculty of Computers and Information.

### Supervisor
- **Dr. Heba El Hadidi** - Project supervisor and evaluator

### Team Members
- Abd-Elrahman Mohammed Salama Eltahrany
- Osama Hamed Elkayyal
- Fedaa Mohammed Elkanishey
- Ahmed Elsharabasy

## License

This project is licensed under the MIT License - see the LICENSE file for details.