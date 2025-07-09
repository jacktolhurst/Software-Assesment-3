import pygame
import Constants as con
from pygame.math import Vector2
from UI import UI

class Text():
    def __init__(self, textStr:str, relativePos:Vector2, relativeSize:int, color:tuple, *, font:str='freesansbold.ttf', bgColor:tuple=(0,0,0,0), maxStrLength:int=1000, numOnly:bool=False, state:bool=True, zDist:int=1, underItems:list=[], defaultStr:str=""):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.originalRelativePos = relativePos
        self.originalRelativeSize = relativeSize
        
        self.color = color
        self.bgColor = bgColor
        self.maxStrLength = maxStrLength
        self.numOnly = numOnly
        self.initialBgColor = bgColor
        self.state = state
        self.underItems = underItems
        self.zDist = zDist
        self.defaultStr = defaultStr
        
        self.fontStr = font
        self.font = None
        self.text = None
        self.rect = None
        self.bgRect = None
        self.bgSurf = None
        
        self.textStr = "Err"
        self.ChangeText(textStr)
        
        
        self.ResetRect()
    
    
    def MoveSet(self, newPos:Vector2):
        self.originalRelativePos = newPos
        
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.originalRelativePos = self.originalRelativePos + addedPos
        
        self.ResetRect()
    
    def SizeSet(self, newSize:int):
        self.originalRelativeSize = newSize
        
        self.ResetRect()
    
    def SizeAdd(self, addedSize:int):
        self.originalRelativeSize = self.originalRelativeSize + addedSize
        
        self.ResetRect()
    
    def ChangeColor(self, newColor:tuple):
        self.color = newColor
        
        self.ResetRect()
    
    def ChangeBgColor(self, newBgColor:tuple):
        self.bgColor = newBgColor
        
        self.ResetRect()
    
    def ChangeText(self, newTextStr:str, checkDefaultStr:bool=False):
        if checkDefaultStr and newTextStr.strip() == "":
            newTextStr = self.defaultStr
        
        if len(newTextStr) <= self.maxStrLength:
            if self.numOnly:
                if newTextStr.isdigit() or newTextStr == "":
                    self.textStr = newTextStr
            else:
                self.textStr = newTextStr
    
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def CheckCollidePoint(self, point) -> bool:
        if self.state:
            return self.rect.collidepoint(point)
        else:
            return False
    
    def GetSizePercent(self) -> int:
        return self.originalRelativeSize
    
    def GetZDist(self) -> int:
        return self.zDist
    
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
    
    def GetPosReal(self) -> Vector2:
        return UI.PercentPosToReal(self.originalRelativePos)
    
    def GetRect(self) -> pygame.Rect:
        return self.rect
    
    def GetRectSize(self) -> Vector2:
        return UI.RealPosToPercent(Vector2(*self.rect.size))

    def GetBgRect(self) -> pygame.Rect:
        return self.bgRect

    def GetBgRectSize(self) -> Vector2:
        return UI.RealPosToPercent(Vector2(*self.bgRect.size))

    def GetBgSurf(self) -> pygame.Surface:
        return self.bgSurf

    def GetUnderItem(self):
        return self.underItems
    
    def ResetRect(self):                
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
    
        fx = self.originalRelativePos.x  / 100.0
        fy = self.originalRelativePos.y  / 100.0

        base = min(self.screenWidth, self.screenHeight)

        absX = fx * base
        absY = fy * base
        pos = Vector2(absX, absY)
        
        relativeSize = int((((self.originalRelativeSize/2))+((self.originalRelativeSize/2)*self.screenHeight))/200) 
        
        self.font = pygame.font.Font(self.fontStr, relativeSize)
        self.text = self.font.render(self.textStr, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.topleft = pos
        
        textW, textH = self.font.size(self.textStr)   
        
        minWidth = int(base * 0.035) 
        self.bgRect = pygame.Rect(pos.x-3, pos.y-4, max(textW + 4, minWidth), textH + 4)
        self.bgSurf = pygame.Surface(pygame.Rect(self.bgRect).size, pygame.SRCALPHA)
        self.bgSurf.fill(self.bgColor)
    
    def Draw(self):
        if self.state:
            con.SCREEN.blit(self.bgSurf, self.bgRect)
            con.SCREEN.blit(self.text, self.rect)
