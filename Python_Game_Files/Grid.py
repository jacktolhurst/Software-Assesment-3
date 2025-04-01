import pygame
import Constants as con
from Cell import Cell

class Grid():
    def __init__(self):
        self.Cells = []
    
    def Draw(self):
        for i in range(int(con.WINDOW_HEIGHT/con.CELLSIZE[1])):
            for j in range(int(con.WINDOW_HEIGHT/con.CELLSIZE[0])):
                cell = Cell((j*con.CELLSIZE[0],i*con.CELLSIZE[1]))
                self.Cells.append(cell)
                
                cell.Draw()