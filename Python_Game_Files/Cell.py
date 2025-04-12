import pygame
import Constants as con

class Cell():
    def __init__(self, position):
        self.pos = position

        self.color = (0,0,0)
        self.state = False
        
        self.rect = pygame.Rect(position[0], position[1], con.CELLSIZE[0], con.CELLSIZE[1])
        
    
    def SetState(self, state):
        self.state = state
        if self.state == True:
            self.color = (255,255,255)
        else:
            self.color = (0,0,0)
    
    def Draw(self):        
        pygame.draw.rect(
            con.SCREEN, 
            self.color, 
            con.CAM.Apply(self.rect)
        )