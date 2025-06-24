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
        self.looping = False
        self.isPlaying = False
        
        self.tickSpeed = 9
        
        self.gridSize = gridSize
        self.grid = Grid(GridAttributes(), gridSize)
        
        self.clock = pygame.time.Clock()
        
        self.UIs = {}
        
        self.Start()
    
    def Start(self):
        if not self.looping:
            con.CURRSCREEN = self
            
            self.UIs["PlayStopSquare"] = UI(Quad, Vector2(1,1), Vector2(20,20), (100,100,100))
            self.UIs["PlaySymbol"] = UI(TriangleRight, Vector2(6,6), Vector2(10,10), (0,255,0))
            self.UIs["SliderSquare"] = UI(Quad, Vector2(52.5,90), Vector2(45,7.5), (100,100,100))
            self.UIs["SliderBackground"] = UI(Quad, Vector2(55,91.25), Vector2(40,5), (50,50,50))
            self.UIs["SliderNotch"] = UI(Circle, Vector2(55,91.25), Vector2(5,5), (255,255,255))
            self.UIs["SliderText"] = Text("TickSpeed", 'freesansbold.ttf', Vector2(930,1000), 20, (255,255,255))
            
            self.looping = True
            self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()       
        
        prevMousePos = None
        
        touchingSlider = False
        
    
        while self.looping:
            if con.WON:
                self.Won()
            
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
                    if self.UIs["SliderNotch"].rect.collidepoint(mousePos):
                        touchingSlider = True
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.UIs["PlaySymbol"].rect.collidepoint(mousePos):
                        self.isPlaying = not self.isPlaying
                        
                    if not self.UIs["SliderNotch"].rect.collidepoint(mousePos):
                        touchingSlider = False
                
                if event.type == QUIT:
                    con.HANDLER.QuitGame()

            keys = pygame.key.get_pressed()            
            if pygame.mouse.get_pressed()[0]:
                if touchingSlider:
                    if not mousePos[0] <= 885 and not  mousePos[0] >= 1235:
                        self.UIs["SliderNotch"].MoveSet(Vector2(mousePos[0], self.UIs["SliderNotch"].GetPos().y))
                        self.tickSpeed = clamp((self.UIs["SliderNotch"].GetPos().x - 880)/5, 1, 120)
                UIRects = [ui.rect for ui in self.UIs.values() if ui.state]
                if not any(rect.collidepoint(mousePos) for rect in UIRects):
                    self.grid.ClickIntersection(mousePos, State.ALIVE)
            if pygame.mouse.get_pressed()[1]:
                con.CELLOFFSETT = con.CELLOFFSETT + Vector2(tuple(numpy.subtract(mousePos, prevMousePos)))
                self.grid.MoveCells()
            if pygame.mouse.get_pressed()[2]:
                self.grid.ClickIntersection(mousePos, State.DEAD)

            if self.isPlaying and elapsedTime >= (1000 / self.tickSpeed):
                self.grid.Update()
                lastUpdateTime = currTime

            self.UIs["SliderText"].ChangeText("Tickspeed: " + str(int(self.tickSpeed)))

            self.DrawEverything()
            pygame.display.update()
            
            prevMousePos = mousePos
            
            self.clock.tick(120)

    def DrawEverything(self):
        con.SCREEN.fill((0,0,0))
        
        self.grid.DrawCells()
        
        for Name, UI in self.UIs.items():
            if UI.state:
                UI.Draw()
    
    def ResetScreen(self):
        self.grid.MoveCells()

    def Stop(self):
        if self.looping:
            self.looping = False
    
    def Won(self):
        con.Won = False
        self.Stop()