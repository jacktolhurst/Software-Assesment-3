import pygame
import Constants as con

class Cell():
    def __init__(self, position, listPos):
        self.pos = position
        self.listPos = listPos

        self.color = (0,0,0)
        self.state = 1
        
        self.rect = pygame.Rect(position[0], position[1], con.CELLSIZE[0], con.CELLSIZE[1])
        
    
    def SetState(self, state):
        self.state = state
        if self.state == 0:
            self.color = con.BACKGROUNDCOLOR
        elif self.state == 1:
            self.color = (0,0,0)
        elif self.state == 2:
            self.color = (255,255,255)
        elif self.state == 3:
            self.color = (255, 0, 0)
            
    
    def Neighbours(self, grid):
        neighbours = []
        
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if (dx,dy) != (0,0):
                    
                    nx, ny = self.listPos[0] + dx, self.listPos[1] + dy
                    
                    if 0 <= ny < con.CELLAMOUNT[1] and 0 <= nx < con.CELLAMOUNT[0]:
                        neighbourCell = grid[nx][ny]
                        if neighbourCell.state != 0 :
                            neighbours.append(neighbourCell)

        return neighbours
    
    def Draw(self):        
        pygame.draw.rect(
            con.SCREEN, 
            self.color, 
            con.CAM.Apply(self.rect)
        )