import pygame
import random
import sys

# Constants
WINDOW_SIZE = (800, 800)
GRID_SIZE = 10
TILE_SIZE = WINDOW_SIZE[0] // GRID_SIZE
FONT_SIZE = 52
WINNER_FONT_SIZE = 75
TEXT_MARGIN = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
ORANGE = (255, 165, 0)

# Game Variables
number_of_lives = 3
memory_time_limit = 5000 # [ms]

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinth Memory Trainer")

def generate_labyrinth(n):
    # Initialize an NxN grid with all paths
    grid = [['path' for _ in range(n)] for _ in range(n)]
    
    # Randomly place walls
    for i in range(n):
        for j in range(n):
            if random.choice([True, False]):
                grid[i][j] = 'wall'
    
    # Ensure at least one path from entry to exit
    # Simple solution: clear a straight path
    for i in range(n):
        grid[i][0] = 'path'
        grid[n-1][i] = 'path'
    
    return grid

def draw_labyrinth(window, labyrinth, show_walls, revealed_walls):
    for y, row in enumerate(labyrinth):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'wall':
                if show_walls:
                    pygame.draw.rect(window, BLACK, rect)
                elif (x, y) in revealed_walls:
                    pygame.draw.rect(window, GRAY, rect)  # Draw gray for revealed walls
                else:
                    pygame.draw.rect(window, WHITE, rect)
            else:
                pygame.draw.rect(window, WHITE, rect)
            pygame.draw.rect(window, GRAY, rect, 1)  # Grid lines

def handle_player_movement(player_position, direction, labyrinth, revealed_walls):
    global number_of_lives

    x, y = player_position
    move = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
    dx, dy = move[direction]
    new_x, new_y = x + dx, y + dy

    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        if labyrinth[new_y][new_x] == 'wall':
            revealed_walls.add((new_x, new_y))  # Add to revealed walls
            number_of_lives -= 1
        else:
            return new_x, new_y

    return x, y

def main():
    global number_of_lives, memory_time_limit

    #
    # SETUP
    #

    labyrinth = generate_labyrinth(GRID_SIZE)
    player_position = (0, 0)
    start_position = (0, 0)
    finish_position = (GRID_SIZE - 1, GRID_SIZE - 1)
    show_walls = True
    revealed_walls = set()  # Set to keep track of revealed walls
    game_over = False
    start_time = pygame.time.get_ticks()  # Start time

    clock = pygame.time.Clock()  # Pygame clock for tracking time

    #
    # MAIN LOOP
    #

    running = True
    while running:
        if not game_over:
            elapsed_time = pygame.time.get_ticks() - start_time  # Update elapsed time only if the game is not over
        memo_time = max(memory_time_limit - elapsed_time, 0) // 1000  # Calculate memo time in seconds

        # Check for keyboard inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                direction = None
                if event.key == pygame.K_UP:
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                elif event.key == pygame.K_LEFT:
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'

                if direction:
                    if show_walls:
                        show_walls = False
                    player_position = handle_player_movement(player_position, direction, labyrinth, revealed_walls)
                
        # Toggle visibility after 5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - start_time > memory_time_limit:  # 5000 milliseconds
            show_walls = False

        window.fill(GRAY)
        draw_labyrinth(window, labyrinth, show_walls, revealed_walls)

        # Draw the start and finish squares
        start_rect = pygame.Rect(start_position[0] * TILE_SIZE, start_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(window, DARK_GREEN, start_rect)
        finish_rect = pygame.Rect(finish_position[0] * TILE_SIZE, finish_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(window, RED, finish_rect)

        # Draw the player
        player_rect = pygame.Rect(player_position[0] * TILE_SIZE, player_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(window, GREEN, player_rect)

        # Check if player reaches the finish point
        if player_position == finish_position:
            game_over = True
            font = pygame.font.SysFont(None, WINNER_FONT_SIZE)
            text = font.render("Congratulations!", True, BLUE)
            window.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

        if number_of_lives <= 0:
            game_over = True
            font = pygame.font.SysFont(None, WINNER_FONT_SIZE)
            game_over_text = font.render("Game Over", True, RED)
            window.blit(game_over_text, (WINDOW_SIZE[0] // 2 - game_over_text.get_width() // 2, WINDOW_SIZE[1] // 2 - game_over_text.get_height() // 2))

        # Displaying the text for lives, current time, and memo time
        font = pygame.font.SysFont(None, FONT_SIZE)
        lives_text = font.render(f"Lives: {number_of_lives}", True, RED)
        current_time_text = font.render(f"{elapsed_time // 1000 // 60:02d}:{elapsed_time // 1000 % 60:02d}", True, BLUE)
        memo_time_text = font.render(f"Memo time: {memo_time}", True, ORANGE) if show_walls else None

        window.blit(lives_text, (TEXT_MARGIN, TEXT_MARGIN))
        window.blit(current_time_text, (WINDOW_SIZE[0] // 2 - current_time_text.get_width() // 2, TEXT_MARGIN))
        if memo_time_text:
            window.blit(memo_time_text, (WINDOW_SIZE[0] - memo_time_text.get_width() - TEXT_MARGIN, TEXT_MARGIN))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
