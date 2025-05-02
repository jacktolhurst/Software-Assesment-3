import sys
import pygame
import random
import Constants as con
from pygame.locals import *
from pygame.math import *
from Grid import Grid

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT), FULLSCREEN)

def main () :
    
    grid = Grid(Vector2(20,20))

    updateGrid = False
    
    looping = True
    while looping:
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    grid.SetCell(Vector2(random.randrange(len(grid.cells)-1),random.randrange(len(grid.cells[0])-1)), True)
                if event.key == pygame.K_p:
                    updateGrid = not updateGrid
                if event.key == pygame.K_q:
                    QuitGame()
            if event.type == QUIT:
                QuitGame()
        

        if updateGrid:
            grid.Update()
        
        grid.DrawCells()
        
        pygame.display.update()
        clock.tick(con.TICKSPEED)

def QuitGame():
    pygame.quit()
    sys.exit()

main()