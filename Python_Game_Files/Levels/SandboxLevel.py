import numpy
import pygame
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from Grid import Grid
from Cell import State
from UI import *

class SandBoxLVL():
    def __init__(self):
        self.looping = False
        self.isPlaying = False
        
        self.tickSpeed = 10
        
        self.grid = Grid(con.CELLAMOUNT)
        
        self.clock = pygame.time.Clock()
        
        self.UIs = {}
        
        self.Start()
    
    def Start(self):
        if not self.looping:
            self.UIs["PlayStopSquare"] = UI(Quad, Vector2(20,20), Vector2(200,200), (100,100,100))
            self.UIs["StopSymbol"] = UI(Hexagon, Vector2(70,70), Vector2(100,100), (255,0,0), False)
            self.UIs["PlaySymbol"] = UI(TriangleRight, Vector2(70,70), Vector2(100,100), (0,255,0), False)
            self.UIs["SliderSquare"] = UI(Quad, Vector2(880,1020), Vector2(400,50), (100,100,100))
            self.UIs["SliderBackground"] = UI(Quad, Vector2(905,1025), Vector2(350,40), (50,50,50))
            self.UIs["SliderNotch"] = UI(Circle, Vector2(900,1025), Vector2(40,40), (255,255,255))
            
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
                self.UIs["StopSymbol"].SetState(True)
                self.UIs["PlaySymbol"].SetState(False)
            else:
                self.UIs["StopSymbol"].SetState(False)
                self.UIs["PlaySymbol"].SetState(True) 
            
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_q:
                        self.Stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.UIs["SliderNotch"].rect.collidepoint(mousePos):
                        touchingSlider = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.UIs["PlaySymbol"].rect.collidepoint(mousePos) and self.UIs["PlaySymbol"].state:
                        self.isPlaying = True
                    elif self.UIs["StopSymbol"].rect.collidepoint(mousePos) and self.UIs["StopSymbol"].state:
                        self.isPlaying = False
                    
                    if not self.UIs["SliderNotch"].rect.collidepoint(mousePos):
                        touchingSlider = False
                if event.type == QUIT:
                    con.HANDLER.QuitGame()

            keys = pygame.key.get_pressed()            
            if pygame.mouse.get_pressed()[0]:
                if touchingSlider:
                    if not mousePos[0] <= 885 and not  mousePos[0] >= 1235:
                        self.UIs["SliderNotch"].MoveSet(Vector2(mousePos[0], self.UIs["SliderNotch"].pos.y))
                        self.tickSpeed = clamp((self.UIs["SliderNotch"].pos.x - 880)/5, 1, 120)
                elif not self.isPlaying:
                    self.grid.ClickIntersection(mousePos, State.ALIVE)
            if pygame.mouse.get_pressed()[1]:
                con.CELLOFFSETT = con.CELLOFFSETT + Vector2(tuple(numpy.subtract(mousePos, prevMousePos)))
                self.grid.MoveCells()
            if pygame.mouse.get_pressed()[2]:
                if not self.isPlaying:
                    self.grid.ClickIntersection(mousePos, State.DEAD)

            if self.isPlaying and elapsedTime >= (1000 / self.tickSpeed):
                self.grid.Update()
                lastUpdateTime = currTime


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
        
        pygame.display.update()

    def Stop(self):
        if self.looping:
            self.looping = False
    
    def Won(self):
        con.Won = False
        self.Stop()