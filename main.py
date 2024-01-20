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

class Game:
    def __init__(self, grid_size, memory_time_limit):
        self.grid_size = grid_size
        self.memory_time_limit = memory_time_limit
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.labyrinth = self.generate_labyrinth(self.grid_size)
        self.player_position = (0, 0)
        self.start_position = (0, 0)
        self.finish_position = (self.grid_size - 1, self.grid_size - 1)
        self.show_walls = True
        self.revealed_walls = set()
        self.number_of_lives = 3
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.in_menu = True

    def generate_labyrinth(self, n):
        grid = [['path' for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if random.choice([True, False]):
                    grid[i][j] = 'wall'
        for i in range(n):
            grid[i][0] = 'path'
            grid[n-1][i] = 'path'
        return grid

    def draw_labyrinth(self, window, labyrinth, show_walls, revealed_walls):
        for y, row in enumerate(labyrinth):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 'wall':
                    if show_walls:
                        pygame.draw.rect(window, BLACK, rect)
                    elif (x, y) in revealed_walls:
                        pygame.draw.rect(window, GRAY, rect)
                    else:
                        pygame.draw.rect(window, WHITE, rect)
                else:
                    pygame.draw.rect(window, WHITE, rect)
                pygame.draw.rect(window, GRAY, rect, 1)

    def handle_player_movement(self, player_position, direction):
        x, y = player_position
        move = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        dx, dy = move[direction]
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            if self.labyrinth[new_y][new_x] == 'wall':
                self.revealed_walls.add((new_x, new_y))  # Add to revealed walls
                self.number_of_lives -= 1
            else:
                return new_x, new_y
        return x, y

    def run(self):
        running = True
        while running:
            if self.in_menu:
                self.handle_menu_events()
                self.draw_menu()
            else:
                self.handle_game_events()
                self.update_game()
                self.draw_game()

            pygame.display.flip()
            self.clock.tick(60)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.in_menu = False  # Start the game

    def draw_menu(self):
        self.window.fill(GRAY)
        font = pygame.font.SysFont(None, FONT_SIZE)
        text = font.render("Press SPACE to play", True, WHITE)
        self.window.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over and event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.in_menu = True
                elif not self.game_over:
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
                        if self.show_walls:
                            self.show_walls = False
                        self.player_position = self.handle_player_movement(self.player_position, direction)

    def update_game(self):
        if not self.game_over:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            self.memo_time = max(self.memory_time_limit - elapsed_time, 0) // 1000

            if elapsed_time > self.memory_time_limit:
                self.show_walls = False

            if self.player_position == self.finish_position:
                self.game_over = True

            if self.number_of_lives <= 0:
                self.game_over = True

    def draw_game(self):
        self.window.fill(GRAY)
        self.draw_labyrinth(self.window, self.labyrinth, self.show_walls, self.revealed_walls)

        # Draw start and finish squares
        start_rect = pygame.Rect(self.start_position[0] * TILE_SIZE, self.start_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.window, DARK_GREEN, start_rect)
        finish_rect = pygame.Rect(self.finish_position[0] * TILE_SIZE, self.finish_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.window, RED, finish_rect)

        # Draw the player
        player_rect = pygame.Rect(self.player_position[0] * TILE_SIZE, self.player_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.window, GREEN, player_rect)

        # Draw the text for lives, current time, and memo time
        font = pygame.font.SysFont(None, FONT_SIZE)
        lives_text = font.render(f"Lives: {self.number_of_lives}", True, RED)
        elapsed_time = pygame.time.get_ticks() - self.start_time
        current_time_text = font.render(f"{elapsed_time // 1000 // 60:02d}:{elapsed_time // 1000 % 60:02d}", True, BLUE)
        memo_time_text = font.render(f"Memo time: {self.memo_time}", True, ORANGE) if self.show_walls else None

        self.window.blit(lives_text, (TEXT_MARGIN, TEXT_MARGIN))
        self.window.blit(current_time_text, (WINDOW_SIZE[0] // 2 - current_time_text.get_width() // 2, TEXT_MARGIN))
        if memo_time_text:
            self.window.blit(memo_time_text, (WINDOW_SIZE[0] - memo_time_text.get_width() - TEXT_MARGIN, TEXT_MARGIN))

        # Display game over or congratulations message
        if self.game_over:
            font = pygame.font.SysFont(None, WINNER_FONT_SIZE)
            if self.number_of_lives <= 0:
                text = font.render("Game Over", True, RED)
            else:
                text = font.render("Congratulations!", True, BLUE)
            self.window.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))

# Game Variables
number_of_lives = 3
memory_time_limit = 5000 # [ms]

# Set up the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Labyrinth Memory Trainer")

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Labyrinth Memory Trainer")
    game = Game(GRID_SIZE, 5000)
    game.run()