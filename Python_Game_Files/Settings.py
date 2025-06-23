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
                self.UIs["InputText"] = InputText("test", 'freesansbold.ttf', Vector2(900,800), 30, (255,255,255), (100,100,100))
                
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
                        
                        if inputText != None:
                            userText = inputText.GetText()
                            if event.key == pygame.K_BACKSPACE:
                                userText = userText[:-1]
                            elif event.unicode.isdigit() and (len(userText)+1) < 3:
                                userText += event.unicode
                            inputText.ChangeText(userText)
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        if inputText != None:
                            if not inputText.ClickIntersection(mousePos):
                                inputText = None
                        else:
                            if self.UIs["InputText"].ClickIntersection(mousePos):
                                inputText = self.UIs["InputText"]
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                
                self.DrawEverything()
                
                self.clock.tick(120)
        
        def DrawEverything(self):
            con.SCREEN.fill((0,0,0))

            for Name, UI in self.UIs.items():
                if UI.state:
                    UI.Draw()

            pygame.display.update()
        
        def Stop(self):
            if self.looping:
                self.looping = False