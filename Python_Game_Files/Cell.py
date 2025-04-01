import pygame
import Constants as con

class Cell():
    def __init__(self, position):
        self.pos = position

        self.color = (0,0,0)
        self.state = False
        
    
    def SetState(self, state):
        self.state = state
        if self.state == True:
            self.color = (255,255,255)
        else:
            self.color = (0,0,0)
    
    def Draw(self):
        pygame.draw.rect(con.SCREEN, self.color, pygame.Rect(self.pos[0], self.pos[1], con.CELLSIZE[0], con.CELLSIZE[1]))