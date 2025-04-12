import pygame
import Constants as con
from Cell import Cell

class Grid():
    def __init__(self):
        self.cells = []
    
    def CreateCells(self):
        for i in range(con.CELLAMOUNT[0]):
            cellsX = [] 
            for j in range(con.CELLAMOUNT[1]):
                cell = Cell((con.CELLPADDING[0]  + ((con.CELLPADDING[0] + con.CELLSIZE[0]) * j), con.CELLPADDING[1] + ((con.CELLPADDING[1]  + con.CELLSIZE[0]) * i)), (j,i))
                cellsX.append(cell)
            self.cells.append(cellsX)
    
    def SetAll(self, state=int):
        for cellsX in self.cells: 
            for cell in cellsX:
                cell.SetState(state)
    
    def SetSpecific(self, setCells=dict):
        for cellPos, value in setCells.items():
            self.cells[cellPos[1]][cellPos[0]].SetState(value)
    
    def CheckLiving(self, neighbours, currentState):
        neighbourStates = []
        for neighbour in neighbours:
            neighbourStates.append(neighbour.state)
        aliveNeighbours = neighbourStates.count(2)
        
        if currentState == 2:
            return aliveNeighbours in [2, 3]
        else:
            return aliveNeighbours == 3


    def update(self):
        newStates = []

        for row in self.cells:
            newRow = []
            for cell in row:
                alive = self.CheckLiving(cell.Neighbours(self.cells), cell.state == 2)
                newState = 2 if alive else 1
                newRow.append(newState)
            newStates.append(newRow)

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.SetState(newStates[i][j])
                cell.Draw()
