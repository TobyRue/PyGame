import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1470, 810
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load("images\dungeon_start_screen.png")
background_top = screen.get_height() - background.get_height()
background_left = screen.get_width()/2 - background.get_width()/2


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("arial", 40)

# Game states: 'start', 'lvl_one', 'lvl_two', 'game_over'
game_state = "start"
game_next_menu = ""

# Dummy player
player_rect = pygame.Rect(400, 500, 50, 50)
player_color = (0, 200, 255)
player_speed = 5

# Dummy game over condition
frames_played = 0
MAX_FRAMES = 600  # After 10 seconds (60 FPS), end game














# Constants
TILE_SIZE = 60
MAP_WIDTH = WIDTH // TILE_SIZE
MAP_HEIGHT = HEIGHT // TILE_SIZE

# Colors
COLOR_WALL = (40, 40, 40)
COLOR_PATH = (200, 200, 200)
COLOR_PLAYER = (255, 0, 0)
COLOR_GOAL = (0, 255, 0)

# Player start
player_pos = [1, 1]  # Start at top-left corner
goal_pos = [MAP_WIDTH - 2, MAP_HEIGHT - 2]  # Goal near bottom-right

    

def create_maze(width, height):
    # Initialize maze with walls
    maze = [['wall' for _ in range(width)] for _ in range(height)]

    def neighbors(x, y):
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        result = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height:
                result.append((nx, ny))
        return result

    def connect_cells(cx, cy, nx, ny):
        mx, my = (cx + nx) // 2, (cy + ny) // 2
        maze[cy][cx] = 'path'
        maze[my][mx] = 'path'
        maze[ny][nx] = 'path'

    # Start maze from (1, 1)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 'path'
    walls = [(start_x, start_y)]

    while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))
        possible = [n for n in neighbors(x, y) if maze[n[1]][n[0]] == 'wall']
        if possible:
            nx, ny = random.choice(possible)
            connect_cells(x, y, nx, ny)
            walls.append((nx, ny))
            walls.append((x, y))

    # Make sure the goal position is a path
    maze[goal_pos[1]][goal_pos[0]] = 'path'
    return maze


# Initialize pygame

# Generate maze
                                  











PUZZLE_ROWS = 1
PUZZLE_COLS = 4
PLATE_SIZE = 100

puzzle_player_rect = pygame.Rect(100, 100, 50, 50)
puzzle_player_speed = 5

# Randomly generated each time
plate_connections = {}
light_states = {}

def generate_puzzle():
    global plate_connections, light_states
    plate_connections = {}
    light_states = {}

    # Set all lights to False initially
    for row in range(PUZZLE_ROWS):
        for col in range(PUZZLE_COLS):
            light_states[(row, col)] = False

    # Randomly generate connections for each plate
    for row in range(PUZZLE_ROWS):
        for col in range(PUZZLE_COLS):
            connected = []
            for _ in range(random.randint(1, PUZZLE_COLS)):  # Connect to 1 to all lights
                cr, cc = random.randint(0, PUZZLE_ROWS-1), random.randint(0, PUZZLE_COLS-1)
                if (cr, cc) not in connected:
                    connected.append((cr, cc))
            plate_connections[(row, col)] = connected

    # Randomly select a sequence of presses to toggle
    presses_to_make_solution = []
    for _ in range(random.randint(3, 6)):  # number of presses to generate solution
        pr, pc = random.randint(0, PUZZLE_ROWS-1), random.randint(0, PUZZLE_COLS-1)
        presses_to_make_solution.append((pr, pc))

    # Apply those presses to light_states
    for pr, pc in presses_to_make_solution:
        for target in plate_connections[(pr, pc)]:
            light_states[target] = not light_states[target]














