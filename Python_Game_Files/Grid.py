import pygame
import Constants as con
from Cell import Cell

class Grid():
    def __init__(self):
        self.cells = []
    
    def CreateCells(self):
        cell = Cell((0,0))
        self.cells.append(cell)

    def update(self):
        for cell in self.cells: 
            cell.Draw()