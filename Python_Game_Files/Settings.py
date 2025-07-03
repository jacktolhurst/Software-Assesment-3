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
            self.underAndItems = {}
            
            self.clock = pygame.time.Clock()

            self.currCursor = None
            
            if currentGridAttributes == None:
                self.gridAttributes = GridAttributes()
            else:
                self.gridAttributes = currentGridAttributes
            
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                inputOffsetX = 60
                
                infoGridSize = Text("The size of the grid.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["GridSizeText"] = Text("Grid Size:", 'freesansbold.ttf', Vector2(2,5), 15, (255,255,255), zDist=1, underItem=infoGridSize)
                self.UIs["InputGridSize"] = Text(str(int(self.gridAttributes.gridSize.x)), 'freesansbold.ttf', self.UIs["GridSizeText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=3, numOnly=True, underItem=infoGridSize)
                
                infoUnderPopulation = Text("Minimum number of Cells required for a live Cell to survive.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["UnderPopulationText"] = Text("Underpopulation Threshold:", 'freesansbold.ttf', Vector2(2,10), 15, (255,255,255), underItem=infoUnderPopulation)
                self.UIs["InputUnderPopulation"] = Text(str(int(self.gridAttributes.underPopulationThreshold)), 'freesansbold.ttf', self.UIs["UnderPopulationText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoUnderPopulation)
                
                infoSurvivalMin = Text("The minimum number of alive Cell to allow a Cell to survive.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["SurvivalMinText"] = Text("Survival Minimum:", 'freesansbold.ttf', Vector2(2,15), 15, (255,255,255), underItem=infoSurvivalMin)
                self.UIs["InputSurvivalMin"] = Text(str(int(self.gridAttributes.survivalMin)), 'freesansbold.ttf', self.UIs["SurvivalMinText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoSurvivalMin)
                
                infoSurvivalMax = Text("The maximum number of alive Cell to allow a Cell to survive.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["SurvivalMaxText"] = Text("Survival Maximum:", 'freesansbold.ttf', Vector2(2,20), 15, (255,255,255), underItem=infoSurvivalMax)
                self.UIs["InputSurvivalMax"] = Text(str(int(self.gridAttributes.survivalMax)), 'freesansbold.ttf', self.UIs["SurvivalMaxText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoSurvivalMax)
                
                infoOverpopulationThreshold = Text("The maximum alive Cells before a live cell dies.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["OverpopulationThresholdText"] = Text("Overpopulation Threshold:", 'freesansbold.ttf', Vector2(2,25), 15, (255,255,255), underItem=infoOverpopulationThreshold)
                self.UIs["InputOverpopulationThreshold"] = Text(str(int(self.gridAttributes.overpopulationThreshold)), 'freesansbold.ttf', self.UIs["OverpopulationThresholdText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoOverpopulationThreshold)
                
                infoReproductionCount = Text("The exact amount of Cells for a dead Cell to become alive.", 'freesansbold.ttf', Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["ReproductionCountText"] = Text("Reproduction Count:", 'freesansbold.ttf', Vector2(2,30), 15, (255,255,255), underItem=infoReproductionCount)
                self.UIs["InputReproductionCount"] = Text(str(int(self.gridAttributes.reproductionCount)), 'freesansbold.ttf', self.UIs["ReproductionCountText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoReproductionCount)
                
                self.UIs["FPSCount"] = Text("FPS", 'freesansbold.ttf', Vector2(100,90), 10, (255,255,255))
                
                self.UIs["QuitButton"] = UI(Circle, Vector2(165,87.5), Vector2(10,10), (255,0,0))
                self.UIs["QuitButtonText"] = Text("Quit", 'freesansbold.ttf', self.UIs["QuitButton"].GetPosPercent()+Vector2(2.4,3.75), 10, (0,0,0))
                
                self.inputUIs = {name: ui for name, ui in self.UIs.items() if name.startswith("Input")}
                
                for ui in self.UIs.values():
                    under = ui.GetUnderItem()
                    if under is not None:
                        if under not in self.underAndItems:
                            self.underAndItems[under] = []
                        self.underAndItems[under].append(ui)
                
                self.looping = True
                
                self.Update()
                
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                
                try:
                    self.gridAttributes.gridSize = Vector2( int(self.UIs["InputGridSize"].GetText()), int(self.UIs["InputGridSize"].GetText()))
                    
                    self.gridAttributes.underPopulationThreshold = int(self.UIs["InputUnderPopulation"].GetText())
                    
                    self.gridAttributes.survivalMin = int(self.UIs["InputSurvivalMin"].GetText())
                    
                    self.gridAttributes.survivalMax = int(self.UIs["InputSurvivalMax"].GetText())
                    
                    self.gridAttributes.overpopulationThreshold = int(self.UIs["InputOverpopulationThreshold"].GetText())
                    
                    self.gridAttributes.reproductionCount = int(self.UIs["InputReproductionCount"].GetText())
                except Exception as e:
                    self.UIs["Error"] = Text("An Error Occured: " + str(e),'freesansbold.ttf', Vector2(20,80), 10, (255,0,0), bgColor=(0,0,0,255))
                    self.DrawEverything()
                    pygame.time.wait(5000)
                
                
                return self.gridAttributes
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                
                if inputText is not None:
                    desired = con.IBEAMCURSOR
                elif self.UIs["QuitButton"].CheckCollidePoint(mousePos):
                    desired = con.HANDCURSOR
                elif any(inputUI.CheckCollidePoint(mousePos) for inputUI in self.inputUIs.values()):
                    desired = con.HANDCURSOR
                else:
                    desired = con.ARROWCURSOR
                
                if desired is not self.currCursor:
                    pygame.mouse.set_cursor(desired)
                    self.currCursor = desired
                
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
                                inputText.ChangeText("")
                            else:
                                if inputText is not None and len(inputText.GetText()) < 1:
                                    inputText.ChangeText("0")
                                inputText = None
                    
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                

                if inputText is None:
                    for under, uiList in self.underAndItems.items():
                        for ui in uiList:
                            if ui.CheckCollidePoint(mousePos):
                                under.MoveSet(UI.RealPosToPercent(con.HANDLER.TupleToVector2(mousePos)))
                                under.SetState(True)
                                break
                            else:
                                under.SetState(False)
                else:
                    for under in self.underAndItems.keys():
                        under.SetState(False)

                if self.UIs["InputSurvivalMax"].GetText() is not "" and self.UIs["InputSurvivalMin"].GetText() is not "":
                    if int(self.UIs["InputSurvivalMax"].GetText()) < int(self.UIs["InputSurvivalMin"].GetText()):
                        self.UIs["InputSurvivalMax"].ChangeText(str(int(self.UIs["InputSurvivalMin"].GetText())+1))
                
                
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