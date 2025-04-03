import os
import time

cells = [
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, True, False, False, False, False, False, False, False]
]

def FindNeighbours(grid, location):
    x, y = location
    rows, cols = len(grid), len(grid[0])
    
    neighbours = []
    
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  
            nx, ny = x + dx, y + dy
            if 0 <= ny < rows and 0 <= nx < cols:
                neighbours.append(grid[ny][nx])
    
    return neighbours

def CheckCells(grid, location):
    x, y = location
    neighbours = FindNeighbours(grid, location)
    alive_neighbours = neighbours.count(True)

    if grid[y][x]: 
        return alive_neighbours in [2, 3]
    else: 
        return alive_neighbours == 3

while True:
    os.system('cls' if os.name == 'nt' else 'clear')    
    
    for row in cells:
        print(" ".join("█" if cell else "." for cell in row))
    print("\n")

    new_cells = [[CheckCells(cells, (j, i)) for j in range(len(cells[0]))] for i in range(len(cells))]

    cells = new_cells  
    
    time.sleep(0.2)
