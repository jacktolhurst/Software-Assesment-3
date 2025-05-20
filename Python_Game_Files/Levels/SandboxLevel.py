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
            self.UIs["SliderBackground"] = UI(Quad, Vector2(500,500), Vector2(100,100), (20,20,20))
            
            self.looping = True
            self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()
        
        prevMousePos = None
    
        while self.looping:
            if con.WON:
                self.Won()
            
            if self.isPlaying:
                self.UIs["StopSymbol"].state = True
                self.UIs["PlaySymbol"].state = False
            else:
                self.UIs["StopSymbol"].state = False
                self.UIs["PlaySymbol"].state = True
            
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_q:
                        self.Stop()
                if event.type == pygame.MOUSEBUTTONUP:
                    for Name, UI in self.UIs.items():
                        if not UI.state:
                            continue
                        if Name == "PlaySymbol" and UI.rect.collidepoint(mousePos):
                            self.isPlaying = True
                        elif Name == "StopSymbol" and UI.rect.collidepoint(mousePos):
                            self.isPlaying = False
                if event.type == QUIT:
                    con.HANDLER.QuitGame()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                self.grid.SetCell(Vector2(random.randrange(len(self.grid.cells)-1), random.randrange(len(self.grid.cells[0])-1)), State.UNTOUCH)
            if keys[pygame.K_w]:
                self.tickSpeed = min(self.tickSpeed + 0.1, 120)
            if keys[pygame.K_s]:
                self.tickSpeed = max(1, self.tickSpeed - 0.1)
            
            if pygame.mouse.get_pressed()[0]:
                if not self.isPlaying:
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