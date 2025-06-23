import math
import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, type, relativePos:Vector2, size:Vector2, color:tuple, state:bool=True, width:int=0):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        
        self.type = type
        
        self.relativePos =  Vector2(min(relativePos.x,100)/100,min(relativePos.y,100)/100)
        self.size = size
        self.color = color
        
        self.state = state
        
        self.width = width

        self.rect = None
        self.vertices = None

        self.ResetRect()
    
    def MoveSet(self, newPos:Vector2):
        self.relativePos = newPos
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.relativePos = self.relativePos + addedPos
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def ResetRect(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        abs_x = self.relativePos.x * self.screenWidth
        abs_y = self.relativePos.y * self.screenHeight
    
        self.rect = pygame.Rect(abs_x, abs_y, self.size.x, self.size.y)
        self.vertices = self.type.GetVertices(self.rect)
    
    def Draw(self):
        if self.screenWidth is not pygame.display.get_surface().get_size()[0] and self.screenHeight is not pygame.display.get_surface().get_size()[1]:
            self.ResetRect()
            
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