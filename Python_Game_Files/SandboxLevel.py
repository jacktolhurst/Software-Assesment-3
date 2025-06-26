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
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        
        self.looping = False
        self.isPlaying = False
        self.skipGeneration = False
        
        self.tickSpeed = 9
        
        self.gridSize = gridSize
        self.grid = Grid(GridAttributes(), gridSize)
        
        self.clock = pygame.time.Clock()
        
        self.generation = 0
        
        self.UIs = {}
        
        self.FPSList = []
        
        
        self.Start()
    
    def Start(self):
        if not self.looping:
            con.CURRSCREEN = self
            
            self.UIs["SymbolBackground"] = UI(Quad, Vector2(1,1), Vector2(23,12), (100,100,100))
            self.UIs["PlaySymbolBackground"] = UI(Quad, Vector2(2,2), Vector2(10,10), (50,50,50))
            self.UIs["PlaySymbol"] = UI(TriangleRight, self.UIs["PlaySymbolBackground"].GetPosPercent()+Vector2(1.5,1.5), self.UIs["PlaySymbolBackground"].GetSizePercent()-Vector2(3,3), (0,255,0))
            self.UIs["SkipSymbolBackground"] = UI(Quad, Vector2(13,2), Vector2(10,10), (50,50,50))
            self.UIs["SkipSymbolTriangle"] = UI(TriangleRight, self.UIs["SkipSymbolBackground"].GetPosPercent()+Vector2(1.5,1.5), self.UIs["SkipSymbolBackground"].GetSizePercent()-Vector2(3,3), (200,255,200))
            self.UIs["SkipSymbolSquare"] = UI(Quad, self.UIs["SkipSymbolTriangle"].GetPosPercent()+Vector2(6,0), Vector2(1.5,7), (200,255,200))
            self.UIs["SliderSquare"] = UI(Quad, Vector2(52, 90), Vector2(46,7.5), (100,100,100))
            self.UIs["SliderBackground"] = UI(Quad, Vector2(55,91.25), Vector2(40,5), (50,50,50))
            self.UIs["SliderNotch"] = UI(Circle, Vector2(55,91.25), Vector2(5,5), (255,255,255))
            
            self.UIs["SliderText"] = Text("TickSpeed", 'freesansbold.ttf', Vector2(53,87), 10, (255,255,255))
            self.UIs["FPSCount"] = Text("FPS", 'freesansbold.ttf', Vector2(100,90), 10, (255,255,255))
            self.UIs["AverageCount"] = Text("Average", 'freesansbold.ttf', Vector2(100,95), 10, (255,255,255))
            self.UIs["UnstableWarning"] = Text("Unstable!", 'freesansbold.ttf', Vector2(85,87), 10, (255,0,0), False)
            self.UIs["GenerationCount"] = Text("Generation: 0", 'freesansbold.ttf', Vector2(120,95), 10, (255,255,255))
            
            self.looping = True
            self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()       
        
        prevMousePos = None
        
        touchingSlider = False

        while self.looping:    
            if self.skipGeneration:
                self.isPlaying = False
                self.skipGeneration = False
            
            if self.isPlaying:
                self.UIs["PlaySymbol"].ChangeColor((255,0,0))
                self.UIs["PlaySymbol"].ChangeShape(Hexagon)
            else:
                self.UIs["PlaySymbol"].ChangeColor((0,255,0))
                self.UIs["PlaySymbol"].ChangeShape(TriangleRight)
            
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEWHEEL:
                    if 0 < con.CELLSIZE + event.y < 100:
                        con.CELLSIZE += event.y
                        self.grid.MoveCells()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_s:
                        settingsMenu = SettingsMenu()
                    if event.key == pygame.K_q:
                        self.Stop()
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.UIs["SliderNotch"].CheckCollidePoint(mousePos):
                        touchingSlider = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.UIs["PlaySymbolBackground"].CheckCollidePoint(mousePos):
                        self.isPlaying = not self.isPlaying
                    if self.UIs["SkipSymbolBackground"].CheckCollidePoint(mousePos):
                        self.skipGeneration = True
                        self.isPlaying = True
                    
                    if event.button == 1: 
                        touchingSlider = False
                
                if event.type == QUIT:
                    con.HANDLER.QuitGame()
                
            if pygame.mouse.get_pressed()[0]:
                if touchingSlider:
                    newSliderPos = UI.RealPosToPercent(Vector2(mousePos[0], mousePos[1]))
                    newSliderPos.y = self.UIs["SliderNotch"].GetPosPercent().y
                    newSliderPos.x = con.HANDLER.Clamp(newSliderPos.x, 53, 92)
                    
                    self.tickSpeed = (newSliderPos.x - 52) * 1.5
                    
                    self.UIs["SliderNotch"].MoveSet(newSliderPos)
                    self.UIs["SliderNotch"].ChangeColor((255,min(255-((newSliderPos.x-85)*8),255),min(255-((newSliderPos.x-85)*8),255)))
                
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

            if self.isPlaying and elapsedTime >= (1000 / self.tickSpeed):
                self.grid.Update()
                
                self.generation += 1
                self.UIs["GenerationCount"].ChangeText("Generation: " + str(self.generation))
                
                lastUpdateTime = currTime

            self.UIs["SliderText"].ChangeText("Tickspeed: " + str(int(self.tickSpeed)))
            
            currFPS = int(self.clock.get_fps())
            self.FPSList.insert(0,int(currFPS))
            self.FPSList = self.FPSList[:100]
            self.UIs["FPSCount"].ChangeText("FPS: " + str(currFPS))
            self.UIs["AverageCount"].ChangeText("Average: " + str(int(sum(self.FPSList) / len(self.FPSList))))
            
            if currFPS <= self.tickSpeed and self.isPlaying or self.tickSpeed >= 50:
                self.UIs["UnstableWarning"].SetState(True)
            else:
                self.UIs["UnstableWarning"].SetState(False)

            self.DrawEverything()
            pygame.display.update()
            
            prevMousePos = mousePos
            
            self.clock.tick(120)

    def DrawEverything(self):
        con.SCREEN.fill((50,0,0))
        
        self.grid.DrawCells()
        
        con.HANDLER.DrawUI(self, self.UIs)
    
    def ResetScreen(self):
        self.grid.MoveCells()

    def Stop(self):
        if self.looping:
            self.looping = False