import numpy
import pygame
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from Grid import Grid
from Cell import State

class SandBoxLVL():
    def __init__(self):
        self.looping = False
        self.isPlaying = False
        
        self.playTickSpeed = 10
        self.stoppedTickSpeed = 60
        
        self.grid = Grid(con.CELLAMOUNT)
        
        self.clock = pygame.time.Clock()
        
        self.Start()
    
    def Start(self):
        if not self.looping:
            self.looping = True
            self.Update()
    
    def Update(self):
        lastUpdateTime = pygame.time.get_ticks()
        
        prevMousePos = None
    
        while self.looping:
            if con.WON:
                self.Won()
            
            currTime = pygame.time.get_ticks()
            elapsedTime = currTime - lastUpdateTime
            
            mousePos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_w:
                        self.playTickSpeed += 2
                    if event.key == pygame.K_s:
                        self.playTickSpeed = max(1, self.playTickSpeed - 2)
                    if event.key == pygame.K_q:
                        self.Stop()
                if event.type == pygame.MOUSEWHEEL:
                    con.CELLSCALE += event.y
                    self.grid.MoveCells()
                if event.type == QUIT:
                    con.HANDLER.QuitGame()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                self.grid.SetCell(Vector2(random.randrange(len(self.grid.cells)-1), random.randrange(len(self.grid.cells[0])-1)), State.PRIZE)
            
            if pygame.mouse.get_pressed()[0]:
                if not self.isPlaying:
                    self.grid.ClickIntersection(mousePos, State.ALIVE)
            if pygame.mouse.get_pressed()[1]:
                con.CELLOFFSETT = con.CELLOFFSETT + Vector2(tuple(numpy.subtract(mousePos, prevMousePos)))
                self.grid.MoveCells()
            if pygame.mouse.get_pressed()[2]:
                if not self.isPlaying:
                    self.grid.ClickIntersection(mousePos, State.DEAD)

            if self.isPlaying and elapsedTime >= (1000 / self.playTickSpeed):
                self.grid.Update()
                lastUpdateTime = currTime

            if self.isPlaying:
                con.SCREEN.fill(con.BACKGROUNDCOLORPLAY)
            else:
                con.SCREEN.fill(con.BACKGROUNDCOLORSTOPPED)

            self.grid.DrawCells()
            pygame.display.update()
            
            prevMousePos = mousePos
            
            self.clock.tick(120)

    def Stop(self):
        if self.looping:
            self.looping = False
    
    def Won(self):
        con.Won = False
        self.Stop()