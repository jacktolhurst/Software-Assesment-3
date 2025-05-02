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
    
    grid = Grid(con.CELLAMOUNT)

    isPlaying = False
    
    looping = True
    while looping:
        if isPlaying:
            con.SCREEN.fill(con.BACKGROUNDCOLORPLAY)
        else:
            con.SCREEN.fill(con.BACKGROUNDCOLORSTOPPED)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_k]:
            grid.SetCell(Vector2(random.randrange(len(grid.cells)-1),random.randrange(len(grid.cells[0])-1)), True)
        
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    isPlaying = not isPlaying
                if event.key == pygame.K_q:
                    QuitGame()
            if event.type == QUIT:
                QuitGame()
        

        if isPlaying:
            grid.Update()
        
        grid.DrawCells()
        
        pygame.display.update()
        clock.tick(con.TICKSPEED)

def QuitGame():
    pygame.quit()
    sys.exit()

main()