import pygame
import numpy
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *

class SettingsMenu():
        def __init__(self):
            self.looping = False
            self.UIs = {}
            self.inputUIs = {}
            self.inputNumUIs = {}
            
            self.clock = pygame.time.Clock()
            
            self.FPSList = []
            
            self.Start()
        
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                self.UIs["InputText"] = Text("test", 'freesansbold.ttf', Vector2(1,1), 30, (255,255,255), (20,30,40,255))
                self.UIs["InputText2"] = Text("12", 'freesansbold.ttf', Vector2(1,11), 30, (255,255,255), (20,30,40,255), 4, True)
                self.UIs["FPSCount"] = Text("FPS", 'freesansbold.ttf', Vector2(100,90), 10, (255,255,255))
                self.UIs["AverageCount"] = Text("Average", 'freesansbold.ttf', Vector2(100,95), 10, (255,255,255))
                
                self.inputUIs = {name: ui for name, ui in self.UIs.items() if name.startswith("Input")}
                
                self.looping = True
                
                self.Update()
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q and inputText is None:
                            self.Stop()
                        
                        if event.key == pygame.K_BACKSPACE:
                            inputText.ChangeText(inputText.GetText()[:-1])
                        elif inputText is not None:
                            inputText.ChangeText(inputText.GetText() + event.unicode)
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        for ui in self.inputUIs.values():
                            ui.ChangeBgColor(ui.GetInitialBgColor())

                        selected = next(
                            (ui for ui in self.inputUIs.values() if ui.CheckCollidePoint(mousePos)),
                            None
                        )

                        if selected:
                            selected.ChangeBgColor(con.SELECTEDUICOLOR)
                            inputText = selected
                        else:
                            inputText = None
                    
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                
                
                currFPS = int(self.clock.get_fps())
                self.FPSList.insert(0,int(currFPS))
                self.FPSList = self.FPSList[:100]
                self.UIs["FPSCount"].ChangeText("FPS: " + str(currFPS))
                self.UIs["AverageCount"].ChangeText("Average: " + str(int(sum(self.FPSList) / len(self.FPSList))))
                
                self.DrawEverything()
                pygame.display.update()
                
                self.clock.tick(120)
        
        def DrawEverything(self):
            con.SCREEN.fill((200,0,0))
            
            con.HANDLER.DrawUI(self, self.UIs)
        
        def ResetScreen(self):
            pass
        
        def Stop(self):
            if self.looping:
                self.looping = False