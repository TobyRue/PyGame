import pygame
import sys
from maze import *

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game")

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_ON = (0, 255, 0)
LIGHT_OFF = (100, 100, 100)
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER = (255, 50, 50)
PLAYER_COLOR = (0, 0, 255)
WALL_COLOR = (50, 50, 50)

# Clock
clock = pygame.time.Clock()

FONT = pygame.font.SysFont(None, 36)

# Global Game State
current_level = 1

# Player for maze
player_rect = pygame.Rect(50, 50, 30, 30)
player_speed = 4

# Simple Maze Walls
walls = [
    pygame.Rect(0, 0, 800, 20), pygame.Rect(0, 0, 20, 600),
    pygame.Rect(780, 0, 20, 600), pygame.Rect(0, 580, 800, 20),
    pygame.Rect(200, 100, 400, 20), pygame.Rect(200, 100, 20, 400),
    pygame.Rect(580, 100, 20, 400), pygame.Rect(200, 480, 400, 20)
]

exit_rect = pygame.Rect(730, 530, 40, 40)

# Puzzle Level Variables
lights = [False, False, False, False]
buttons = [
    pygame.Rect(100, 100, 60, 60),
    pygame.Rect(100, 200, 60, 60),
    pygame.Rect(100, 300, 60, 60),
    pygame.Rect(100, 400, 60, 60)
]

# Which lights each button affects
button_connections = [
    [0, 1],
    [1, 2],
    [2, 3],
    [0, 3]
]

def draw_text(text, pos, color=WHITE):
    render = FONT.render(text, True, color)
    SCREEN.blit(render, pos)

def puzzle_level():
    global lights, current_level

    SCREEN.fill(BLACK)

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    for i, button in enumerate(buttons):
        color = BUTTON_COLOR
        if button.collidepoint(mouse_pos):
            color = BUTTON_HOVER
        pygame.draw.rect(SCREEN, color, button)
        draw_text(f"{i+1}", (button.x + 20, button.y + 15))

    # Draw lights
    for i in range(4):
        light_color = LIGHT_ON if lights[i] else LIGHT_OFF
        pygame.draw.circle(SCREEN, light_color, (300, 150 + i*100), 30)

    # Check if all lights are on to progress
    if all(lights):
        draw_text("Puzzle Solved! Press N for next level.", (400, 50))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            current_level = 2
            reset_maze()

def reset_maze():
    global player_rect
    player_rect.x, player_rect.y = 50, 50

def maze_level():
    global current_level

    SCREEN.fill(BLACK)
    keys = pygame.key.get_pressed()

    move_x = move_y = 0
    if keys[pygame.K_LEFT]:
        move_x = -player_speed
    if keys[pygame.K_RIGHT]:
        move_x = player_speed
    if keys[pygame.K_UP]:
        move_y = -player_speed
    if keys[pygame.K_DOWN]:
        move_y = player_speed

    # Move and collide with walls
    player_rect.x += move_x
    for wall in walls:
        if player_rect.colliderect(wall):
            if move_x > 0:
                player_rect.right = wall.left
            if move_x < 0:
                player_rect.left = wall.right
    player_rect.y += move_y
    for wall in walls:
        if player_rect.colliderect(wall):
            if move_y > 0:
                player_rect.bottom = wall.top
            if move_y < 0:
                player_rect.top = wall.bottom

    # Draw walls
    for wall in walls:
        pygame.draw.rect(SCREEN, WALL_COLOR, wall)

    # Draw player
    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)

    # Draw exit
    pygame.draw.rect(SCREEN, (0, 200, 0), exit_rect)
    draw_text("Reach the green square!", (20, 20))

    # Check for win
    if player_rect.colliderect(exit_rect):
        draw_text("You Escaped! Press Q to quit.", (250, 250))
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def handle_events():
    global lights
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and current_level == 1:
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    # Toggle connected lights
                    for light_index in button_connections[i]:
                        lights[light_index] = not lights[light_index]

def main():
    while True:
        handle_events()

        if current_level == 1:
            puzzle_level()
        elif current_level == 2:
            maze_level()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()