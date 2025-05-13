import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, size:Vector2, pos:Vector2):
        self.size = size
        self.pos = pos
        
        self.color = (40,40,40)
        
        self.rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
    
    def Draw(self):
        pygame.draw.rect(con.SCREEN,
                self.color,
                self.rect)