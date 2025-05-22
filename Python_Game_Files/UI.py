import math
import pygame
import Constants as con
from pygame.math import Vector2

class UI:
    def __init__(self, type, pos:Vector2, size:Vector2, color:tuple, state:bool=True, width:int=0):
        self.type = type
        
        self.pos = pos
        self.size = size
        self.color = color
        
        self.state = state
        
        self.rect = None
        
        if self.type.objType == "Shape":
            self.width = width

            self.vertices = None

            self.ResetRect()
        elif self.type.objType == "Text":
            self.text = self.type.font.render('GeeksForGeeks', True, self.color)
            self.rect = self.text.get_rect()
            self.rect.center = (self.pos.x // 2, self.pos.y // 2)
    
    def MoveSet(self, newPos:Vector2):
        self.pos = newPos
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.pos = self.pos + addedPos
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def ResetRect(self):
        if self.type.objType == "Shape":
            self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
            self.vertices = self.type.GetVertices(self.rect)
        elif self.type.objType == "Text":
            self.rect.center = (self.pos.x // 2, self.pos.y // 2)
    
    def Draw(self):
        if self.type.objType == "Shape":
            pygame.draw.polygon(con.SCREEN, self.color, self.vertices, self.width)
        elif self.type.objType == "Text":
            con.SCREEN.blit(self.text, self.rect)

class Quad:
    objType = "Shape"
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [
            (rect.x, rect.y),
            (rect.x + rect.w, rect.y),
            (rect.x + rect.w, rect.y + rect.h),
            (rect.x, rect.y + rect.h)
            ]

class TriangleUp:
    objType = "Shape"
    @staticmethod
    def GetVertices(rect:pygame.Rect):
        return [
            (rect.x + rect.w/2, rect.y),
            (rect.x, rect.y + rect.h),
            (rect.x + rect.w, rect.y + rect.h)
            ]

class TriangleDown:
    objType = "Shape"
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x, rect.y),                     
            (rect.x + rect.w, rect.y),            
            (rect.x + rect.w / 2, rect.y + rect.h)
            ]

class TriangleLeft:
    objType = "Shape"
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x + rect.w, rect.y),          
            (rect.x + rect.w, rect.y + rect.h),    
            (rect.x, rect.y + rect.h / 2)         
            ]

class TriangleRight:
    objType = "Shape"
    @staticmethod
    def GetVertices(rect: pygame.Rect):
        return [
            (rect.x, rect.y),                   
            (rect.x, rect.y + rect.h),             
            (rect.x + rect.w, rect.y + rect.h / 2)  
            ]

class Pentagon:
    objType = "Shape"
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
    objType = "Shape"
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
    objType = "Shape"
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
    objType = "Shape"
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

class Text:
    objType = "Text"
    def __init__(self, text:str):
        self.text = text
        
        self.font = pygame.font.Font('freesansbold.ttf', 32)