import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("arial", 40)

# Game states: 'start', 'playing', 'game_over'
game_state = "start"

# Dummy player
player_rect = pygame.Rect(400, 500, 50, 50)
player_color = (0, 200, 255)
player_speed = 5

# Dummy game over condition
frames_played = 0
MAX_FRAMES = 600  # After 10 seconds (60 FPS), end game

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "start":
        draw_text("MY GAME TITLE", 60, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Start", 30, WHITE, WIDTH // 2, HEIGHT // 2)

        if keys[pygame.K_SPACE]:
            game_state = "playing"
            frames_played = 0

    elif game_state == "playing":
        # Move player with arrow keys
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Draw player
        pygame.draw.rect(screen, player_color, player_rect)

        frames_played += 1
        if frames_played > MAX_FRAMES:
            game_state = "game_over"

    elif game_state == "game_over":
        draw_text("GAME OVER", 60, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text("Press R to Restart", 30, WHITE, WIDTH // 2, HEIGHT // 2)

        if keys[pygame.K_r]:
            game_state = "start"
            player_rect.x = 400  # Reset player position

    pygame.display.flip()

pygame.quit()
sys.exit()