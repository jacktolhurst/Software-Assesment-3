import pygame
import Constants as con

class Grid():
    def __init__(self, boxSize, color):
        self.sizeX = boxSize[0]
        self.sizeY = boxSize[1]
        
        self.color = color
        
        print("test")
    
    def Draw(self):
        # for i in range(int(con.WINDOW_WIDTH/self.sizeX)):
        pygame.draw.rect(con.SCREEN, self.color, pygame.Rect(30, 30, self.sizeX, self.sizeY))