import sys
import pygame
from pygame.locals import *
import numpy
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
    
    panning = False
    initialClickPos = None

    while looping :
        for event in pygame.event.get() :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    panning = True
                    initialClickPos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    panning = False
                    initialClickPos = None
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_l:   
                    grid.SetAll(True)
            
            if event.type == pygame.MOUSEWHEEL:
                if con.CURRENTSCROLL + event.y/5 > 0.5 and con.CURRENTSCROLL + event.y/5 < 400:
                    con.CURRENTSCROLL += event.y/5
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
        
        if panning:
            currentMousePos = pygame.mouse.get_pos()
            difference = numpy.subtract(currentMousePos, initialClickPos)
            con.SCREENPOS += difference
            initialClickPos = currentMousePos
        
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        grid.update()
        
        pygame.display.update()
        fpsClock.tick(con.FPS)

main()