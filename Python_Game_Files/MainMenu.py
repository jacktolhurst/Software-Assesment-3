import pygame
import json
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import *

class MainMenu():
    def __init__(self):
        self.looping = False
        
        self.tickSpeed = 5
        
        self.UIs = {}
        
        self.currCursor = None
        
        self.bgGrid = None
        self.bgGridAttributes = None
        self.lastBgGridPreset = None
        self.CreateGrid()

        self.Start()
    
    def Start(self):
        self.looping = True
        
        changeGridInfo = Text("Changes the background.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
        self.UIs["ChangeGridText"] = Text("Change Background", Vector2(2,UI.GetEdgeYPercentage()-5), 8, (255,255,255), bgColor=(20,30,40,255))
        
        self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()     
        
        while self.looping:
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()
            
            if self.UIs["ChangeGridText"].CheckCollidePoint(mousePos):
                desired = con.HANDCURSOR
            else:
                desired = con.ARROWCURSOR
            
            if desired is not self.currCursor:
                    pygame.mouse.set_cursor(desired)
                    self.currCursor = desired
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.Stop()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.UIs["ChangeGridText"].CheckCollidePoint(mousePos):
                        self.CreateGrid()
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            if elapsedTime >= (1000 / self.tickSpeed):
                self.bgGrid.Update()
                
                lastUpdateTime = currTime
            
            if currTime % 1000 == 1:
                self.CreateGrid()
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill((0,0,0))
        
        self.bgGrid.DrawCells()
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
    
    def CreateRandomCells(self, randomCellAmount:int=100):
        maxX = int(self.bgGrid.size.x) - 1
        maxY = int(self.bgGrid.size.y) - 1
        
        spawnedCells = [Vector2(random.randint(1, maxX-1), random.randint(1, maxY-1))]
        
        for i in range(randomCellAmount):
            lastPos = spawnedCells[len(spawnedCells)-1]
            
            offset = random.choice(Grid.possibleOffsets)
            
            addedOffset = lastPos+Vector2(*offset)
            
            if self.bgGrid.GetCell(addedOffset).GetState() == State.UNTOUCH or self.bgGrid.GetCell(addedOffset).GetState() == State.ALIVE:
                randomCellAmount += 1
            else:
                spawnedCells.append(addedOffset)
            
        
        for spawnedCellPos in spawnedCells:
            self.bgGrid.SetCell(spawnedCellPos, State.ALIVE)
    
    def CreateGrid(self):
        with open(con.SETTINGSSAVEPATH, 'r') as file:
            data = json.load(file)
        preset = random.choice(list(data.values()))
        while self.lastBgGridPreset == preset:
            preset = random.choice(list(data.values()))
        self.lastBgGridPreset = preset
        self.bgGridAttributes = GridAttributes(**preset)
        self.bgGridAttributes.gridSize = Grid.ScreenToGridSize()
        
        self.bgGrid = Grid(self.bgGridAttributes)
        self.CreateRandomCells(3000)
        
    def ResetScreen(self):
        pass
        
    def Stop(self):
        if self.looping:
            self.looping = False