import math
import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    @staticmethod
    def RealPosToPercent(realPos:Vector2):
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        screenRatio = screenWidth/screenHeight
        
        relativeX = (realPos.x / screenWidth) * 100 * screenRatio
        relativeY = (realPos.y / screenHeight) * 100
        
        return Vector2(relativeX, relativeY)
    
    def __init__(self, type, relativePos:Vector2, relativeSize:Vector2, color:tuple, state:bool=True, width:int=0):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.type = type
        
        self.originalRelativePos = relativePos
        self.originalRelativeSize = relativeSize
        
        self.color = color
        
        self.state = state
        
        self.width = width

        self.rect = None
        self.vertices = None

        self.ResetRect()
    
    def MoveSet(self, newPos:Vector2):
        self.originalRelativePos = newPos
        
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos + addedPos
        
        self.ResetRect()
    
    def SizeSet(self, newSize:Vector2):
        self.originalRelativeSize = newSize
        
        self.ResetRect()
    
    def SizeAdd(self, addedSize:Vector2):
        self.originalRelativeSize = self.originalRelativeSize + addedSize
        
        self.ResetRect()
    
    def ChangeColor(self, newColor:tuple):
        self.color = newColor
        
        self.ResetRect()
    
    def ChangeShape(self, newType):
        self.type = newType
        
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def CheckCollidePoint(self, point) -> bool:
        return self.rect.collidepoint(point)
    
    def GetPosPercent(self) -> Vector2:
        return self.originalRelativePos
    
    def GetSizePercent(self) -> Vector2:
        return self.originalRelativeSize
    
    def GetRect(self) -> pygame.Rect:
        return self.rect

    def ResetRect(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
    
        fx = self.originalRelativePos.x  / 100.0
        fy = self.originalRelativePos.y  / 100.0
        sx = self.originalRelativeSize.x / 100.0
        sy = self.originalRelativeSize.y / 100.0

        base = min(self.screenWidth, self.screenHeight)

        absX = fx * base
        absY = fy * base
        absW = sx * base
        absH = sy * base

        self.rect = pygame.Rect(absX, absY, absW, absH)
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