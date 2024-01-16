import pygame
import random
import sys

# Constants
WINDOW_SIZE = (800, 800)
GRID_SIZE = 10
TILE_SIZE = WINDOW_SIZE[0] // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

def draw_labyrinth(window, labyrinth, show_walls=True):
    for y, row in enumerate(labyrinth):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 'wall' and show_walls:
                pygame.draw.rect(window, BLACK, rect)
            else:
                pygame.draw.rect(window, WHITE, rect)
            pygame.draw.rect(window, GRAY, rect, 1)  # Grid lines

def handle_player_movement(player_position, direction, labyrinth):
    x, y = player_position
    if direction == 'up' and y > 0 and labyrinth[y - 1][x] != 'wall':
        y -= 1
    elif direction == 'down' and y < GRID_SIZE - 1 and labyrinth[y + 1][x] != 'wall':
        y += 1
    elif direction == 'left' and x > 0 and labyrinth[y][x - 1] != 'wall':
        x -= 1
    elif direction == 'right' and x < GRID_SIZE - 1 and labyrinth[y][x + 1] != 'wall':
        x += 1
    return x, y

def main():
    labyrinth = generate_labyrinth(GRID_SIZE)
    player_position = (0, 0)
    start_position = (0, 0)  # Starting point
    finish_position = (GRID_SIZE - 1, GRID_SIZE - 1)  # Finish point
    show_walls = True
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    player_position = handle_player_movement(player_position, 'up', labyrinth)
                elif event.key == pygame.K_DOWN:
                    player_position = handle_player_movement(player_position, 'down', labyrinth)
                elif event.key == pygame.K_LEFT:
                    player_position = handle_player_movement(player_position, 'left', labyrinth)
                elif event.key == pygame.K_RIGHT:
                    player_position = handle_player_movement(player_position, 'right', labyrinth)
                elif event.key == pygame.K_SPACE:
                    show_walls = not show_walls

        window.fill(GRAY)
        draw_labyrinth(window, labyrinth, show_walls)

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
            font = pygame.font.SysFont(None, 55)
            text = font.render("Congratulations!", True, BLUE)
            window.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
