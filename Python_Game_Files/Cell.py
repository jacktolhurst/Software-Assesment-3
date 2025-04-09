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
        zoom = con.CURRENTSCROLL
        offset = con.SCREENPOS
        
        scaled_x = (self.pos[0] * zoom) + offset[0]
        scaled_y = (self.pos[1] * zoom) + offset[1]
        scaled_width = con.CELLSIZE[0] * zoom
        scaled_height = con.CELLSIZE[1] * zoom

        pygame.draw.rect(
            con.SCREEN, 
            self.color, 
            pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        )