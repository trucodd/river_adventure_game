# River Adventure Game

A Pygame-based river adventure game where you navigate a boat down a river, collecting coins while avoiding obstacles.

## Game Structure

- `river_adventure_game.py`: Main game file containing all game logic
- `assets/`: Directory containing game images
  - `boat.png`: Player's boat image
  - `stone.png`: Obstacle image
  - `coin.png`: Collectible coin image
  - `magnet.png`: Power-up that attracts coins
  - `background.png`: River background image

## How to Play

1. Run the game: `python river_adventure_game.py`
2. Use LEFT and RIGHT arrow keys to navigate the boat
3. Collect coins to increase your score
4. Avoid hitting stones
5. Collect magnets to attract nearby coins

## Adding Your Own Assets

You can easily customize the game by adding your own images to the `assets/` folder:

1. Create your own images with the following names:
   - `boat.png`
   - `stone.png`
   - `coin.png`
   - `magnet.png`
   - `background.jpg`
2. Place them in the `assets/` folder
3. The game will automatically use your images

If any image is missing, the game will fall back to using colored shapes as placeholders.

## Game Features

- Boat navigation
- Obstacle avoidance
- Coin collection
- Magnet power-up that attracts coins
- Score tracking
- Game over screen with restart option
