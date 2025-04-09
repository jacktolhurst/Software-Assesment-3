import pygame
import Constants as con
from Cell import Cell

class Grid():
    def __init__(self):
        self.cells = []
    
    def CreateCells(self):
        for i in range(40):
            cellsX = [] 
            for j in range(40):
                cell = Cell((con.CELLPADDING[0]  + ((con.CELLPADDING[0] + con.CELLSIZE[0]) * j), con.CELLPADDING[1] + ((con.CELLPADDING[1]  + con.CELLSIZE[0]) * i)))
                cellsX.append(cell)
            self.cells.append(cellsX)
    
    def SetAll(self, state):
        for cellsX in self.cells: 
            for cell in cellsX:
                cell.SetState(state)

    def update(self):
        for cellsX in self.cells: 
            for cell in cellsX:
                cell.Draw()