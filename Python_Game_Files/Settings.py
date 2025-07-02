import pygame
import numpy
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import GridAttributes

class SettingsMenu():
        def __init__(self, currentGridAttributes:GridAttributes=None):
            self.looping = False
            self.UIs = {}
            self.inputUIs = {}
            self.inputNumUIs = {}
            
            self.clock = pygame.time.Clock()
            
            if currentGridAttributes == None:
                self.gridAttributes = GridAttributes()
            else:
                self.gridAttributes = currentGridAttributes
            
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                self.UIs["GridSizeText"] = Text("Grid Size:", 'freesansbold.ttf', Vector2(2,5), 15, (255,255,255))
                self.UIs["InputGridSize"] = Text(str(int(self.gridAttributes.gridSize.x)), 'freesansbold.ttf', self.UIs["GridSizeText"].GetPosPercent()+Vector2(19,0), 15, (255,255,255), (20,30,40,255), 3, True)
                self.UIs["GridSizeInfo"] = Text("The size of the grid.", 'freesansbold.ttf', Vector2(0,0), 10, (120,120,120), (70,70,70,255), 100, False, False)
                
                self.UIs["InputAliveCount"] = Text("12", 'freesansbold.ttf', Vector2(1,11), 30, (255,255,255), (20,30,40,255), 4, True)
                
                self.UIs["FPSCount"] = Text("FPS", 'freesansbold.ttf', Vector2(100,90), 10, (255,255,255))
                
                self.UIs["QuitButton"] = UI(Circle, Vector2(165,87.5), Vector2(10,10), (255,0,0))
                self.UIs["QuitButtonText"] = Text("Quit", 'freesansbold.ttf', self.UIs["QuitButton"].GetPosPercent()+Vector2(2.4,3.75), 10, (0,0,0))
                
                self.inputUIs = {name: ui for name, ui in self.UIs.items() if name.startswith("Input")}
                
                self.looping = True
                
                self.Update()
                
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                
                try:
                    gridSize = int(self.UIs["InputGridSize"].GetText())
                    self.gridAttributes.gridSize = Vector2(gridSize,gridSize)
                except:
                    self.UIs["Error"] = Text("An Error Occured",'freesansbold.ttf', Vector2(50,80), 30, (255,0,0), (0,0,0,255))
                    self.DrawEverything()
                    pygame.time.wait(1000)
                
                
                return self.gridAttributes
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                mousePosV2 = con.HANDLER.TupleToVector2(mousePos)
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q and inputText is None:
                            self.Stop()
                        
                        if inputText is not None:                            
                            if event.key == pygame.K_BACKSPACE:
                                inputText.ChangeText(inputText.GetText()[:-1])
                            elif event.key == pygame.K_DELETE:
                                inputText.ChangeText(inputText.GetText()[:-1])
                            elif event.key == pygame.K_RETURN:
                                inputText.ChangeBgColor(inputText.GetInitialBgColor())
                                inputText = None
                            else:
                                inputText.ChangeText(inputText.GetText() + event.unicode)
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.UIs["QuitButton"].CheckCollidePoint(mousePos):
                            self.Stop()
                        else:
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
                                
                if inputText is not None:
                    cursor = pygame.cursors.compile(pygame.cursors.textmarker_strings)
                    pygame.mouse.set_cursor((8, 16), (0, 0), *cursor)
                elif self.UIs["GridSizeText"].CheckCollidePoint(mousePos) or self.UIs["InputGridSize"].CheckCollidePoint(mousePos):
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    self.UIs["GridSizeInfo"].MoveSet(UI.RealPosToPercent(mousePosV2))
                    self.UIs["GridSizeInfo"].SetState(True)
                else:
                    self.UIs["GridSizeInfo"].SetState(False)
                
                
                if self.UIs["QuitButton"].CheckCollidePoint(mousePos):
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                
                currFPS = int(self.clock.get_fps())
                self.UIs["FPSCount"].ChangeText("FPS: " + str(currFPS))
                
                self.DrawEverything()
                
                self.clock.tick(120)
        
        def DrawEverything(self):
            con.SCREEN.fill((0,0,255))
            
            con.HANDLER.DrawUI(self, self.UIs)
            
            pygame.display.update()
        
        def ResetScreen(self):
            pass
        
        def Stop(self):
            if self.looping:
                self.looping = False