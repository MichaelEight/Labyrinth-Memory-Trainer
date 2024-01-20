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
    def __init__(self, window_size):
        self.window_size = window_size
        self.window = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.grid_size = 10  # Default grid size
        self.memory_time_limit = 5000  # Default memory time limit
        self.game_over = False
        self.in_menu = True
        self.final_elapsed_time = None  # New attribute to store final elapsed time
        self.initialize_buttons()
        self.reset_game()

    def initialize_buttons(self):
        button_width = 200
        button_height = 50
        horizontal_center = self.window_size[0] // 2 - button_width // 2
        vertical_start = 250  # Starting position for the buttons (vertically)
        vertical_spacing = 100  # Space between each button

        self.buttons = {
            "Easy": pygame.Rect(horizontal_center, vertical_start, button_width, button_height),
            "Medium": pygame.Rect(horizontal_center, vertical_start + vertical_spacing, button_width, button_height),
            "Hard": pygame.Rect(horizontal_center, vertical_start + vertical_spacing * 2, button_width, button_height)
        }

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse click
                    for difficulty, button in self.buttons.items():
                        if button.collidepoint(event.pos):
                            grid_size = {"Easy": 5, "Medium": 7, "Hard": 10}[difficulty]
                            self.memory_time_limit = 5000
                            self.grid_size = grid_size
                            self.reset_game()
                            self.in_menu = False

        for difficulty, button in self.buttons.items():
            if button.collidepoint(event.pos):
                self.grid_size = {"Easy": 5, "Medium": 7, "Hard": 10}[difficulty]
                self.memory_time_limit = 5000
                self.reset_game()  # Call reset_game here after setting grid_size
                self.in_menu = False
                return

    def reset_game(self):
        # Calculate tile size based on grid size
        self.tile_size = min(self.window_size[0] // self.grid_size, self.window_size[1] // self.grid_size)
        
        # Calculate offset to center the labyrinth
        self.labyrinth_offset_x = (self.window_size[0] - self.tile_size * self.grid_size) // 2
        self.labyrinth_offset_y = (self.window_size[1] - self.tile_size * self.grid_size) // 2

        self.labyrinth = self.generate_labyrinth(self.grid_size)
        self.player_position = (0, 0)
        self.start_position = (0, 0)
        self.finish_position = (self.grid_size - 1, self.grid_size - 1)
        self.show_walls = True
        self.revealed_walls = set()
        self.number_of_lives = 3
        self.game_over = False
        self.start_time = pygame.time.get_ticks()

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
                rect = pygame.Rect(
                    self.labyrinth_offset_x + x * self.tile_size,
                    self.labyrinth_offset_y + y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
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
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                for difficulty, button in self.buttons.items():
                    if button.collidepoint(event.pos):
                        self.grid_size = {"Easy": 5, "Medium": 7, "Hard": 10}[difficulty]
                        self.memory_time_limit = 5000
                        self.reset_game()
                        self.in_menu = False
                        return  # Exit the loop once a button is clicked

    def draw_menu(self):
        self.window.fill(GRAY)
        font = pygame.font.SysFont(None, FONT_SIZE)

        # Draw the "Main Menu" title
        title_text = font.render("Main Menu", True, WHITE)
        title_rect = title_text.get_rect(center=(self.window_size[0] // 2, 200))
        self.window.blit(title_text, title_rect)

        # Draw buttons
        for difficulty, button in self.buttons.items():
            pygame.draw.rect(self.window, WHITE, button)  # Draw the button
            text = font.render(difficulty, True, BLACK)
            text_rect = text.get_rect(center=button.center)
            self.window.blit(text, text_rect)

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

            if self.player_position == self.finish_position or self.number_of_lives <= 0:
                self.game_over = True
                self.final_elapsed_time = elapsed_time  # Store the final elapsed time

    def draw_game(self):
        self.window.fill(GRAY)
        self.draw_labyrinth(self.window, self.labyrinth, self.show_walls, self.revealed_walls)

        # Calculate positions with offset for start, finish, and player
        start_rect = pygame.Rect(
            self.labyrinth_offset_x + self.start_position[0] * self.tile_size,
            self.labyrinth_offset_y + self.start_position[1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        finish_rect = pygame.Rect(
            self.labyrinth_offset_x + self.finish_position[0] * self.tile_size,
            self.labyrinth_offset_y + self.finish_position[1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )
        player_rect = pygame.Rect(
            self.labyrinth_offset_x + self.player_position[0] * self.tile_size,
            self.labyrinth_offset_y + self.player_position[1] * self.tile_size,
            self.tile_size,
            self.tile_size
        )

        pygame.draw.rect(self.window, DARK_GREEN, start_rect)
        pygame.draw.rect(self.window, RED, finish_rect)
        pygame.draw.rect(self.window, GREEN, player_rect)

        # Draw the text for lives, current time, and memo time
        font = pygame.font.SysFont(None, FONT_SIZE)
        lives_text = font.render(f"Lives: {self.number_of_lives}", True, RED)
        # Use final_elapsed_time if the game is over, else calculate current elapsed time
        current_time = self.final_elapsed_time if self.game_over else pygame.time.get_ticks() - self.start_time
        current_time_text = font.render(f"{current_time // 1000 // 60:02d}:{current_time // 1000 % 60:02d}", True, BLUE)
        self.window.blit(current_time_text, (WINDOW_SIZE[0] // 2 - current_time_text.get_width() // 2, TEXT_MARGIN))

        memo_time_text = font.render(f"Memo time: {self.memo_time}", True, ORANGE) if self.show_walls else None
        self.window.blit(lives_text, (TEXT_MARGIN, TEXT_MARGIN))

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
    game = Game(WINDOW_SIZE)
    game.run()