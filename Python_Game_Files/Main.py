import sys
import pygame
import Constants as con
from pygame.locals import *
from pygame.math import *
from Grid import Grid

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT), FULLSCREEN)

def main () :
    looping = True
    
    grid = Grid(Vector2(20,20))
    
    while looping :
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    grid.SetCell(Vector2(10,10), True)
                    neighbours = grid.GetNeighbours(Vector2(10,11))
                    for cell in neighbours:
                        print(cell.state)
            if event.type == QUIT :
                pygame.quit()
                sys.exit()
                looping = False
        

        
        grid.UpdateCells()
        grid.DrawCells()
        
        pygame.display.update()
        clock.tick(con.TICKSPEED)

main()