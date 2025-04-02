import sys
import pygame
from pygame.locals import *
import Constants as con
from Grid import Grid
import random

pygame.init()

fpsClock = pygame.time.Clock()

con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
pygame.display.set_caption(con.TITLE)

def main () :
    looping = True
    
    con.SCREEN.fill(con.BACKGROUNDCOLOR)
    
    grid = Grid()
    grid.Draw()

    while looping :
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
    
        grid.Cells[random.randint(0,len(grid.Cells))].SetState(True)
        
        pygame.display.update()
        fpsClock.tick(con.FPS)

main()