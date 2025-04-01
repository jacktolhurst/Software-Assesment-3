import sys
import pygame
from pygame.locals import *

pygame.init()

BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

def main () :
    looping = True

    while looping :
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
    
    WINDOW.fill(BACKGROUND)
    pygame.display.update()
    fpsClock.tick(FPS)

main()