import sys
import pygame
import random
import Constants as con
from pygame.locals import *
from pygame.math import *
from SandboxLevel import SandBoxLVL
from Handler import Handler

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT), FULLSCREEN)

con.HANDLER = Handler()

def main () :
    looping = True
    while looping:
        for event in pygame.event.get() :      
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        SandBox = SandBoxLVL()
                    if event.key == pygame.K_q:
                        con.HANDLER.QuitGame()
            if event.type == QUIT:
                con.HANDLER.QuitGame()
        
        con.SCREEN.fill((10,60,20))
        
        pygame.display.update()
        
        clock.tick(60)

main()