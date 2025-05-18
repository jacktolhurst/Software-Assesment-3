import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, type, pos:Vector2, size:Vector2, color:tuple, state:bool=True, width:int=0):
        self.pos = pos
        
        self.color = color
        
        self.state = state
        
        self.rect = type.rect
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.rect.w = size.x
        self.rect.h = size.y
        
        self.width = width
        
        self.borderRadius = type.borderRadius
    
    def SetState(self, newState):
        self.state = newState
    
    def Draw(self):
        pygame.draw.rect(con.SCREEN,
                self.color,
                self.rect,
                self.width,
                self.borderRadius)

class Quad:
    rect = pygame.Rect(0, 0, 0, 0)
    borderRadius = 0

class RoundedQuad:
    rect = pygame.Rect(0, 0, 0, 0)
    borderRadius = 20

class Circle:
    rect = pygame.Rect(0, 0, 0, 0)
    borderRadius = 50