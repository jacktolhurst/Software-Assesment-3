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

class About():
    def __init__(self):
        self.looping = False
        
        self.UIs = {}
        
        self.currCursor = None
        
        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.ResetScreen()
        
        self.Update()
    
    def Update(self):
        while self.looping:
            currTime = pygame.time.get_ticks()

            mousePos = pygame.mouse.get_pos()
            
            if self.UIs["ExitText"].CheckCollidePoint(mousePos):
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
                        pass
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
    
    def ResetScreen(self):
        self.UIs["test"] = Text("This is the first line \n This is the second line \n This is the third line", Vector2(10,10), 30, (255,255,255))
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
    def Stop(self):
        if self.looping:
            self.looping = False