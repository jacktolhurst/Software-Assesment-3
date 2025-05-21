import math
import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, type, pos:Vector2, size:Vector2, color:tuple, state:bool=True, width:int=0):
        self.pos = pos
        self.size = size
        
        self.type = type
        
        self.color = color
        
        self.state = state
        
        self.width = width
        
        self.rect = None
        self.vertices = None
        
        self.ResetRect()
    
    def MoveSet(self, newPos:Vector2):
        self.pos = newPos
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.pos = self.pos + addedPos
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def ResetRect(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.vertices = self.type.GetVertices(self.rect)
    
    def Draw(self):
        pygame.draw.polygon(con.SCREEN, self.color, self.vertices, self.width)

class Quad:
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [
            (rect.x, rect.y),
            (rect.x + rect.w, rect.y),
            (rect.x + rect.w, rect.y + rect.h),
            (rect.x, rect.y + rect.h)
            ]

class TriangleUp:
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [
            (rect.x + rect.w/2, rect.y),
            (rect.x, rect.y + rect.h),
            (rect.x + rect.w, rect.y + rect.h)
            ]

class TriangleDown:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x, rect.y),                     
            (rect.x + rect.w, rect.y),            
            (rect.x + rect.w / 2, rect.y + rect.h)
            ]

class TriangleLeft:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x + rect.w, rect.y),          
            (rect.x + rect.w, rect.y + rect.h),    
            (rect.x, rect.y + rect.h / 2)         
            ]

class TriangleRight:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x, rect.y),                   
            (rect.x, rect.y + rect.h),             
            (rect.x + rect.w, rect.y + rect.h / 2)  
            ]

class Pentagon:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        cx = rect.x + rect.w / 2
        cy = rect.y + rect.h / 2
        radius = min(rect.w, rect.h) / 2

        return [
            (
                cx + radius * math.cos(2 * math.pi * i / 5),
                cy + radius * math.sin(2 * math.pi * i / 5)
            )
            for i in range(5)
            ]

class Hexagon:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        cx = rect.x + rect.w / 2
        cy = rect.y + rect.h / 2
        radius = min(rect.w, rect.h) / 2

        return [
            (
                cx + radius * math.cos(2 * math.pi * i / 6),
                cy + radius * math.sin(2 * math.pi * i / 6)
            )
            for i in range(6)
            ]

class Octagon:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        cx = rect.x + rect.w / 2
        cy = rect.y + rect.h / 2
        radius = min(rect.w, rect.h) / 2

        return [
            (
                cx + radius * math.cos(2 * math.pi * i / 8),
                cy + radius * math.sin(2 * math.pi * i / 8)
            )
            for i in range(8)
            ]

class Circle:
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        cx = rect.x + rect.w / 2
        cy = rect.y + rect.h / 2
        radius = min(rect.w, rect.h) / 2

        return [
            (
                cx + radius * math.cos(2 * math.pi * i / 32),
                cy + radius * math.sin(2 * math.pi * i / 32)
            )
            for i in range(32)
            ]