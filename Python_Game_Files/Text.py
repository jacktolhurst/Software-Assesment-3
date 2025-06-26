import pygame
import Constants as con
from pygame.math import Vector2

class Text():
    @staticmethod
    def RealPosToPercent(realPos:Vector2):
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        
        relativeX = (realPos.x / screenWidth) * 100
        relativeY = (realPos.y / screenHeight) * 100
        
        return Vector2(relativeX, relativeY)

    def __init__(self, textStr:str, font:str, relativePos:Vector2, relativeSize:int, color:tuple, state:bool=True):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.textStr = textStr
        
        self.origionalRelativePos = relativePos
        self.origionalRelativeSize = relativeSize
            
        self.color = color
        self.state = state
        
        self.fontStr = font
        self.font = None
        self.text = None
        self.rect = None
        self.ResetRect()
    
    
    def MoveSet(self, newPos:Vector2):
        self.origionalRelativePos = newPos
        
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.origionalRelativePos = self.origionalRelativePos + addedPos
        
        self.ResetRect()
    
    def SizeSet(self, newSize:Vector2):
        self.origionalRelativeSize = newSize
        
        self.ResetRect()
    
    def SizeAdd(self, addedSize:Vector2):
        self.origionalRelativeSize = self.origionalRelativeSize + addedSize
        
        self.ResetRect()
    
    def ChangeColor(self, newColor:tuple):
        self.color = newColor
        
        self.ResetRect()
    
    def SetState(self, newState):
        self.state = newState
    
    def ChangeText(self, newTextStr:str):
        self.textStr = newTextStr
        self.text = self.font.render(newTextStr, True, self.color)
    
    def GetRect(self) -> pygame.Rect:
        return self.rect

    
    def ResetRect(self):                
        
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
    
        fx = self.origionalRelativePos.x  / 100.0
        fy = self.origionalRelativePos.y  / 100.0

        base = min(self.screenWidth, self.screenHeight)

        absX = fx * base
        absY = fy * base
        
        relativeSize = int((((self.origionalRelativeSize/2))+((self.origionalRelativeSize/2)*self.screenHeight))/200) 
        
        self.font = pygame.font.Font(self.fontStr, relativeSize)
        self.text = self.font.render(self.textStr, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.topleft = Vector2(absX, absY)
    
    def Draw(self):
        con.SCREEN.blit(self.text, self.rect)


class InputText():
    def __init__(self, textStr:str, font:str, pos:Vector2, size:int, color:tuple, bgColor:tuple, state:bool=True):
        self.textStr = textStr
        
        self.pos = pos
        self.size = size
        self.color = color
        self.bgColor = bgColor
        self.state = state
        
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(textStr, True, color)
        self.rect = self.text.get_rect()
        self.bgRect = pygame.Rect(pos.x-35, pos.y-15, (size/2)*(len(textStr)+1),size)
        self.rect.center = pos
    
    def GetText(self):
        return self.textStr
    
    def MoveSet(self, newPos:Vector2):
        self.pos = newPos
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.pos = self.pos + addedPos
        self.ResetRect()
    
    def ChangeText(self, newTextStr:str):
        self.textStr = newTextStr
        self.text = self.font.render(newTextStr, True, self.color)
    
    def ChangeColor(self, newColor:tuple):
        self.color = newColor
        self.text = self.font.render(self.textStr, True, newColor, self.bgColor)
        
    def ChangeBGColor(self, newBGColor:tuple):
        self.bgColor = newBGColor
    
    def ClickIntersection(self, mousePos:Vector2):
        return self.bgRect.collidepoint(mousePos)
    
    def ResetTextRect(self):
        self.rect = self.text.get_rect()
    
    def Draw(self):
        pygame.draw.rect(con.SCREEN,
                    self.bgColor,
                    self.bgRect)
        con.SCREEN.blit(self.text, self.rect)
