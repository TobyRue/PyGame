import os
from maze import *
import pygame
from pygame.locals import *

WINSIZE = (Cell.w * 41, Cell.h * 41)


def draw_maze(screen):
    maze = Maze(WINSIZE)
    maze.generate(screen, True)


def main():
    pygame.init()
    scr_inf = pygame.display.Info()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(scr_inf.current_w // 2 - WINSIZE[0] // 2,
                                                         scr_inf.current_h // 2 - WINSIZE[1] // 2)
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Maze')
    screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    draw_maze(screen)

    done = 0
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1

        pygame.display.update()
        clock.tick()


if __name__ == '__main__':
    main()