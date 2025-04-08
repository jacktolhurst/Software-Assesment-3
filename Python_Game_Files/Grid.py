import pygame
import Constants as con
from Cell import Cell

class Grid():
    def __init__(self):
        self.cells = []
    
    def CreateCells(self):
        for i in range(10):
            cellsX = [] 
            for j in range(10):
                cell = Cell((1 + ((5 + con.CELLSIZE[0]) * j), 5 + ((5 + con.CELLSIZE[0]) * i)))
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