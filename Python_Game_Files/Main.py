import pygame
import asyncio
import Constants as con
from pygame.locals import *
from pygame.math import *
from Handler import Handler
from MainMenu import MainMenu

pygame.init()

clock = pygame.time.Clock()

pygame.display.set_caption('Game Of Life')
# con.SCREEN = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT), FULLSCREEN)
con.SCREEN = pygame.display.set_mode((con.WINDOWWIDTH, con.WINDOWHEIGHT), pygame.RESIZABLE)
con.SCREENRECT = pygame.Rect(0,0,con.WINDOWWIDTH, con.WINDOWHEIGHT)

con.HANDLER = Handler()

async def main ():
    mainMenu = MainMenu()

asyncio.run(main())