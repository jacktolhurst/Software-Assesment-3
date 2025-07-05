import numpy
import pygame
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from Grid import Grid, GridAttributes
from Cell import State
from Settings import SettingsMenu
from UI import *
from Text import *

class SandBoxLVL():
    def __init__(self, gridSize:Vector2):
        self.gridSize = gridSize
        
        self.gridAttributes = GridAttributes()
        
        self.currCursor = None
        
        self.Setup()
        self.Start()
        
    def Setup(self):
        self.looping = False
        self.isPlaying = False
        self.skipGeneration = False
        
        self.tickSpeed = 10
        
        con.CELLOFFSETT = Vector2(0,0)
        con.CELLSIZE = 20

        self.grid = Grid(self.gridAttributes)
        
        self.clock = pygame.time.Clock()
        
        self.generation = 0
        
        self.UIs = {}
        self.underAndItems = {}
    
    def Start(self):
        if not self.looping:
            con.CURRSCREEN = self
            
            self.UIs["SymbolBackground"] = UI(Quad, Vector2(1,1), Vector2(34,12), (100,100,100))
            self.UIs["PlaySymbolBackground"] = UI(Quad, Vector2(2,2), Vector2(10,10), (50,50,50))
            self.UIs["PlaySymbol"] = UI(TriangleRight, self.UIs["PlaySymbolBackground"].GetPosPercent()+Vector2(1.5,1.5), self.UIs["PlaySymbolBackground"].GetSizePercent()-Vector2(3,3), (0,255,0))
            self.UIs["SkipSymbolBackground"] = UI(Quad, Vector2(13,2), Vector2(10,10), (50,50,50))
            self.UIs["SkipSymbolTriangle"] = UI(TriangleRight, self.UIs["SkipSymbolBackground"].GetPosPercent()+Vector2(1.5,1.5), self.UIs["SkipSymbolBackground"].GetSizePercent()-Vector2(3,3), (200,255,200))
            self.UIs["SkipSymbolSquare"] = UI(Quad, self.UIs["SkipSymbolTriangle"].GetPosPercent()+Vector2(6,0), Vector2(1.5,7), (200,255,200))
            self.UIs["RestartSymbolBackground"] = UI(Quad, Vector2(24,2), Vector2(10,10), (50,50,50))
            self.UIs["RestartSymbolOuter"] = UI(Circle, self.UIs["RestartSymbolBackground"].GetPosPercent()+Vector2(1,1), self.UIs["RestartSymbolBackground"].GetSizePercent()-Vector2(2,2), (0,0,255))
            self.UIs["RestartSymbolInner"] = UI(Circle, self.UIs["RestartSymbolBackground"].GetPosPercent()+Vector2(2,2), self.UIs["RestartSymbolBackground"].GetSizePercent()-Vector2(4,4), self.UIs["RestartSymbolBackground"].GetColor())
            self.UIs["RestartSymbolInnerCircle"] = UI(Circle, self.UIs["RestartSymbolBackground"].GetPosPercent()+Vector2(2,0), self.UIs["RestartSymbolBackground"].GetSizePercent()-Vector2(7,6), self.UIs["RestartSymbolBackground"].GetColor())
            self.UIs["RestartSymbolOuterSquare"] = UI(Quad, self.UIs["RestartSymbolBackground"].GetPosPercent()+Vector2(4,0.25), Vector2(1,2.5), self.UIs["RestartSymbolOuter"].GetColor())
            self.UIs["SliderSquare"] = UI(Quad, Vector2(52, 90), Vector2(46,7.5), (100,100,100))
            self.UIs["SliderBackground"] = UI(Quad, Vector2(55,91.25), Vector2(40,5), (50,50,50))
            self.UIs["SliderNotch"] = UI(Circle, Vector2(60,91.25), Vector2(5,5), (255,255,255))
            self.UIs["SettingsBackgroundOuter"] = UI(Quad, Vector2(UI.GetEdgeXPercentage()-13, self.UIs["SymbolBackground"].GetPosPercent().y), Vector2(12,12), (100,100,100))
            self.UIs["SettingsBackgroundInner"] = UI(Quad, self.UIs["SettingsBackgroundOuter"].GetPosPercent()+Vector2(1,1), self.UIs["SettingsBackgroundOuter"].GetSizePercent()-Vector2(2,2), (50,50,50))
            self.UIs["SettingscircleOuter"] = UI(Circle, self.UIs["SettingsBackgroundOuter"].GetPosPercent()+Vector2(2,2), self.UIs["SettingsBackgroundOuter"].GetSizePercent()-Vector2(4,4), (75,75,75))
            self.UIs["SettingscircleInner"] = UI(Circle, self.UIs["SettingsBackgroundOuter"].GetPosPercent()+Vector2(3,3), self.UIs["SettingsBackgroundOuter"].GetSizePercent()-Vector2(6,6), (50,50,50))
            
            self.UIs["SliderText"] = Text("TickSpeed", Vector2(53,87), 10, (255,255,255))
            self.UIs["FPSCount"] = Text("FPS", Vector2(1,95), 10, (255,255,255))
            self.UIs["UnstableWarning"] = Text("Unstable!", Vector2(85,87), 10, (255,0,0))
            
            self.UIs["GenerationCount"] = Text("Generation: 0", Vector2(1,13), 10, (255,255,255)) 
            
            self.underAndItems = self.GetUnderItems()
            
            
            self.looping = True
            self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()       
        
        prevMousePos = None
        
        touchingSlider = False

        while self.looping:    
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()

            
            if self.UIs["PlaySymbolBackground"].CheckCollidePoint(mousePos) or self.UIs["SkipSymbolBackground"].CheckCollidePoint(mousePos) or self.UIs["RestartSymbolBackground"].CheckCollidePoint(mousePos) or self.UIs["SliderNotch"].CheckCollidePoint(mousePos) or self.UIs["SettingsBackgroundInner"].CheckCollidePoint(mousePos):
                desired = con.HANDCURSOR
            else:
                desired = con.ARROWCURSOR
            
            if desired is not self.currCursor:
                    pygame.mouse.set_cursor(desired)
                    self.currCursor = desired
            
            if self.skipGeneration:
                self.isPlaying = False
                self.skipGeneration = False
            
            if self.isPlaying:
                self.UIs["PlaySymbol"].ChangeColor((255,0,0))
                self.UIs["PlaySymbol"].ChangeShape(Hexagon)
            else:
                self.UIs["PlaySymbol"].ChangeColor((0,255,0))
                self.UIs["PlaySymbol"].ChangeShape(TriangleRight)
            
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    if 0 < con.CELLSIZE + event.y < 100:
                        con.CELLSIZE += event.y
                        self.grid.MoveCells()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_q:
                        self.Stop()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.UIs["SliderNotch"].CheckCollidePoint(mousePos):
                        touchingSlider = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.UIs["PlaySymbolBackground"].CheckCollidePoint(mousePos):
                        self.isPlaying = not self.isPlaying
                    elif self.UIs["SkipSymbolBackground"].CheckCollidePoint(mousePos):
                        self.skipGeneration = True
                        self.isPlaying = True
                    elif self.UIs["RestartSymbolBackground"].CheckCollidePoint(mousePos):
                        self.Restart()
                        pygame.time.wait(10)
                        return
                    elif self.UIs["SettingsBackgroundInner"].CheckCollidePoint(mousePos):
                        settingsMenu = SettingsMenu(self.grid.GetGridAttributes())
                        self.gridAttributes = settingsMenu.Start()
                        settingsMenu = None
                        self.Restart()
                    
                    if event.button == 1: 
                        touchingSlider = False
                
                if event.type == QUIT:
                    con.HANDLER.QuitGame()
                
            if pygame.mouse.get_pressed()[0]:
                if touchingSlider:
                    newSliderPos = UI.RealPosToPercent(Vector2(mousePos[0], mousePos[1]))

                    newSliderPos.y = self.UIs["SliderNotch"].GetPosPercent().y

                    notchHalfWPercent = self.UIs["SliderNotch"].GetSizePercent().x / 2
                    newSliderPos.x -= notchHalfWPercent 

                    newSliderPos.x = con.HANDLER.Clamp(newSliderPos.x, 53, 92)

                    self.UIs["SliderNotch"].MoveSet(newSliderPos)
                    self.UIs["SliderNotch"].ChangeColor((255,min(255-((newSliderPos.x-80)*20),255),min(255-((newSliderPos.x-80)*20),255)))
                    
                    self.tickSpeed = (self.UIs["SliderNotch"].GetPosPercent().x-52)*1.5
                
                UIRects = [ui.GetRect() for ui in self.UIs.values() if ui.state]
                if not any(rect.collidepoint(mousePos) for rect in UIRects) and not touchingSlider:
                    if  self.isPlaying:
                        if abs((con.HANDLER.TupleMagnitude(mousePos) - con.HANDLER.TupleMagnitude(prevMousePos))) < 50-self.tickSpeed:
                            self.grid.ClickIntersection(mousePos, State.ALIVE)
                    else:
                        self.grid.ClickIntersection(mousePos, State.ALIVE)
            
            if pygame.mouse.get_pressed()[1]:
                con.CELLOFFSETT = con.CELLOFFSETT + Vector2(tuple(numpy.subtract(mousePos, prevMousePos)))
                self.grid.MoveCells()
            if pygame.mouse.get_pressed()[2]:
                self.grid.ClickIntersection(mousePos, State.DEAD)
            
            for under, uiList in self.underAndItems.items():
                for ui in uiList:
                    if ui.CheckCollidePoint(mousePos):
                        under.MoveSet(UI.RealPosToPercent(Vector2(*mousePos))+Vector2(1,1))
                        under.SetState(True)
                        break
                    else:
                        under.SetState(False)

            if self.isPlaying and elapsedTime >= (1000 / self.tickSpeed):
                self.grid.Update()
                
                self.generation += 1
                self.UIs["GenerationCount"].ChangeText("Generation: " + str(self.generation))
                
                lastUpdateTime = currTime

            self.UIs["SliderText"].ChangeText("Tickspeed: " + str(int(self.tickSpeed)))
            
            currFPS = int(self.clock.get_fps())
            self.UIs["FPSCount"].ChangeText("FPS: " + str(currFPS))
            
            if currFPS <= self.tickSpeed and self.isPlaying or self.tickSpeed >= 50:
                self.UIs["UnstableWarning"].SetState(True)
            else:
                self.UIs["UnstableWarning"].SetState(False)
            

            self.DrawEverything()
            
            prevMousePos = mousePos
            
            self.clock.tick(120)

    def DrawEverything(self):
        con.SCREEN.fill((50,0,0))
        
        self.grid.DrawCells()
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
        
    def GetUnderItems(self) -> dict:
        underItems = {}
        
        for ui in self.UIs.values():
            under = ui.GetUnderItem() 
            if under is not None:
                if under not in underItems:
                    underItems[under] = []
                underItems[under].append(ui)
        
        return underItems
    
    def ResetScreen(self):
        self.grid.MoveCells()
    
    def Restart(self):
        self.looping = False
        self.Setup()
        self.Start()

    def Stop(self):
        self.looping = False