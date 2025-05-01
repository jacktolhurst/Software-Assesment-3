import pygame
import Constants as con
from pygame.math import *

class Cell():
    def __init__(self, pos: Vector2, state=False):
        self.pos = pos
        self.state = state
        self.color = (0,0,0)
        
        if state:
            self.color = (255,255,255)
        
        self.rect = pygame.Rect(pos.x, pos.y, con.CELLSIZE.x, con.CELLSIZE.y)

    def Draw(self):
        pygame.draw.rect(con.SCREEN,
                        self.color,
                        self.rect)