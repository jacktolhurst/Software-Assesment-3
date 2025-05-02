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
                if event.key == pygame.K_w:
                    con.TICKSPEED = con.TICKSPEED + 5
                if event.key == pygame.K_s:
                    con.TICKSPEED = max(1, con.TICKSPEED - 5)
                if event.key == pygame.K_q:
                    QuitGame()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not isPlaying:
                        mousePos = pygame.mouse.get_pos()
                        grid.ClickIntersection(mousePos)
            if event.type == QUIT:
                QuitGame()
        
        
        
        print(con.TICKSPEED)
        if isPlaying:
            grid.Update()
        
        grid.DrawCells()
        
        pygame.display.update()
        if isPlaying:
            clock.tick(con.TICKSPEED)
        else:
            clock.tick(60)

def QuitGame():
    pygame.quit()
    sys.exit()

main()