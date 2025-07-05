import pygame
import asyncio
import Constants as con
from pygame.locals import *
from pygame.math import *
from SandboxLevel import SandBoxLVL
from Handler import Handler
from Settings import SettingsMenu
from MainMenu import MainMenu

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT), FULLSCREEN)
# con.SCREEN = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT), pygame.RESIZABLE)
con.SCREENRECT = pygame.Rect(0,0,con.WINDOWWIDTH, con.WINDOWHEIGHT)

con.HANDLER = Handler()

async def main ():
    looping = True
    while looping:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
        for event in pygame.event.get() :      
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        sandBoxLVL = MainMenu(Vector2(9,9))
                    if event.key == pygame.K_s:
                        mainMenu = MainMenu()
                    if event.key == pygame.K_q:
                        con.HANDLER.QuitGame()
            if event.type == QUIT:
                con.HANDLER.QuitGame()
        
        sandBoxLVL = None
        mainMenu = None
        
        con.SCREEN.fill((10,60,20))
        
        pygame.display.update()
        
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())