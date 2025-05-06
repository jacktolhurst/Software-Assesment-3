import sys
import pygame
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from Grid import Grid

class SandBoxLVL():
    def __init__(self):
        self.looping = False
        self.isPlaying = False
        
        self.playTickSpeed = 10
        self.stoppedTickSpeed = 60
        
        self.grid = Grid(con.CELLAMOUNT)
        
        self.clock = pygame.time.Clock()
    
    def Start(self):
        if not self.looping:
            self.looping = True
            self.Update()
    
    def Update(self):
        while self.looping:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                self.grid.SetCell(Vector2(random.randrange(len(self.grid.cells)-1),random.randrange(len(self.grid.cells[0])-1)), True)
            
            for event in pygame.event.get() :
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.isPlaying = not self.isPlaying
                    if event.key == pygame.K_w:
                        self.playTickSpeed = self.playTickSpeed + 2
                    if event.key == pygame.K_s:
                        self.playTickSpeed = max(1, self.playTickSpeed - 2)
                    if event.key == pygame.K_q:
                        self.Stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.isPlaying:
                            mousePos = pygame.mouse.get_pos()
                            self.grid.ClickIntersection(mousePos)
                if event.type == QUIT:
                    con.HANDLER.QuitGame()
            
            if self.isPlaying:
                self.grid.Update()
            
            if self.isPlaying:
                con.SCREEN.fill(con.BACKGROUNDCOLORPLAY)
            else:
                con.SCREEN.fill(con.BACKGROUNDCOLORSTOPPED)
            
            self.grid.DrawCells()
            
            pygame.display.update()
            if self.isPlaying:
                self.clock.tick(self.playTickSpeed)
            else:
                self.clock.tick(self.stoppedTickSpeed)
        
    def Stop(self):
        if self.looping:
            self.looping = False