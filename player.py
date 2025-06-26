import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")# Game Loop

# Load player image
player_img = pygame.image.load("images/player.png")
player_width = player_img.get_width()
player_height = player_img.get_height()

player_x, player_y = 50, 500  # Initial position
player_y_change = 0
gravity = 0.5
jump = -15
jump_pressed = False  # Prevents holding jump
on_ground = False

def draw_player(x, y):
    win.blit(player_img, (x, y))

# Platform settup
platforms = [(300, 400), (500, 300), (700, 200), (25,550)]

def draw_platforms():
    for plat in platforms:
        pygame.draw.rect(win, (0, 0, 255), [plat[0], plat[1], 100, 10])

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and on_ground:
                player_y_change = jump
                on_ground = False
                jump_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                jump_pressed = False    
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= 6
    if keys[pygame.K_d]:
        player_x += 6
    
    player_y_change += gravity
    player_y += player_y_change

    # Simple platform collision (bottom of player touches top of platform)
    on_ground = False  # Reset before checking collisions
    for plat_x, plat_y in platforms:
        if (
            plat_x < player_x + player_width and
            player_x < plat_x + 100 and
            player_y + player_height <= plat_y + player_y_change and
            player_y + player_height + player_y_change >= plat_y
        ):
            player_y = plat_y - player_height
            player_y_change = 0
            on_ground = True

    # Reset if player falls off
    if player_y > HEIGHT:
        player_x, player_y = 50, 500
        player_y_change = 0

    win.fill((0, 0, 0))  # Clear screen

    #Draw everything on the screen
    draw_platforms() 
    draw_player(player_x, player_y)
    pygame.display.flip()

            
pygame.quit()