import sys
import pygame
from pygame.locals import *
import Constants as con
from Grid import Grid

pygame.init()

fpsClock = pygame.time.Clock()

con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
pygame.display.set_caption(con.TITLE)

def main () :
    looping = True
    
    con.SCREEN.fill(con.BACKGROUNDCOLOR)
    
    grid = Grid()
    grid.CreateCells()

    while looping :
        for event in pygame.event.get() :
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:   
                    grid.SetAll(True)
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        
        grid.update()
        
        pygame.display.update()
        fpsClock.tick(con.FPS)

main()