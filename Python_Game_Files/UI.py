import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, type, pos:Vector2, size:Vector2, color:tuple, state:bool=True, width:int=0):
        self.pos = pos
        
        self.color = color
        
        self.state = state
        
        self.rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        self.vertices = type.GetVertices(self.rect)
        
        self.width = width
        
    def SetState(self, newState):
        self.state = newState
    
    def Draw(self):
        pygame.draw.polygon(con.SCREEN, self.color, self.vertices, self.width)

class Quad:
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [(rect.x, rect.y), (rect.x + rect.w, rect.y), (rect.x + rect.w, rect.y + rect.h), (rect.x, rect.y + rect.h)]

class Triangle:
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [(rect.x + rect.w/2, rect.y), (rect.x, rect.y + rect.h), (rect.x + rect.w, rect.y + rect.h)]

class Circle:
    borderRadius = 50