import pygame
import json
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import *
from SandboxLevel import SandBoxLVL

class Settings():
    def __init__(self):
        self.looping = False
        
        self.UIs = {}
        
        self.currCursor = None

        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.UIs["ColourPickerBg"] = con.HANDLER.CreateColourWheel(Vector2(10,10), Vector2(10,10))
        self.UIs["ColourPickerPointer"] = self.UIs["ColourPickerBg"].GetUnderItem()[0]
        
        self.Update()
    
    def Update(self):
        while self.looping:
            mousePos = pygame.mouse.get_pos()
            
            self.UIs["ColourPickerPointer"].MoveSet(UI.RealPosToPercent(Vector2(*mousePos))-(self.UIs["ColourPickerPointer"].GetSizePercent()/2))
            
            if False:
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
                    pass
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            self.sandBoxLevel = None
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
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
        presets = list(data.items())
        name, preset = random.choice(presets)
        while name == self.presetName:
            name, preset = random.choice(presets)
        self.presetName = name
        self.bgGridAttributes = GridAttributes(**preset)
        self.bgGridAttributes.gridSize = Grid.ScreenToGridSize()

        self.bgGrid = Grid(self.bgGridAttributes)
        self.CreateRandomCells(1000)
        
    def ResetScreen(self):
        pass
        
    def Stop(self):
        if self.looping:
            self.looping = False