import pygame
import asyncio
import Constants as con
from pygame.locals import *
from pygame.math import *
from SandboxLevel import SandBoxLVL
from Settings import SettingsMenu
from Handler import Handler

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
con.SCREEN = pygame.display.set_mode((con.WINDOW_WIDTH, con.WINDOW_HEIGHT), FULLSCREEN)
con.SCREENRECT = pygame.Rect(0,0,con.WINDOW_WIDTH, con.WINDOW_HEIGHT)

con.HANDLER = Handler()

async def main () :
    looping = True
    while looping:
        for event in pygame.event.get() :      
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        sandBoxLVL = SandBoxLVL(Vector2(50,50))
                    if event.key == pygame.K_s:
                        settingsLVL = SettingsMenu()
                    if event.key == pygame.K_q:
                        con.HANDLER.QuitGame()
            if event.type == QUIT:
                con.HANDLER.QuitGame()
        
        sandBoxLVL = None
        settingsLVL = None
        
        con.SCREEN.fill((10,60,20))
        
        pygame.display.update()
        
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())