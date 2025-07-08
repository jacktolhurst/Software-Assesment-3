import math
import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    @staticmethod
    def RealPosToPercent(realPos:Vector2) -> Vector2:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        screenRatio = screenWidth/screenHeight
        
        relativeX = (realPos.x / screenWidth) * 100 * screenRatio
        relativeY = (realPos.y / screenHeight) * 100
        
        return Vector2(relativeX, relativeY)
    
    @staticmethod
    def RealSizeToPercent(realSize:Vector2) -> Vector2:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        base = min(screenWidth, screenHeight)

        percentWidth = (realSize.x / base) * 100
        percentHeight = (realSize.y / base) * 100

        return Vector2(percentWidth, percentHeight)
    
    @staticmethod
    def PercentPosToReal(percentPos: Vector2) -> Vector2:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        screenRatio = screenWidth / screenHeight

        realX = (percentPos.x / (100 * screenRatio)) * screenWidth
        realY = (percentPos.y / 100) * screenHeight

        return Vector2(realX, realY)

    @staticmethod
    def PercentSizeToReal(percentSize: Vector2) -> Vector2:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        base = min(screenWidth, screenHeight)

        realW = (percentSize.x / 100.0) * base
        realH = (percentSize.y / 100.0) * base

        return Vector2(realW, realH)

    @staticmethod
    def GetEdgeXPercentage() -> float:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        
        return UI.RealSizeToPercent(Vector2(screenWidth, screenHeight)).x

    @staticmethod
    def GetEdgeYPercentage() -> float:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        
        return UI.RealSizeToPercent(Vector2(screenWidth, screenHeight)).y
    
    def __init__(self, type, relativePos:Vector2, relativeSize:Vector2, color:tuple, *, state:bool=True, zDist:int=1, underItems:list=[]):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.type = type
        
        self.originalRelativePos = relativePos
        self.originalRelativeSize = relativeSize
        
        self.color = color
        
        self.state = state
        self.zDist = zDist
        
        self.rect = None
        self.vertices = None
        
        self.underItems = underItems

        self.ResetRect()
    
    def MoveSet(self, newPos:Vector2):
        self.originalRelativePos = newPos
        
        self.ResetRect()

    def MoveSetReal(self, newPos:Vector2):
        self.originalRelativePos = UI.RealPosToPercent(newPos)
        
        self.ResetRect()

    def MoveSetRealX(self, newX:int|float):
        self.originalRelativePos = Vector2(UI.RealPosToPercent(Vector2(0,newX)).x, self.originalRelativePos.y)
        
        self.ResetRect()

    def MoveSetRealY(self, newY:int|float):
        self.originalRelativePos = Vector2(self.originalRelativePos.x, UI.RealPosToPercent(Vector2(0,newY)).y)
        
        self.ResetRect()
    
    def MoveSetCenter(self, newPos:Vector2):
        self.originalRelativePos = newPos - (self.originalRelativeSize/2)
        
        self.ResetRect()
    
    def MoveSetRealCenter(self, newPos:Vector2):
        self.originalRelativePos = UI.RealPosToPercent(newPos) - (self.originalRelativeSize/2)
        
        self.ResetRect()
    

    
    def MoveAdd(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos + addedPos
        
        self.ResetRect()
    
    def MoveAddReal(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos + UI.RealPosToPercent(addedPos)
        
        self.ResetRect()
    
    def MoveAddCenter(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos  + (addedPos - (self.originalRelativeSize/2))
        
        self.ResetRect()

    def MoveAddRealCenter(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos + (UI.RealPosToPercent(addedPos) - (self.originalRelativeSize/2))
        
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
    
    def SetState(self, newState:bool):
        self.state = newState
    
    def AddUnderItems(self, underItems:list):
        self.underItems.extend(underItems)
    
    def CheckCollidePoint(self, point) -> bool:
        if self.state:
            return self.rect.collidepoint(point)
        else:
            return False
    
    def GetZDist(self) -> int:
        return self.zDist
    
    def GetColor(self) -> tuple[float,float,float]:
        return self.color
    
    def GetPosPercent(self) -> Vector2:
        return self.originalRelativePos
    
    def GetPosPercentCenter(self) -> Vector2:
        return UI.RealPosToPercent(Vector2(*self.rect.center))
    
    def GetPosReal(self) -> Vector2:
        return Vector2(self.rect.x, self.rect.y)
    
    def GetPosRealCenter(self) -> Vector2:
        return Vector2(*self.rect.center)
    
    def GetSizePercent(self) -> Vector2:
        return self.originalRelativeSize
    
    def GetSizeReal(self) -> Vector2:
        return Vector2(self.rect.w, self.rect.h)
    
    def GetRect(self) -> pygame.Rect:
        return self.rect
    
    def GetUnderItem(self) -> list:
        return self.underItems

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
        if self.state:
            pygame.draw.polygon(con.SCREEN, self.color, self.vertices)

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
            angle_offset = -math.pi / 2 

            return [
                (
                    cx + radius * math.cos(2 * math.pi * i / 5 + angle_offset),
                    cy + radius * math.sin(2 * math.pi * i / 5 + angle_offset)
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