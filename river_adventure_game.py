import pygame
import random
import sys
import time
import os
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Game variables
BOAT_WIDTH = 70
BOAT_HEIGHT = 100
STONE_WIDTH = 200
STONE_HEIGHT = 40
COIN_SIZE = 30
MAGNET_SIZE = 35
SCROLL_SPEED = 3
PLAYER_SPEED = 5
STONE_SPAWN_RATE = 60  # Lower is more frequent
COIN_SPAWN_RATE = 80   # Lower is more frequent
MAGNET_SPAWN_RATE = 300  # Lower is more frequent
MAGNET_DURATION = 5  # seconds

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('River Adventure')
clock = pygame.time.Clock()

# Asset loading
def load_image(filename):
    """Load an image from the assets folder"""
    return pygame.image.load(os.path.join('assets', filename)).convert_alpha()

# Load images
try:
    boat_img = load_image('boat.png')
    boat_img = pygame.transform.scale(boat_img, (BOAT_WIDTH, BOAT_HEIGHT))
except pygame.error:
    # Fallback to colored rectangle if image not found
    boat_img = pygame.Surface((BOAT_WIDTH, BOAT_HEIGHT))
    boat_img.fill(BLUE)
    print("Warning: Could not load boat.png, using placeholder")

try:
    stone_img = load_image('stone.png')
    stone_img = pygame.transform.scale(stone_img, (STONE_WIDTH, STONE_HEIGHT))
except pygame.error:
    # Fallback to colored rectangle if image not found
    stone_img = pygame.Surface((STONE_WIDTH, STONE_HEIGHT))
    stone_img.fill(RED)
    print("Warning: Could not load stone.png, using placeholder")

try:
    coin_img = load_image('coin.png')
    coin_img = pygame.transform.scale(coin_img, (COIN_SIZE, COIN_SIZE))
except pygame.error:
    # Fallback to colored rectangle if image not found
    coin_img = pygame.Surface((COIN_SIZE, COIN_SIZE))
    coin_img.fill(YELLOW)
    print("Warning: Could not load coin.png, using placeholder")

try:
    magnet_img = load_image('magnet.png')
    # Rotate the magnet image 90 degrees counterclockwise
    magnet_img = pygame.transform.rotate(magnet_img, 90)
    magnet_img = pygame.transform.scale(magnet_img, (MAGNET_SIZE, MAGNET_SIZE))
except pygame.error:
    # Fallback to colored rectangle if image not found
    magnet_img = pygame.Surface((MAGNET_SIZE, MAGNET_SIZE))
    magnet_img.fill(GREEN)
    print("Warning: Could not load magnet.png, using placeholder")

# Try to load background image
try:
    background_img = load_image('background.png')  # Changed to .png
    # Keep original size for tiling instead of stretching
    background_width = background_img.get_width()
    background_height = background_img.get_height()
    has_background = True
except pygame.error:
    has_background = False
    print("Warning: Could not load background.png, using solid color")

# Font setup
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

class Boat:
    def __init__(self):
        self.width = BOAT_WIDTH
        self.height = BOAT_HEIGHT
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        # Position the boat more toward the center of the screen
        self.y = WINDOW_HEIGHT // 2 + 50
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = 3
        self.invulnerable_time = 0
        self.crash_effect_time = 0
        
    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        if direction == 'right' and self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x
    
    def take_damage(self):
        if time.time() > self.invulnerable_time:
            self.health -= 1
            self.invulnerable_time = time.time() + 1  # 1 second invulnerability
            self.crash_effect_time = time.time() + 0.3  # 0.3 second crash effect
            return True
        return False
        
    def draw(self):
        window.blit(boat_img, (self.x, self.y))

class Stone:
    def __init__(self):
        self.width = STONE_WIDTH
        self.height = STONE_HEIGHT
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.speed = SCROLL_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        
    def draw(self):
        window.blit(stone_img, (self.x, self.y))

class Coin:
    def __init__(self):
        self.width = COIN_SIZE
        self.height = COIN_SIZE
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.speed = SCROLL_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.attracted = False
        
    def update(self, boat=None, magnet_active=False):
        if magnet_active and boat:
            # Move toward boat when magnet is active
            self.attracted = True
            dx = boat.x + boat.width/2 - (self.x + self.width/2)
            dy = boat.y + boat.height/2 - (self.y + self.height/2)
            dist = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            self.x += dx / dist * 5
            self.y += dy / dist * 5
        else:
            self.y += self.speed
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self):
        window.blit(coin_img, (self.x, self.y))

