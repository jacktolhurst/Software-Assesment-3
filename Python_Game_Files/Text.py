import pygame
import Constants as con
from pygame.math import Vector2

class Text():
    def __init__(self, textStr:str, font:str, relativePos:Vector2, relativeSize:int, color:tuple, bgColor:tuple=(0,0,0,0), padding:int=4, state:bool=True):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.textStr = textStr
        
        self.origionalRelativePos = relativePos
        self.origionalRelativeSize = relativeSize
        
        self.color = color
        self.bgColor = bgColor
        self.initialBgColor = bgColor
        self.padding = padding
        self.state = state
        
        self.fontStr = font
        self.font = None
        self.text = None
        self.rect = None
        self.bgRect = None
        self.bgSurf = None
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
    
    def ChangeBgColor(self, newBgColor:tuple):
        self.bgColor = newBgColor
        
        self.ResetRect()
    
    def ChangeText(self, newTextStr:str):
        self.textStr = newTextStr
        
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def CheckCollidePoint(self, point) -> bool:
        return self.bgRect.collidepoint(point)
    
    def GetText(self) -> str:
        return self.textStr
    
    def GetColor(self) -> tuple[float,float,float]:
        return self.color
    
    def GetBgColor(self) -> tuple[float,float,float]:
        return self.bgColor
    
    def GetInitialBgColor(self) -> tuple[float,float,float]:
        return self.initialBgColor
    
    def GetPosPercent(self) -> Vector2:
        return self.originalRelativePos
    
    def GetSizePercent(self) -> Vector2:
        return self.originalRelativeSize
    
    def GetRect(self) -> pygame.Rect:
        return self.rect

    
    def ResetRect(self):                
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
    
        fx = self.origionalRelativePos.x  / 100.0
        fy = self.origionalRelativePos.y  / 100.0

        base = min(self.screenWidth, self.screenHeight)

        absX = fx * base
        absY = fy * base
        pos = Vector2(absX, absY)
        
        relativeSize = int((((self.origionalRelativeSize/2))+((self.origionalRelativeSize/2)*self.screenHeight))/200) 
        
        self.font = pygame.font.Font(self.fontStr, relativeSize)
        self.text = self.font.render(self.textStr, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.topleft = pos
        
        textW, textH = self.font.size(self.textStr)   
        
        self.bgRect = pygame.Rect(pos.x, pos.y,max(textW+self.padding, 35),textH+self.padding)
        self.bgSurf = pygame.Surface(pygame.Rect(self.bgRect).size, pygame.SRCALPHA)
        self.bgSurf.fill(self.bgColor)
    
    def Draw(self):
        con.SCREEN.blit(self.bgSurf, self.bgRect)
        con.SCREEN.blit(self.text, self.rect)
