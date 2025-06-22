import pygame
import Constants as con
from pygame.math import Vector2

class Text():    
    def __init__(self, textStr:str, font:str, pos:Vector2, size:int, color:tuple, state:bool=True):
        self.textStr = textStr
        
        self.pos = pos
        self.size = size
        self.color = color
        self.state = state
        
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(textStr, True, color)
        self.rect = self.text.get_rect()
        self.rect.center = pos
    
    
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
        self.rect = self.text.get_rect()
    
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
        self.text = self.font.render(textStr, True, color, bgColor)
        self.rect = self.text.get_rect()
        self.rect.center = pos
    
    
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
        self.text = self.font.render(self.textStr, True, self.Color, newBGColor)
        
    def ResetRect(self):
        self.rect = self.text.get_rect()
    
    def Draw(self):
        con.SCREEN.blit(self.text, self.rect)