import pygame
import random
import Constants as con
from pygame.math import *
from Cell import Cell

class Grid():
    def __init__(self, size:Vector2):
        self.size = size
        
        self.cells = self.GenerateCells()
    
    def GenerateCells(self):
        cells = []
        for x in range(int(self.size.x) + 1):
            cellsX = []
            for y in range(int(self.size.y) + 1):
                cellsX.append(Cell(Vector2(x*con.CELLSIZE.x,y*con.CELLSIZE.y)))
            cells.append(cellsX)
        
        return cells
    
    def SetCell(self, pos:Vector2, state:bool):
        try:
            self.cells[int(pos.x)][int(pos.y)].SetState(state)
        except:
            print("Cell does not exist")
    
    def GetNeighbours(self, cellPos:Vector2):
        coords = [-1,0,1]
        neighbours = []
        
        for x in coords:
            for y in coords:
                zero = False
                if x == 0:
                    zero = True
                if y != 0:
                    zero = False
                
                if not zero:
                    neighbours.append(self.cells[x+int(cellPos.x)][y+int(cellPos.y)])
        
        return neighbours

    def DrawCells(self):
        for cellsX in self.cells:
            for cell in cellsX:
                cell.Draw()
    
    def UpdateCells(self):
        for cellsX in self.cells:
            for cell in cellsX:
                cell.update()