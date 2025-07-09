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
from Settings import Settings

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
        self.settings = None

        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.ResetScreen()
        
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
            
            if self.UIs["RestartSymbolForeground"].CheckCollidePoint(mousePos) or self.UIs["PlayForeground"].CheckCollidePoint(mousePos) or self.UIs["SettingsForeground"].CheckCollidePoint(mousePos) or self.UIs["ExitText"].CheckCollidePoint(mousePos) or self.UIs["AboutForeground"].CheckCollidePoint(mousePos):
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
                    if event.button == 1:
                        if self.UIs["RestartSymbolForeground"].CheckCollidePoint(mousePos):
                            self.CreateGrid()
                        elif self.UIs["PlayForeground"].CheckCollidePoint(mousePos):
                            self.sandBoxLevel = SandBoxLVL()
                            self.CreateGrid()
                        elif self.UIs["SettingsForeground"].CheckCollidePoint(mousePos):
                            self.settings = Settings()
                            self.CreateGrid()
                        elif self.UIs["ExitText"].CheckCollidePoint(mousePos):
                            self.Stop()
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            if elapsedUpdateTime >= (1000 / self.tickSpeed):
                self.bgGrid.Update()
                
                lastUpdateTime = currTime
            
            if elapsedGridChangeTime >= 10000 + randomAddedTime:
                self.CreateGrid()
                
                randomAddedTime = random.randint(-1000,1000)
                lastGridChangeTime = currTime
            
            self.UIs["RuleNameText"].ChangeText(self.presetName)
            
            self.sandBoxLevel = None
            self.settings = None
            
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
        con.CELLOFFSETT = Vector2(0,0)
        con.CELLSIZE = 20
        con.CELLGAP = 0.99
        
        with open(con.ATTRIBUTESSAVEPATH, 'r') as file:
            data = json.load(file)
        presets = list(data.items())
        name, preset = random.choice(presets)
        while name == self.presetName:
            name, preset = random.choice(presets)
        self.presetName = name
        self.bgGridAttributes = GridAttributes(**preset)
        self.bgGridAttributes.gridSize = Grid.ScreenToGridSize()

        self.bgGrid = Grid(self.bgGridAttributes)
        
        if self.bgGridAttributes.gridSize.x > 1 and self.bgGridAttributes.gridSize.y > 1:
            self.CreateRandomCells(int(self.bgGrid.size.x * 10))
        
    def ResetScreen(self):
        self.UIs["RestartSymbolBackground"] = UI(Quad, Vector2(0,0), Vector2(10,10), (100,100,100))
        self.UIs["RestartSymbolBackground"].MoveSet(Vector2(2, (UI.GetEdgeYPercentage()-self.UIs["RestartSymbolBackground"].GetSizePercent().y)-3))
        self.UIs["RestartSymbolForeground"] = UI(Quad, self.UIs["RestartSymbolBackground"].GetPosPercent()+Vector2(1,1), self.UIs["RestartSymbolBackground"].GetSizePercent()-Vector2(2,2), (50,50,50))
        self.UIs["RestartSymbolOuterCircle"] = UI(Circle,UI.RealPosToPercent(Vector2(*self.UIs["RestartSymbolBackground"].GetRect().center)), self.UIs["RestartSymbolForeground"].GetSizePercent()-Vector2(1,1), (0,0,255))
        self.UIs["RestartSymbolOuterCircle"].MoveAdd(UI.RealSizeToPercent(Vector2(self.UIs["RestartSymbolOuterCircle"].GetRect().w,self.UIs["RestartSymbolOuterCircle"].GetRect().h))*-0.5)
        self.UIs["RestartSymbolInnerCircle"]  = UI(Circle, UI.RealPosToPercent(Vector2(*self.UIs["RestartSymbolBackground"].GetRect().center)), self.UIs["RestartSymbolOuterCircle"].GetSizePercent()-Vector2(2,2), (50,50,50))
        self.UIs["RestartSymbolInnerCircle"].MoveAdd(UI.RealSizeToPercent(Vector2(self.UIs["RestartSymbolInnerCircle"].GetRect().w,self.UIs["RestartSymbolInnerCircle"].GetRect().h))*-0.5)
        self.UIs["RestartSymbolInnerCircleBlock"]  = UI(Circle, UI.RealPosToPercent(Vector2(*self.UIs["RestartSymbolBackground"].GetRect().center)), self.UIs["RestartSymbolInnerCircle"].GetSizePercent()-Vector2(2,2), (50,50,50))
        self.UIs["RestartSymbolInnerCircleBlock"].MoveAdd((UI.RealSizeToPercent(Vector2(self.UIs["RestartSymbolInnerCircleBlock"].GetRect().w,self.UIs["RestartSymbolInnerCircleBlock"].GetRect().h))*-0.5)-Vector2(2,2))
        self.UIs["RestartSymbolInnerSquare"]  = UI(Quad, UI.RealPosToPercent(Vector2(*self.UIs["RestartSymbolInnerCircleBlock"].GetRect().center)), Vector2(1,2), (0,0,255))
        self.UIs["RestartSymbolInnerSquare"].MoveAdd((UI.RealSizeToPercent(Vector2(self.UIs["RestartSymbolInnerSquare"].GetRect().w,self.UIs["RestartSymbolInnerSquare"].GetRect().h))*-0.5)+Vector2(1,-0.75))
        
        backgroundSize = Vector2(80,40)
        self.UIs["OptionsBackground"] = UI(Quad, Vector2((UI.GetEdgeXPercentage()/2)-(backgroundSize.x/2), (UI.GetEdgeYPercentage()/2)-(backgroundSize.y/2)) + Vector2(0, 10), backgroundSize, (100,100,100))
        self.UIs["PlayForeground"] = UI(Quad, self.UIs["OptionsBackground"].GetPosPercent() + Vector2(1,1), Vector2(self.UIs["OptionsBackground"].GetSizePercent().x, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(2,2), (50,50,50))
        self.UIs["SettingsForeground"] = UI(Quad, self.UIs["PlayForeground"].GetPosPercent() + Vector2(0, self.UIs["PlayForeground"].GetSizePercent().y+1), Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2)+1, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(2,1), (50,50,50))
        self.UIs["AboutForeground"] = UI(Quad, self.UIs["SettingsForeground"].GetPosPercent() + Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2), 0), Vector2((self.UIs["OptionsBackground"].GetSizePercent().x/2)-1, self.UIs["OptionsBackground"].GetSizePercent().y/2) - Vector2(1,1), (50,50,50))
        
        self.UIs["PlayText"] = Text("Play", UI.RealPosToPercent(Vector2(*self.UIs["PlayForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["PlayText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["PlayText"].GetRect().size))/2)*-1)
        self.UIs["SettingsText"] = Text("Settings", UI.RealPosToPercent(Vector2(*self.UIs["SettingsForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["SettingsText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["SettingsText"].GetRect().size))/2)*-1)
        self.UIs["AboutText"] = Text("About", UI.RealPosToPercent(Vector2(*self.UIs["AboutForeground"].GetRect().center)), 30, (255,255,255))
        self.UIs["AboutText"].MoveAdd((UI.RealSizeToPercent(Vector2(*self.UIs["AboutText"].GetRect().size))/2)*-1)
        # * THIS IS FUCKING MAGICAL CODE THAT FIGURES THE CENTRE OF A TEXT ELEMENT, DO NOT CHANGE.
        # sorry for swearing.
        
        self.UIs["RuleNameText"] = Text(self.presetName, Vector2(2,2), 8, (255,255,255))
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
        self.UIs["NameText"] = Text("The Games Of Life", Vector2(UI.GetEdgeXPercentage()/2,UI.GetEdgeYPercentage()/4), 40, (255,255,255), bgColor=(0,0,0,255))
        self.UIs["NameText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["NameText"].GetRect().size))*-0.5)
        
        self.CreateGrid()
        
    def Stop(self):
        if self.looping:
            self.looping = False