def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont("arial", size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_state == "lvl_two":
                for row in range(PUZZLE_ROWS):
                    for col in range(PUZZLE_COLS):
                        plate_rect = pygame.Rect(300 + col * PLATE_SIZE, 100 + row * PLATE_SIZE, PLATE_SIZE - 10, PLATE_SIZE - 10)
                        if puzzle_player_rect.colliderect(plate_rect):
                            # Toggle lights when stepping onto a plate
                                for target in plate_connections[(row, col)]:
                                    light_states[target] = not light_states[target]    
    if game_state == "menu":
        screen.blit(background, (background_left, background_top))
        draw_text("Level Completed", 60, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press N to go to Next Level", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        if keys[pygame.K_n]:
            game_state = game_next_menu

    elif game_state == "start":
        screen.blit(background, (background_left, background_top))
        draw_text("MY GAME TITLE", 60, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Start", 30, WHITE, WIDTH // 2, HEIGHT // 2)

        if keys[pygame.K_SPACE]:
            tilemap = create_maze(MAP_WIDTH, MAP_HEIGHT)
            game_state = "lvl_one"
            frames_played = 0

    elif game_state == "lvl_one":
        # Handle movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1    
        elif keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_d]:
            dx = 1

        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy

        # Check bounds and collision
        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            if tilemap[new_y][new_x] != 'wall':
                player_pos = [new_x, new_y]

        # Check goal
        if player_pos == goal_pos:
            print("🎉 You reached the goal!")
            player_pos = [1, 1]
            game_next_menu = "lvl_two"
            game_state = "menu"
            generate_puzzle()
            puzzle_player_rect.x, puzzle_player_rect.y = 100, 100

        # Draw map
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                rect2 = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tilemap[y][x] == 'wall':
                    maze_wall = pygame.image.load("images/dungeon_brick_maze.png")
                    maze_wall = pygame.transform.scale(maze_wall, (TILE_SIZE, TILE_SIZE))
                    screen.blit(maze_wall, rect2)
                    # color = COLOR_WALL
                else:
                    maze_path = pygame.image.load("images/dungeon_maze_path.png")
                    maze_path = pygame.transform.scale(maze_path, (TILE_SIZE, TILE_SIZE))
                    screen.blit(maze_path, rect2)

        # Draw goal
        goal_rect = pygame.Rect(goal_pos[0] * TILE_SIZE, goal_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_GOAL, goal_rect)

        # Draw player
        # player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        # pygame.draw.rect(screen, COLOR_PLAYER, player_rect)
        player_maze = pygame.image.load("images/player.png")
        player_maze = pygame.transform.scale(player_maze, (TILE_SIZE, TILE_SIZE))
        rect = player_maze.get_rect()
        rect = rect.move((player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
        screen.blit(player_maze, rect)


        # Update display
        pygame.display.flip()
    elif game_state == "lvl_two":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            puzzle_player_rect.x -= puzzle_player_speed
        if keys[pygame.K_RIGHT]:
            puzzle_player_rect.x += puzzle_player_speed
        if keys[pygame.K_UP]:
            puzzle_player_rect.y -= puzzle_player_speed
        if keys[pygame.K_DOWN]:
            puzzle_player_rect.y += puzzle_player_speed

        # Draw puzzle background
        screen.fill((30, 30, 30))

        # Draw lights
        for row in range(PUZZLE_ROWS):
            for col in range(PUZZLE_COLS):
                color = (0, 255, 0) if light_states[(row, col)] else (80, 80, 80)
                rect = pygame.Rect(300 + col * PLATE_SIZE, 100 + row * PLATE_SIZE, PLATE_SIZE - 10, PLATE_SIZE - 10)
                pygame.draw.rect(screen, color, rect)

        # Draw pressure plates (outline)
        for row in range(PUZZLE_ROWS):
            for col in range(PUZZLE_COLS):
                rect = pygame.Rect(300 + col * PLATE_SIZE, 100 + row * PLATE_SIZE, PLATE_SIZE - 10, PLATE_SIZE - 10)
                pygame.draw.rect(screen, (255, 255, 0), rect, 3)

        # Draw player
        pygame.draw.rect(screen, (0, 200, 255), puzzle_player_rect)


        if all(light_states.values()):
            draw_text("Puzzle Solved! Press N for next level.", 40, WHITE, WIDTH // 2, 50)
            game_state = "game_over"

    elif game_state == "game_over":
        screen.blit(background, (background_left, background_top))
        draw_text("GAME OVER", 60, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press R to Restart", 30, WHITE, WIDTH // 2, HEIGHT // 2)

        if keys[pygame.K_r]:
            game_state = "start"
            player_rect.x = 400  # Reset player position

    pygame.display.flip()

pygame.quit()
sys.exit()