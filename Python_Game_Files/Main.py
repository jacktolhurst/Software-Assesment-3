import sys
import pygame
import Constants as con
from pygame.locals import *
from pygame.math import *
from Cell import Cell

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT))

def main () :
    looping = True
    
    cell = Cell(Vector2(10,10), True)

    while looping :
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        for event in pygame.event.get() :
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
                looping = False
        
        cell.Draw()
        
        pygame.display.update()
        clock.tick(con.TICKSPEED)

main()