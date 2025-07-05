import pygame
import json
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
            self.savedRulesUI = {}
            
            self.clock = pygame.time.Clock()

            self.currCursor = None
            
            if currentGridAttributes == None:
                self.gridAttributes = GridAttributes()
            else:
                self.gridAttributes = currentGridAttributes
            
            try:
                with open(con.SETTINGSSAVEPATH, 'r') as file:
                    self.gridAttributesData = json.load(file)
            except:
                self.gridAttributesData = {}
            
            
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                inputOffsetX = 60
                
                infoGridSize = Text("The size of the grid.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["GridSizeText"] = Text("Grid Size:", Vector2(2,5), 15, (255,255,255), zDist=1, underItem=infoGridSize)
                self.UIs["InputGridSize"] = Text("0", self.UIs["GridSizeText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=3, numOnly=True, underItem=infoGridSize, defaultStr="100")
                
                infoUnderPopulation = Text("Minimum number of Cells required for a live Cell to survive.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["UnderPopulationText"] = Text("Underpopulation Threshold:", Vector2(2,10), 15, (255,255,255), underItem=infoUnderPopulation)
                self.UIs["InputUnderPopulation"] = Text("0", self.UIs["UnderPopulationText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoUnderPopulation, defaultStr="0")
                
                infoSurvivalMin = Text("The minimum number of alive Cell to allow a Cell to survive.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["SurvivalMinText"] = Text("Survival Minimum:", Vector2(2,15), 15, (255,255,255), underItem=infoSurvivalMin)
                self.UIs["InputSurvivalMin"] = Text("0", self.UIs["SurvivalMinText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoSurvivalMin, defaultStr="0")
                
                infoSurvivalMax = Text("The maximum number of alive Cell to allow a Cell to survive.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["SurvivalMaxText"] = Text("Survival Maximum:", Vector2(2,20), 15, (255,255,255), underItem=infoSurvivalMax)
                self.UIs["InputSurvivalMax"] = Text("0", self.UIs["SurvivalMaxText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoSurvivalMax, defaultStr="0")
                
                infoOverpopulationThreshold = Text("The maximum alive Cells before a live cell dies.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["OverpopulationThresholdText"] = Text("Overpopulation Threshold:", Vector2(2,25), 15, (255,255,255), underItem=infoOverpopulationThreshold)
                self.UIs["InputOverpopulationThreshold"] = Text("0", self.UIs["OverpopulationThresholdText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoOverpopulationThreshold, defaultStr="0")
                
                infoReproductionCount = Text("The exact amount of Cells for a dead Cell to become alive.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["ReproductionCountText"] = Text("Reproduction Count:", Vector2(2,30), 15, (255,255,255), underItem=infoReproductionCount)
                self.UIs["InputReproductionCount"] = Text("0", self.UIs["ReproductionCountText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=1, numOnly=True, underItem=infoReproductionCount, defaultStr="0")
                
                self.EnterGridAttributesToUI()
                
                infoEnterName = Text("The name of the saved rule.", Vector2(0,0), 8, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                self.UIs["EnterNameText"] = Text("Name:", Vector2(2,35), 15, (255,255,255), underItem=infoEnterName)
                self.UIs["InputEnterName"] = Text("Name", self.UIs["EnterNameText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, (255,255,255), bgColor=(20,30,40,255), maxStrLength=12, underItem=infoEnterName, defaultStr="Name")
                
                self.UIs["SaveButton"] = Text("Save", Vector2(inputOffsetX,45), 20, (255,255,255), bgColor=(20,30,40,255))
                
                self.UIs["FPSCount"] = Text("FPS", Vector2(100,90), 10, (255,255,255))
                
                self.UIs["QuitButton"] = UI(Circle, Vector2(165,87.5), Vector2(10,10), (255,0,0))
                self.UIs["QuitButtonText"] = Text("Quit", self.UIs["QuitButton"].GetPosPercent()+Vector2(2.4,3.75), 10, (0,0,0))
                
                self.RecreateGridUIs()
                
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
                
                self.EnterDataToGridAttributes()
                
                try:
                    self.gridAttributes.gridSize = Vector2( int(self.UIs["InputGridSize"].GetText()), int(self.UIs["InputGridSize"].GetText()))
                    
                    self.gridAttributes.underPopulationThreshold = int(self.UIs["InputUnderPopulation"].GetText())
                    
                    self.gridAttributes.survivalMin = int(self.UIs["InputSurvivalMin"].GetText())
                    
                    self.gridAttributes.survivalMax = int(self.UIs["InputSurvivalMax"].GetText())
                    
                    self.gridAttributes.overpopulationThreshold = int(self.UIs["InputOverpopulationThreshold"].GetText())
                    
                    self.gridAttributes.reproductionCount = int(self.UIs["InputReproductionCount"].GetText())
                except Exception as e:
                    self.UIs["Error"] = Text("An Error Occured: " + str(e), Vector2(20,80), 10, (255,0,0), bgColor=(0,0,0,255))
                    self.DrawEverything()
                    pygame.time.wait(5000)
                
                
                return self.gridAttributes
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                
                if inputText is not None:
                    desired = con.IBEAMCURSOR
                elif self.UIs["QuitButton"].CheckCollidePoint(mousePos) or self.UIs["SaveButton"].CheckCollidePoint(mousePos):
                    desired = con.HANDCURSOR
                elif any(element.CheckCollidePoint(mousePos) for element in self.inputUIs.values()):
                    desired = con.HANDCURSOR
                elif any(element.CheckCollidePoint(mousePos) for element in self.savedRulesUI.values()):
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
                            self.EnterDataToGridAttributes()
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.UIs["QuitButton"].CheckCollidePoint(mousePos):
                            self.Stop()
                        elif self.UIs["SaveButton"].CheckCollidePoint(mousePos):
                            with open(con.SETTINGSSAVEPATH, 'w') as file:
                                
                                dataName = str(self.UIs["InputEnterName"].GetText())
                                data = self.gridAttributes.ToDict()
                                
                                self.gridAttributesData[dataName] = data
                                
                                json.dump(self.gridAttributesData, file, indent=4)
                                
                                self.RecreateGridUIs()
                        elif any(element.CheckCollidePoint(mousePos) for element in self.savedRulesUI.values()):
                            saveName = None
                            for name, element in self.savedRulesUI.items():
                                if element.CheckCollidePoint(mousePos):
                                    saveName = name
                                    break
                            
                            with open(con.SETTINGSSAVEPATH, 'r') as file:
                                data = json.load(file)
                                
                                for name, valueData in data.items():
                                    if saveName.lower() in name.lower():
                                        innerData = valueData
                                
                                self.gridAttributes.FromDict(innerData)
                                
                                self.EnterGridAttributesToUI()
                            
                        else:
                            for ui in self.inputUIs.values():
                                ui.ChangeBgColor(ui.GetInitialBgColor())

                            selected = next(
                                (ui for ui in self.inputUIs.values() if ui.CheckCollidePoint(mousePos)),
                                None
                            )

                            if selected and inputText is None:
                                selected.ChangeBgColor(con.SELECTEDUICOLOR)
                                inputText = selected
                                inputText.ChangeText("")
                            else:
                                if inputText is not None:
                                    inputText.ChangeText(inputText.GetText(), True)
                                inputText = None
                    
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                

                if inputText is None:
                    for under, uiList in self.underAndItems.items():
                        for ui in uiList:
                            if ui.CheckCollidePoint(mousePos):
                                under.MoveSet(UI.RealPosToPercent(Vector2(*mousePos)))
                                under.SetState(True)
                                break
                            else:
                                under.SetState(False)
                else:
                    for under in self.underAndItems.keys():
                        under.SetState(False)

                if self.UIs["InputSurvivalMax"].GetText() != "" and self.UIs["InputSurvivalMin"].GetText() != "":
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
        
        def RecreateGridUIs(self):
            for name in self.savedRulesUI.keys():
                self.UIs.pop(name)

            self.savedRulesUI = {}
            
            for name in self.gridAttributesData.keys():
                element = Text(name, Vector2(120,5+(10*len(self.savedRulesUI))), 20, (255,255,255), bgColor=(20,30,40,255))
                self.savedRulesUI[name] = element
                self.UIs[name] = element
        
        def EnterGridAttributesToUI(self):
            self.UIs["InputGridSize"].ChangeText(str(int(self.gridAttributes.gridSize.x)))
            self.UIs["InputUnderPopulation"].ChangeText(str(int(self.gridAttributes.underPopulationThreshold)))
            self.UIs["InputSurvivalMin"].ChangeText(str(int(self.gridAttributes.survivalMin)))
            self.UIs["InputSurvivalMax"].ChangeText(str(int(self.gridAttributes.survivalMax)))
            self.UIs["InputOverpopulationThreshold"].ChangeText(str(int(self.gridAttributes.overpopulationThreshold)))
            self.UIs["InputReproductionCount"].ChangeText(str(int(self.gridAttributes.reproductionCount)))\
        
        def EnterDataToGridAttributes(self):
            try:
                self.gridAttributes.gridSize = Vector2(int(self.UIs["InputGridSize"].GetText()), int(self.UIs["InputGridSize"].GetText()))
                self.gridAttributes.underPopulationThreshold = int(self.UIs["InputUnderPopulation"].GetText())
                self.gridAttributes.survivalMin = int(self.UIs["InputSurvivalMin"].GetText())
                self.gridAttributes.survivalMax = int(self.UIs["InputSurvivalMax"].GetText())
                self.gridAttributes.overpopulationThreshold = int(self.UIs["InputOverpopulationThreshold"].GetText())
                self.gridAttributes.reproductionCount = int(self.UIs["InputReproductionCount"].GetText())
            except Exception as e:
                self.UIs["Error"] = Text("An Error Occured: " + str(e), Vector2(20,80), 10, (255,0,0), bgColor=(0,0,0,255))
                self.DrawEverything()
                pygame.time.wait(5000)
        
        def ResetScreen(self):
            pass
        
        def Stop(self):
            if self.looping:
                self.looping = False