import Constants as con
from pygame.math import *
from Cell import Cell, State

class Grid():
    possibleOffsets = [(dx, dy) 
        for dx in (-1, 0, 1) 
        for dy in (-1, 0, 1) 
        if not (dx == 0 and dy == 0)]
    
    def __init__(self, size:Vector2, offset:Vector2=Vector2(0,0)):
        self.size = size
        self.offset = offset
        
        self.buffer = {}
        self.activeCells = set()
        self.stationaryCells = set()
        
        self.cells = self.GenerateCells()
        self.prevPlayCells = self.cells

        
        self.DrawCells()
    
    def GenerateCells(self):
        cells = []
        for x in range(int(self.size.x) + 1):
            cellsX = []
            for y in range(int(self.size.y) + 1):
                cellPos = Vector2(x*con.CELLGAP*con.CELLSIZE.x+self.offset.x,y*con.CELLGAP*con.CELLSIZE.y+self.offset.y)
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

        if cell.state == State.ALIVE and liveCount < 2:
            return State.DEAD
        elif cell.state == State.ALIVE and (liveCount == 2 or liveCount == 3):
            return State.ALIVE
        elif cell.state == State.ALIVE and liveCount > 3:
            return State.DEAD
        elif cell.state == State.DEAD and liveCount == 3:
            return State.ALIVE
        elif cell.state == State.PRIZE and liveCount > 0:
            con.WON = True
            return State.ALIVE

        return cell.state

    def ClickIntersection(self, mousePos, state:State=State.DEAD):
        for dx in range(int(self.size.x)+1):
            for dy in range(int(self.size.y)+1):
                cellPos = Vector2(dx,dy)
                cell = self.cells[dx][dy]
                if cell.state != State.UNTOUCH and cell.state != State.PRIZE:
                    if cell.CheckMouseCollide(mousePos):
                        self.SetCell(cellPos, state)
                        break

    def MoveCells(self):
        for cellsX in self.cells:
            for cell in cellsX:
                cell.Move()

    def ApplyBuffer(self):
        for cellPos, cellState in self.buffer.items():
            self.cells[int(cellPos[0])][int(cellPos[1])].SetState(cellState)
        
        self.buffer.clear()

    def DrawCells(self):
        self.ApplyBuffer()
        
        for cellPos in self.activeCells:
            self.cells[int(cellPos[0])][int(cellPos[1])].Draw()
        
        for cellPos in self.stationaryCells:
            self.cells[int(cellPos[0])][int(cellPos[1])].Draw()
    
    def Update(self):
        oldActiveCells = list(self.activeCells)
        self.activeCells.clear()
        
        for cellPos in oldActiveCells:
            cellPos = Vector2(cellPos)
            self.SetCell(cellPos, self.CheckCellState(cellPos))