class Magnet:
    def __init__(self):
        self.width = MAGNET_SIZE
        self.height = MAGNET_SIZE
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = -self.height
        self.speed = SCROLL_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        
    def draw(self):
        window.blit(magnet_img, (self.x, self.y))

class Particle:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)
        self.speed = random.uniform(0.5, 2)
        self.size = random.randint(1, 3)
        
    def update(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = -5
            self.x = random.randint(0, WINDOW_WIDTH)
            
    def draw(self):
        pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), self.size)

def show_start_screen():
    # Animation variables
    start_time = pygame.time.get_ticks()
    particles = [Particle() for _ in range(20)]
    
    waiting = True
    while waiting:
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - start_time) / 1000.0  # Time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                waiting = False
        
        # Update particles
        for particle in particles:
            particle.update()
        
        # Draw background - same as the main game and end screen
        if has_background:
            for y in range(0, WINDOW_HEIGHT, background_height):
                for x in range(0, WINDOW_WIDTH, background_width):
                    window.blit(background_img, (x, y))
        else:
            # Use the same fallback as the main game
            window.fill((0, 0, 100))  # Dark blue water
            
            # Add animated river current lines
            for i in range(20):
                y_pos = (i * 40 + elapsed * 30) % WINDOW_HEIGHT
                line_width = random.randint(100, 300)
                line_x = random.randint(0, WINDOW_WIDTH - line_width)
                pygame.draw.line(window, (0, 0, 150), 
                                (line_x, y_pos), 
                                (line_x + line_width, y_pos), 2)
        
        # Add dark overlay for night winter ocean feel
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        window.blit(overlay, (0, 0))
        
        # Draw particles on top of overlay
        for particle in particles:
            particle.draw()
        
        # Draw title at top center
        title_bg = pygame.Surface((600, 80), pygame.SRCALPHA)
        title_bg.fill((20, 20, 40, 200))
        window.blit(title_bg, (WINDOW_WIDTH//2 - 300, 50))
        
        # Draw title with shadow effect
        title_shadow = big_font.render('River Adventure', True, BLACK)
        title_text = big_font.render('River Adventure', True, WHITE)
        
        # Add slight floating effect
        title_y_offset = math.sin(elapsed * 1.5) * 3
        
        # Draw shadow slightly offset
        window.blit(title_shadow, (WINDOW_WIDTH//2 - title_shadow.get_width()//2 + 2, 
                                  70 + 2 + title_y_offset))
        # Draw main title
        window.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 
                                70 + title_y_offset))
        

        
        # Create pulsing "Press SPACE to start" text at bottom
        pulse_value = (math.sin(elapsed * 3) + 1) / 2
        pulse_color = (
            int(200 + 55 * pulse_value),
            int(200 + 55 * pulse_value),
            int(255 * pulse_value)
        )
        
        # Create button-like background for the start instruction
        start_bg = pygame.Surface((350, 50), pygame.SRCALPHA)
        start_bg.fill((10, 10, 30, 180 + int(pulse_value * 50)))
        window.blit(start_bg, (WINDOW_WIDTH//2 - 175, WINDOW_HEIGHT - 120))
        
        # Draw pulsing border around the start button
        pygame.draw.rect(window, pulse_color, 
                        (WINDOW_WIDTH//2 - 175, WINDOW_HEIGHT - 120, 350, 50), 2)
        
        instructions = font.render('Press SPACE to Start', True, pulse_color)
        window.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 
                                  WINDOW_HEIGHT - 110))
        
        # Draw styled control instructions
        controls_bg = pygame.Surface((500, 40), pygame.SRCALPHA)
        controls_bg.fill((10, 10, 20, 180))
        window.blit(controls_bg, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT - 60))
        
        controls = font.render('Use LEFT and RIGHT arrow keys to move', True, WHITE)
        window.blit(controls, (WINDOW_WIDTH//2 - controls.get_width()//2, 
                              WINDOW_HEIGHT - 50))
        
        # Draw animated boat in center
        boat_x = WINDOW_WIDTH//2 - BOAT_WIDTH//2
        boat_y = WINDOW_HEIGHT//2 + math.sin(elapsed * 2) * 8
        
        if 'boat_img' in globals():
            window.blit(boat_img, (boat_x, boat_y))
        else:
            pygame.draw.rect(window, BLUE, (boat_x, boat_y, BOAT_WIDTH, BOAT_HEIGHT))
        
        # Draw coins around the boat
        coin_positions = [
            (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 80, COIN_SIZE),
            (WINDOW_WIDTH//2 + 120, WINDOW_HEIGHT//2 - 60, COIN_SIZE * 1.5),
            (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 100, COIN_SIZE * 1.2)
        ]
        
        for i, (x_pos, y_pos, size) in enumerate(coin_positions):
            y_pos += math.sin(elapsed * 2 + i) * 8
            
            if 'coin_img' in globals():
                scaled_coin = pygame.transform.scale(coin_img, (int(size), int(size)))
                window.blit(scaled_coin, (x_pos, y_pos))
            else:
                pygame.draw.circle(window, YELLOW, (int(x_pos + size/2), int(y_pos + size/2)), int(size//2))
        

        
        pygame.display.update()
        clock.tick(60)  # Cap the frame rate

def show_game_over(score):
    # Animation variables
    start_time = pygame.time.get_ticks()
    
    waiting = True
    while waiting:
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - start_time) / 1000.0  # Time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting = False
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
        
        # Draw background - same as the start screen and main game
        if has_background:
            for y in range(0, WINDOW_HEIGHT, background_height):
                for x in range(0, WINDOW_WIDTH, background_width):
                    window.blit(background_img, (x, y))
        else:
            # Use the same fallback as the main game
            window.fill((0, 0, 100))  # Dark blue water
            
            # Add some river current lines
            for i in range(20):
                y_pos = (i * 40 + elapsed * 50) % WINDOW_HEIGHT
                line_width = random.randint(100, 300)
                line_x = random.randint(0, WINDOW_WIDTH - line_width)
                pygame.draw.line(window, (0, 0, 150), 
                                (line_x, y_pos), 
                                (line_x + line_width, y_pos), 2)
        
        # Draw a darkened overlay to make text more visible
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Darker overlay for game over
        window.blit(overlay, (0, 0))
        
        # Draw game over text with pulsing effect
        pulse_value = (math.sin(elapsed * 2) + 1) / 2  # Value between 0 and 1
        red_pulse = max(150, int(255 * pulse_value))
        game_over_color = (red_pulse, 0, 0)  # Pulsing red
        
        game_over_text = big_font.render('GAME OVER', True, game_over_color)
        window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                                    WINDOW_HEIGHT//3))
        
        # Draw score with a highlight effect
        score_bg = pygame.Surface((300, 60), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 150))
        window.blit(score_bg, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 10))
        
        score_text = font.render(f'Final Score: {score}', True, YELLOW)  # Use coin color for score
        window.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, WINDOW_HEIGHT//2))
        
        # Draw instruction buttons with a style matching the game
        restart_bg = pygame.Surface((350, 40), pygame.SRCALPHA)
        restart_bg.fill((0, 0, 100, 150))
        window.blit(restart_bg, (WINDOW_WIDTH//2 - 175, WINDOW_HEIGHT//2 + 60))
        
        restart_text = font.render('Press SPACE to play again', True, WHITE)
        window.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                                  WINDOW_HEIGHT//2 + 65))
        
        quit_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
        quit_bg.fill((100, 0, 0, 150))
        window.blit(quit_bg, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 120))
        
        quit_text = font.render('Press Q to quit', True, WHITE)
        window.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 
                               WINDOW_HEIGHT//2 + 125))
        
        # Draw some game elements in the background
        
        # Draw twinkling particles
        for i in range(50):
            x_pos = random.randint(0, WINDOW_WIDTH)
            y_pos = random.randint(0, WINDOW_HEIGHT)
            particle_alpha = random.randint(50, 200)
            particle_size = random.randint(1, 4)
            
            particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (255, 255, 255, particle_alpha), (particle_size, particle_size), particle_size)
            window.blit(particle_surface, (x_pos, y_pos))
        
        pygame.display.update()
        clock.tick(60)

def main():
    show_start_screen()
    
    while True:
        # Game setup
        boat = Boat()
        stones = []
        coins = []
        magnets = []
        particles = [Particle() for _ in range(30)]
        score = 0
        magnet_active = False
        magnet_end_time = 0
        game_over = False
        screen_shake = 0
        last_stone_spawn = 0
        
        # Main game loop
        while not game_over:
            # Process events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            
            # Get key presses
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                boat.move('left')
            if keys[K_RIGHT]:
                boat.move('right')
            
            # Check if magnet power-up is active
            if magnet_active and time.time() > magnet_end_time:
                magnet_active = False
            
            # Spawn objects
            if random.randint(1, STONE_SPAWN_RATE) == 1:
                new_stone = Stone()
                # Check horizontal spacing to avoid clustering
                can_spawn = True
                for existing_stone in stones:
                    if existing_stone.y < 150 and abs(existing_stone.x - new_stone.x) < 250:
                        can_spawn = False
                        break
                if can_spawn:
                    stones.append(new_stone)
                
            if random.randint(1, COIN_SPAWN_RATE) == 1:
                coins.append(Coin())
                
            if random.randint(1, MAGNET_SPAWN_RATE) == 1:
                magnets.append(Magnet())
            
            # Update objects
            for particle in particles:
                particle.update()
                
            for stone in stones[:]:
                stone.update()
                # Check collision with boat
                if stone.rect.colliderect(boat.rect):
                    if boat.take_damage():
                        stones.remove(stone)
                        screen_shake = 10
                        if boat.health <= 0:
                            game_over = True
                # Remove if off screen
                elif stone.y > WINDOW_HEIGHT:
                    stones.remove(stone)
            
            for coin in coins[:]:
                coin.update(boat, magnet_active)
                # Check collision with boat
                if coin.rect.colliderect(boat.rect):
                    coins.remove(coin)
                    score += 10
                # Remove if off screen
                elif coin.y > WINDOW_HEIGHT:
                    coins.remove(coin)
            
            for magnet in magnets[:]:
                magnet.update()
                # Check collision with boat
                if magnet.rect.colliderect(boat.rect):
                    magnets.remove(magnet)
                    magnet_active = True
                    magnet_end_time = time.time() + MAGNET_DURATION
                # Remove if off screen
                elif magnet.y > WINDOW_HEIGHT:
                    magnets.remove(magnet)
            
            # Apply screen shake
            shake_x = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
            shake_y = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
            screen_shake = max(0, screen_shake - 1)
            
            # Draw everything
            window.fill(BLACK)
            
            # Draw background
            if has_background:
                # Tile the background image instead of stretching it
                for y in range(0, WINDOW_HEIGHT, background_height):
                    for x in range(0, WINDOW_WIDTH, background_width):
                        window.blit(background_img, (x, y))
            else:
                # Blue background as water
                window.fill(BLUE)
            
            # Add dark overlay for night winter ocean feel
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            window.blit(overlay, (0, 0))
            
            # Draw particles on top of overlay
            for particle in particles:
                particle.draw()
                
            # Draw objects with shake effect
            window.blit(boat_img, (boat.x + shake_x, boat.y + shake_y))
            for stone in stones:
                window.blit(stone_img, (stone.x + shake_x, stone.y + shake_y))
            for coin in coins:
                window.blit(coin_img, (coin.x + shake_x, coin.y + shake_y))
            for magnet in magnets:
                window.blit(magnet_img, (magnet.x + shake_x, magnet.y + shake_y))
            
            # Draw crash effect (red flash)
            if time.time() < boat.crash_effect_time:
                crash_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                crash_overlay.fill((255, 0, 0, 100))
                window.blit(crash_overlay, (0, 0))
            
            # Draw score and health
            score_text = font.render(f'Score: {score}', True, WHITE)
            window.blit(score_text, (10, 10))
            
            health_text = font.render(f'Health: {boat.health}', True, RED)
            window.blit(health_text, (10, 50))
            
            # Draw magnet timer if active
            if magnet_active:
                time_left = int(magnet_end_time - time.time())
                magnet_text = font.render(f'Magnet: {time_left}s', True, GREEN)
                window.blit(magnet_text, (10, 90))
            
            pygame.display.update()
            clock.tick(FPS)
        
        # Game over
        show_game_over(score)

if __name__ == '__main__':
    main()
