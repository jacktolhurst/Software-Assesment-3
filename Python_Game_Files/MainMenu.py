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

class MainMenu():
    def __init__(self):
        self.looping = False
        
        self.tickSpeed = 5
        
        self.UIs = {}
        
        self.currCursor = None
        
        self.bgGrid = None
        self.bgGridAttributes = None
        self.lastBgGridPreset = None
        self.presetName = None
        self.CreateGrid()
        
        self.sandBoxLevel = None

        self.Start()
    
    def Start(self):
        self.looping = True
        
        changeGridInfo = Text("Changes the background.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
        self.UIs["ChangeGridText"] = Text("Change Background", Vector2(2,UI.GetEdgeYPercentage()-5), 8, (255,255,255), bgColor=(20,30,40,255))
        
        backgroundSize = Vector2(80,40)
        self.UIs["OptionsBackground"] = UI(Quad, Vector2((UI.GetEdgeXPercentage()/2)-(backgroundSize.x/2), (UI.GetEdgeYPercentage()/2)-(backgroundSize.y/2)), backgroundSize, (100,100,100))
        self.UIs["PlayForeground"] = UI(Quad, self.UIs["OptionsBackground"].GetPosPercent() + Vector2(1,1), Vector2(self.UIs["OptionsBackground"].GetSizePercent().x, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(2,2), (50,50,50))
        self.UIs["SettingsForeground"] = UI(Quad, self.UIs["PlayForeground"].GetPosPercent() + Vector2(0, self.UIs["PlayForeground"].GetSizePercent().y+1), Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2)+1, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(2,1), (50,50,50))
        self.UIs["AboutForeground"] = UI(Quad, self.UIs["SettingsForeground"].GetPosPercent() + Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2), 0), Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2)-1, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(1,1), (50,50,50))
        
        self.UIs["PlayText"] = Text("Play", UI.RealPosToPercent(Vector2(*self.UIs["PlayForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["PlayText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["PlayText"].GetRect().size))/2)*-1)
        self.UIs["SettingsText"] = Text("Settings", UI.RealPosToPercent(Vector2(*self.UIs["SettingsForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["SettingsText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["SettingsText"].GetRect().size))/2)*-1)
        self.UIs["AboutText"] = Text("About", UI.RealPosToPercent(Vector2(*self.UIs["AboutForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["AboutText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["AboutText"].GetRect().size))/2)*-1)
        # * THIS IS FUCKING MAGICAL CODE THAT FIGURES THE CENTRE OF A TEXT ELEMENT, DO NOT CHANGE. YES ITS 3AM.
        # sorry for swearing.
        
        self.UIs["RuleNameText"] = Text(self.presetName, Vector2(2,2), 8, (255,255,255))
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
        self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()
        lastGridChangeTime = pygame.time.get_ticks()     
        
        randomAddedTime = random.randint(-1000,1000)
        
        while self.looping:
            currTime = pygame.time.get_ticks()
            elapsedUpdateTime = currTime - lastUpdateTime
            elapsedGridChangeTime = currTime - lastGridChangeTime
            
            mousePos = pygame.mouse.get_pos()
            
            if self.UIs["ChangeGridText"].CheckCollidePoint(mousePos) or self.UIs["PlayForeground"].CheckCollidePoint(mousePos) or self.UIs["SettingsForeground"].CheckCollidePoint(mousePos) or self.UIs["ExitText"].CheckCollidePoint(mousePos) or self.UIs["AboutForeground"].CheckCollidePoint(mousePos):
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
                    elif self.UIs["PlayForeground"].CheckCollidePoint(mousePos):
                        self.sandBoxLevel = SandBoxLVL()
                    elif self.UIs["ExitText"].CheckCollidePoint(mousePos):
                        self.Stop()
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            if elapsedUpdateTime >= (1000 / self.tickSpeed):
                self.bgGrid.Update()
                
                lastUpdateTime = currTime
            
            if elapsedGridChangeTime >= 5000 + randomAddedTime:
                self.CreateGrid()
                
                randomAddedTime = random.randint(-1000,1000)
                lastGridChangeTime = currTime
            
            self.UIs["RuleNameText"].ChangeText(self.presetName)
            
            self.sandBoxLevel = None
            
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