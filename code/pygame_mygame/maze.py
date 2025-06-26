import pygame
import random

# Constants
WIDTH, HEIGHT = 3200, 1000
TILE_SIZE = 5
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

def generate(width, height): 
    create_maze(width, height)

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
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Generate maze
tilemap = create_maze(MAP_WIDTH, MAP_HEIGHT)

# Game loop
running = True
while running:
    clock.tick(15)  # FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        running = False

    # Draw map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tilemap[y][x] == 'wall':
                color = COLOR_WALL
            else:
                color = COLOR_PATH
            pygame.draw.rect(screen, color, rect)

    # Draw goal
    goal_rect = pygame.Rect(goal_pos[0] * TILE_SIZE, goal_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLOR_GOAL, goal_rect)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLOR_PLAYER, player_rect)

    # Update display
    pygame.display.flip()

pygame.quit()                                          