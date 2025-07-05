import Constants as con
import pygame
import pygame
from pygame.math import *
from Cell import Cell, State

class Grid():
    possibleOffsets = [(dx, dy) 
        for dx in (-1, 0, 1) 
        for dy in (-1, 0, 1) 
        if not (dx == 0 and dy == 0)]
    
    @staticmethod
    def ScreenToGridSize() -> Vector2:
        screenWidth, screenHeight = pygame.display.get_surface().get_size()
        
        stride = con.CELLSIZE * con.CELLGAP
        
        totalCols = int(screenWidth // stride)
        totalRows = int(screenHeight // stride)

        # subtract the border on *both* sides
        usableCols = max(0, totalCols - 2)
        usableRows = max(0, totalRows - 2)

        return Vector2(usableCols, usableRows)
    
    def __init__(self, gridAttributes, offset:Vector2=Vector2(0,0)):
        self.gridAttributes = gridAttributes
        self.size = gridAttributes.gridSize + Vector2(1,1)
        
        self.offset = offset
        
        self.buffer = {}
        self.activeCells = set()
        self.stationaryCells = set()
        
        self.cells = self.GenerateCells()
        self.prevPlayCells = self.cells
        
        self.onScreenCells = {}
        
        self.MoveCells()
        self.DrawCells()
    
    def GenerateCells(self):
        cells = []
        for x in range(int(self.size.x) + 1):
            cellsX = []
            for y in range(int(self.size.y) + 1):
                cellPos = Vector2(x*con.CELLGAP*con.CELLSIZE+self.offset.x,y*con.CELLGAP*con.CELLSIZE+self.offset.y)
                cell = Cell(cellPos, State.DEAD)
                if x == 0 or y == 0 or x == int(self.size.x) or y == int(self.size.y):
                    cell.SetState(State.UNTOUCH)
                    self.stationaryCells.add((x, y))
                cellsX.append(cell)
            cells.append(cellsX)
        
        return cells
    
    
    def SetCell(self, cellPos:Vector2, state:State):
        cell = self.cells[int(cellPos.x)][int(cellPos.y)]
        if cell.state != state:
            self.buffer[(cellPos.x, cellPos.y)] = state
            if state == State.ALIVE or state == State.DEAD:
                self.activeCells.add((cellPos.x, cellPos.y))
                for offset in Grid.possibleOffsets:
                    newX = int(cellPos.x) + offset[0]
                    newY = int(cellPos.y) + offset[1]
                    if 0 <= newX < len(self.cells) and 0 <= newY < len(self.cells[0]):
                        self.activeCells.add((newX, newY))
            else:
                self.stationaryCells.add((cellPos.x, cellPos.y))
    
    def GetCell(self, cellPos:Vector2):
        return self.cells[int(cellPos.x)][int(cellPos.y)]

    def GetNeighbours(self, cellPos: Vector2):
        neighbours = []
        
        for offset in Grid.possibleOffsets:
                newX = int(cellPos.x) + offset[0]
                newY = int(cellPos.y) + offset[1]

                if 0 <= newX < len(self.cells) and 0 <= newY < len(self.cells[0]):
                    neighbours.append(self.cells[newX][newY])

        return neighbours

    def CheckCellState(self, cellPos:Vector2):
        neighbours = self.GetNeighbours(cellPos)
        cell = self.cells[int(cellPos.x)][int(cellPos.y)]

        liveCount = sum(neighbour.state == State.ALIVE for neighbour in neighbours)

        if cell.state == State.ALIVE and liveCount < self.gridAttributes.underPopulationThreshold:
            return State.DEAD
        elif cell.state == State.ALIVE and (liveCount == self.gridAttributes.survivalMin or liveCount == self.gridAttributes.survivalMax):
            return State.ALIVE
        elif cell.state == State.ALIVE and liveCount > self.gridAttributes.overpopulationThreshold:
            return State.DEAD
        elif cell.state == State.DEAD and liveCount == self.gridAttributes.reproductionCount:
            return State.ALIVE

        return cell.state

    def ClickIntersection(self, mousePos, state:State=State.DEAD):
        for cell, cellPos in self.onScreenCells.items():
            if cell.state != State.UNTOUCH:
                if cell.CheckMouseCollide(mousePos):
                    self.SetCell(cellPos, state)
                    break

    def MoveCells(self):
        onScreenCellsNew = {}
        posX = 0
        for cellsX in self.cells:
            posY = 0 
            for cell in cellsX:
                cell.Move()
                if cell.IsOnScreen():
                    onScreenCellsNew[cell] = Vector2(posX, posY)
                posY += 1
            posX += 1
        
        self.onScreenCells = onScreenCellsNew

    def ApplyBuffer(self):
        for cellPos, cellState in self.buffer.items():
            self.cells[int(cellPos[0])][int(cellPos[1])].SetState(cellState)
        
        self.buffer.clear()

    def DrawCells(self):
        self.ApplyBuffer()
        
        
        
        for cellsX in self.cells:
            for cell in cellsX:
                cell.Draw()
    
    def Update(self):
        oldActiveCells = list(self.activeCells)
        self.activeCells.clear()
        
        for cellPos in oldActiveCells:
            cellPos = Vector2(cellPos)
            self.SetCell(cellPos, self.CheckCellState(cellPos))
    
    def GetGridAttributes(self):
        return self.gridAttributes

class GridAttributes():    
    def __init__(self, gridSize:Vector2=Vector2(100,100), underPopulationThreshold:int=2, survivalMin:int=2, survivalMax:int=3, overpopulationThreshold:int=3, reproductionCount:int=3):
        self.gridSize = gridSize
        self.underPopulationThreshold = underPopulationThreshold
        self.survivalMin = survivalMin
        self.survivalMax = survivalMax
        self.overpopulationThreshold = overpopulationThreshold
        self.reproductionCount = reproductionCount
    
    def ToDict(self):
        return {
            "gridSize": [self.gridSize.x, self.gridSize.y],  # Serialize Vector2 as a list
            "underPopulationThreshold": self.underPopulationThreshold,
            "survivalMin": self.survivalMin,
            "survivalMax": self.survivalMax,
            "overpopulationThreshold": self.overpopulationThreshold,
            "reproductionCount": self.reproductionCount
        }

    def FromDict(self, data):
        self.gridSize=Vector2(*data["gridSize"])
        self.underPopulationThreshold=data["underPopulationThreshold"]
        self.survivalMin=data["survivalMin"]
        self.survivalMax=data["survivalMax"]
        self.overpopulationThreshold=data["overpopulationThreshold"]
        self.reproductionCount=data["reproductionCount"]