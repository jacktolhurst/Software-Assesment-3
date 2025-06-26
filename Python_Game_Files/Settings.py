import pygame
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *

class SettingsMenu():
        def __init__(self):
            self.looping = False
            self.UIs = {}
            
            self.clock = pygame.time.Clock()
            
            self.Start()
        
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                self.UIs["InputText"] = InputText("test", 'freesansbold.ttf', Vector2(1,1), 30, (255,255,255), (100,100,100))
                
                self.looping = True
                
                self.Update()
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.Stop()
                            
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.UIs["InputText"].CheckCollidePoint(mousePos):
                            inputText = self.UIs["InputText"]
                    
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                
                self.DrawEverything()
                pygame.display.update()
                
                self.clock.tick(120)
        
        def DrawEverything(self):
            con.SCREEN.fill((0,0,0))
            
            con.HANDLER.DrawUI(self, self.UIs)
        
        def ResetScreen(self):
            pass
        
        def Stop(self):
            if self.looping:
                self.looping = False