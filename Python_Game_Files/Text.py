import pygame
import Constants as con
from pygame.math import Vector2

class Text():
    @staticmethod
    def RealPosToPercent(realPos:Vector2):
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        screenRatio = screenWidth/screenHeight
        
        relativeX = ((realPos.x / screenWidth)*screenRatio) * 100
        relativeY = (realPos.y / screenHeight) * 100
        
        return Vector2(relativeX, relativeY)

    def __init__(self, textStr:str, font:str, relativePos:Vector2, relativeSize:int, color:tuple, state:bool=True):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        
        self.textStr = textStr
        
        self.origionalRelativePos = relativePos
        self.origionalRelativeSize = relativeSize
        self.relativePos =  Vector2(min(self.origionalRelativePos.x/self.screenRatio,100)/100,min(self.origionalRelativePos.y,100)/100)
        self.relativeSize = min(self.origionalRelativeSize/self.screenRatio,100)
        
        self.color = color
        self.state = state
        
        self.fontStr = font
        self.font = None
        self.text = None
        self.rect = None
        self.ResetRect()
    
    
    def MoveSet(self, newPos:Vector2):
        self.pos = newPos
        self.ResetRect()
    
    def MoveAdd(self, addedPos:Vector2):
        self.pos = self.pos + addedPos
        self.ResetRect()
    
    def ChangeText(self, newTextStr:str):
        self.textStr = newTextStr
        self.text = self.font.render(newTextStr, True, self.color)
    
    def ResetRect(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        self.screenRatio = self.screenWidth/self.screenHeight
        self.relativeSize = int(min(self.origionalRelativeSize/self.screenRatio,100))
        
        self.relativePos = Vector2(min(self.origionalRelativePos.x/self.screenRatio,100)/100,min(self.origionalRelativePos.y,100)/100)
        
        absX = self.relativePos.x * self.screenWidth
        absY = self.relativePos.y * self.screenHeight
        absPos = Vector2(absX, absY)
        
        self.font = pygame.font.Font(self.fontStr, self.relativeSize)
        self.text = self.font.render(self.textStr, True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = absPos
    
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
