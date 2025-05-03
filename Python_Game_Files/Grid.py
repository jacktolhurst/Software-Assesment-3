import pygame
import random
import Constants as con
from pygame.math import *
from Cell import Cell

class Grid():
    def __init__(self, size:Vector2):
        self.size = size
        
        self.cells = self.GenerateCells()
        
        self.buffer = {}
    
    def GenerateCells(self):
        cells = []
        for x in range(int(self.size.x) + 1):
            cellsX = []
            for y in range(int(self.size.y) + 1):
                cellsX.append(Cell(Vector2(x*con.CELLGAP*con.CELLSIZE.x,y*con.CELLGAP*con.CELLSIZE.y)))
            cells.append(cellsX)
        
        return cells
    
    
    def SetCell(self, cell: Vector2 | Cell, state: bool):
        if isinstance(cell, Vector2):
            pos = cell
        else:
            pos = self.GetCellPosition(cell)
        
        self.buffer[(pos.x, pos.y)] = state

    def GetCellPosition(self, target_cell: Cell):
        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                if cell is target_cell: 
                    return Vector2(x, y)
        print("No such cell")
        return None

    def GetNeighbours(self, cellPos: Vector2):
        coords = [-1, 0, 1]
        neighbours = []

        for x in coords:
            for y in coords:
                if x == 0 and y == 0:
                    continue 
                
                newX = int(cellPos.x) + x
                newY = int(cellPos.y) + y

                if 0 <= newX < len(self.cells) and 0 <= newY < len(self.cells[0]):
                    neighbours.append(self.cells[newX][newY])

        return neighbours

    def CheckCellState(self, cellPos: Vector2):
        neighbours = self.GetNeighbours(cellPos)
        cell = self.cells[int(cellPos.x)][int(cellPos.y)]

        liveCount = sum(neighbour.state for neighbour in neighbours)

        if cell.state and liveCount < 2:
            return False
        if cell.state and (liveCount == 2 or liveCount == 3):
            return True
        if cell.state and liveCount > 3:
            return False
        if not cell.state and liveCount == 3:
            return True

        return cell.state

    def ClickIntersection(self, mousePos):
        for cellsX in self.cells:
            for cell in cellsX:
                if cell.CheckMouseCollide(mousePos):
                    self.SetCell(cell, not cell.state)

    def ApplyBuffer(self):
        for cellPos, cellState in self.buffer.items():
            self.cells[int(cellPos[0])][int(cellPos[1])].SetState(cellState)

    def DrawCells(self):
        self.ApplyBuffer()
        
        for cellsX in self.cells:
            for cell in cellsX:
                cell.Draw()
    
    def Update(self):
        for dx in range(int(self.size.x)):
            for dy in range(int(self.size.y)):
                cellPos = Vector2(dx,dy)
                self.SetCell(cellPos, self.CheckCellState(cellPos))