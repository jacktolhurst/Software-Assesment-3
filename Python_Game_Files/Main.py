import sys
import pygame
import time
from pygame.locals import *
import Constants as con
from Grid import Grid
from Camera import Camera

pygame.init()

fpsClock = pygame.time.Clock()

con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))
pygame.display.set_caption(con.TITLE)

con.CAM = Camera()

def main () :
    looping = True
    
    con.SCREEN.fill(con.BACKGROUNDCOLOR)
    
    grid = Grid()
    grid.CreateCells()
    
    while looping :
        events = pygame.event.get()        
        for event in events :
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:   
                    grid.SetSpecific({(3,3):2,(4,4):2,(5,4):2,(5,3):2,(5,2):2})
            if event.type == QUIT :
                pygame.quit()
                sys.exit()

        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        con.CAM.update(events)
        grid.update()

        pygame.display.flip()
        fpsClock.tick(con.FPS)
        
        time.sleep(2)

main()