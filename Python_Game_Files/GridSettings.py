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
                with open(con.ATTRIBUTESSAVEPATH, 'r') as file:
                    self.gridAttributesData = json.load(file)
            except:
                self.gridAttributesData = {}
            
            
        def Start(self):
            if not self.looping:
                con.CURRSCREEN = self
                
                self.ResetScreen()
                
                self.looping = True
                
                self.Update()
                
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                
                
                self.EnterDataToGridAttributes()
                
                return self.gridAttributes
        
        def Update(self):
            inputText = None
            
            while self.looping:
                mousePos = pygame.mouse.get_pos()
                
                if inputText is not None:
                    desired = con.IBEAMCURSOR
                elif self.UIs["SaveAndQuitText"].CheckCollidePoint(mousePos) or self.UIs["SaveAttributesButton"].CheckCollidePoint(mousePos):
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
                        else:
                            if event.key == pygame.K_q:
                                self.Stop()
                        
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            if self.UIs["SaveAndQuitText"].CheckCollidePoint(mousePos):
                                self.Stop()
                            elif self.UIs["SaveAttributesButton"].CheckCollidePoint(mousePos):
                                newName = self.UIs["InputEnterName"].GetText()
                                if newName != "Name":
                                    self.UIs["SaveBlock"].SetState(False)
                                    
                                    with open(con.ATTRIBUTESSAVEPATH, 'w') as file:

                                        dataName = str(self.UIs["InputEnterName"].GetText())
                                        newData = self.gridAttributes.ToDict()
                                        
                                        oldKey = None
                                        for name, data in self.gridAttributesData.items():
                                            if newData == data:
                                                oldKey = name
                                                break
                                        if oldKey:
                                            del self.gridAttributesData[oldKey]

                                        self.gridAttributesData[dataName] = newData

                                        json.dump(self.gridAttributesData, file, indent=4)

                                        self.RecreateGridUIs()

                                    self.UIs["InputEnterName"].ChangeText("Name")
                                else:
                                    self.UIs["SaveBlock"].SetState(True)
                                
                            elif any(element.CheckCollidePoint(mousePos) for element in self.savedRulesUI.values()):
                                saveName = None
                                for name, element in self.savedRulesUI.items():
                                    if element.CheckCollidePoint(mousePos):
                                        saveName = name
                                        break
                                    
                                with open(con.ATTRIBUTESSAVEPATH, 'r') as file:
                                    data = json.load(file)

                                    for name, valueData in data.items():
                                        if saveName.lower() in name.lower():
                                            innerData = valueData
                                            break
                                        
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
                        elif event.button == 3:
                            for name, element in self.savedRulesUI.items():
                                if element.CheckCollidePoint(mousePos):
                                    clickedElementName = name
                                    break
                            else:
                                clickedElementName = None
                        
                            if clickedElementName:
                                with open(con.ATTRIBUTESSAVEPATH, 'r') as file:
                                    self.gridAttributesData = json.load(file)
                        
                                keysToRemove = [key for key in self.gridAttributesData.keys() if clickedElementName.lower() in key.lower()]
                                for key in keysToRemove:
                                    self.gridAttributesData.pop(key)
                        
                                with open(con.ATTRIBUTESSAVEPATH, 'w') as file:
                                    json.dump(self.gridAttributesData, file, indent=4)

                                self.RecreateGridUIs()
                    
                    if event.type == QUIT:
                        con.HANDLER.QuitGame()
                

                if inputText is None:
                    for under, uiList in self.underAndItems.items():
                        for ui in uiList:
                            if ui.CheckCollidePoint(mousePos):
                                under.MoveSet(UI.RealPosToPercent(Vector2(*mousePos))+Vector2(1,1))
                                under.SetState(True)
                                break
                            else:
                                under.SetState(False)
                else:
                    for under in self.underAndItems.keys():
                        under.SetState(False)

                if self.UIs["InputSurvivalMax"].GetText() != "" and self.UIs["InputSurvivalMin"].GetText() != "" and self.UIs["InputUnderPopulation"].GetText() != "":
                    if int(self.UIs["InputSurvivalMin"].GetText()) <= int(self.UIs["InputUnderPopulation"].GetText()):
                        self.UIs["InputSurvivalMin"].ChangeText(str(int(int(self.UIs["InputUnderPopulation"].GetText()))))
                    if int(self.UIs["InputSurvivalMax"].GetText()) <= int(self.UIs["InputSurvivalMin"].GetText()):
                        self.UIs["InputSurvivalMax"].ChangeText(str(int(self.UIs["InputSurvivalMin"].GetText())))
                
                if self.UIs["InputEnterName"].GetText() == "Name":
                    self.UIs["SaveAttributesButton"].ChangeBgColor((70,70,70))
                else:
                    self.UIs["SaveAttributesButton"].ChangeBgColor(con.INPUTUICOLOR)
                
                self.DrawEverything()
                
                self.clock.tick(120)
        
        def DrawEverything(self):
            con.SCREEN.fill(con.BACKGROUNDCOLOR)
            
            con.HANDLER.DrawUI(self, self.UIs)
            
            pygame.display.update()
        
        def RecreateGridUIs(self):
            for name in self.savedRulesUI.keys():
                self.UIs.pop(name)

            self.savedRulesUI = {}
            
            for name in self.gridAttributesData.keys():
                underItem = Text("Right Click to delete.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
                element = Text(name, Vector2(UI.GetEdgeXPercentage()-25,15+(5*len(self.savedRulesUI))), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, underItems=[underItem])
                self.savedRulesUI[name] = element
                self.UIs[name] = element
                self.underAndItems = self.GetUnderItems()
        
        def EnterGridAttributesToUI(self):
            self.UIs["InputGridSize"].ChangeText(str(int(self.gridAttributes.gridSize.x)))
            self.UIs["InputUnderPopulation"].ChangeText(str(int(self.gridAttributes.underPopulationThreshold)))
            self.UIs["InputSurvivalMin"].ChangeText(str(int(self.gridAttributes.survivalMin)))
            self.UIs["InputSurvivalMax"].ChangeText(str(int(self.gridAttributes.survivalMax)))
            self.UIs["InputOverpopulationThreshold"].ChangeText(str(int(self.gridAttributes.overpopulationThreshold)))
            self.UIs["InputReproductionCount"].ChangeText(str(int(self.gridAttributes.reproductionCount)))\
        
        def EnterDataToGridAttributes(self):
            try:
                if self.UIs["InputGridSize"].GetText() != "":
                    size = int(self.UIs["InputGridSize"].GetText())
                    self.gridAttributes.gridSize = Vector2(size, size)

                if self.UIs["InputUnderPopulation"].GetText() != "":
                    self.gridAttributes.underPopulationThreshold = int(self.UIs["InputUnderPopulation"].GetText())

                if self.UIs["InputSurvivalMin"].GetText() != "":
                    self.gridAttributes.survivalMin = int(self.UIs["InputSurvivalMin"].GetText())

                if self.UIs["InputSurvivalMax"].GetText() != "":
                    self.gridAttributes.survivalMax = int(self.UIs["InputSurvivalMax"].GetText())

                if self.UIs["InputOverpopulationThreshold"].GetText() != "":
                    self.gridAttributes.overpopulationThreshold = int(self.UIs["InputOverpopulationThreshold"].GetText())

                if self.UIs["InputReproductionCount"].GetText() != "":
                    self.gridAttributes.reproductionCount = int(self.UIs["InputReproductionCount"].GetText())
            except :
                pass


        def GetUnderItems(self) -> dict:
            underItems = {}
            
            for ui in self.UIs.values():
                unders = ui.GetUnderItem() 
                if unders:
                    for under in unders:
                        if under not in underItems:
                            underItems[under] = []
                        underItems[under].append(ui)
            
            return underItems
        
        def ResetScreen(self):
            inputOffsetX = 60
            
            self.UIs["GridAttributesHeader"] = Text("Grid Attributes:", Vector2(20,5), 20, con.TEXTCOLOR)
            self.UIs["GridPresetsHeader"] = Text("Grid Presets:", Vector2(UI.GetEdgeXPercentage()-35,5), 20, con.TEXTCOLOR)
            
            infoGridSize = Text("The size of the grid.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["GridSizeText"] = Text("Grid Size:", Vector2(2,15), 15, con.TEXTCOLOR, zDist=1, underItems=[infoGridSize])
            self.UIs["InputGridSize"] = Text("0", self.UIs["GridSizeText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=3, numOnly=True, underItems=[infoGridSize], defaultStr="100")
            
            infoUnderPopulation = Text("The lowest number of neighbors a live Cell must have to avoid dying.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["UnderPopulationText"] = Text("Underpopulation Threshold:", self.UIs["GridSizeText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoUnderPopulation])
            self.UIs["InputUnderPopulation"] = Text("0", self.UIs["UnderPopulationText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=1, numOnly=True, underItems=[infoUnderPopulation], defaultStr="0")
            
            infoSurvivalMin = Text("The minimum number of neighbors a live Cell must have to continue living.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["SurvivalMinText"] = Text("Survival Minimum:",  self.UIs["UnderPopulationText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoSurvivalMin])
            self.UIs["InputSurvivalMin"] = Text("0", self.UIs["SurvivalMinText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=1, numOnly=True, underItems=[infoSurvivalMin], defaultStr="0")
            
            infoSurvivalMax = Text("The maximum number of alive Cell to allow a Cell to survive.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["SurvivalMaxText"] = Text("Survival Maximum:", self.UIs["SurvivalMinText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoSurvivalMax])
            self.UIs["InputSurvivalMax"] = Text("0", self.UIs["SurvivalMaxText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=1, numOnly=True, underItems=[infoSurvivalMax], defaultStr="0")
            
            infoOverpopulationThreshold = Text("The maximum alive Cells before a live cell dies.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["OverpopulationThresholdText"] = Text("Overpopulation Threshold:", self.UIs["SurvivalMaxText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoOverpopulationThreshold])
            self.UIs["InputOverpopulationThreshold"] = Text("0", self.UIs["OverpopulationThresholdText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=1, numOnly=True, underItems=[infoOverpopulationThreshold], defaultStr="0")
            
            infoReproductionCount = Text("The exact amount of Cells for a dead Cell to become alive.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["ReproductionCountText"] = Text("Reproduction Count:", self.UIs["OverpopulationThresholdText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoReproductionCount])
            self.UIs["InputReproductionCount"] = Text("0", self.UIs["ReproductionCountText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=1, numOnly=True, underItems=[infoReproductionCount],defaultStr="0")
            
            self.EnterGridAttributesToUI()
            
            infoEnterName = Text("The name of the preset.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["EnterNameText"] = Text("Preset Name:", self.UIs["ReproductionCountText"].GetPosPercent()+Vector2(0,5), 15, con.TEXTCOLOR, underItems=[infoEnterName])
            self.UIs["InputEnterName"] = Text("Name", self.UIs["EnterNameText"].GetPosPercent()+Vector2(inputOffsetX,0), 15, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, maxStrLength=12, underItems=[infoEnterName], defaultStr="Name")
            
            infoSave = Text("Save the values to a preset.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            self.UIs["SaveAttributesButton"] = Text("Save Preset", Vector2(inputOffsetX/2-4,self.UIs["EnterNameText"].GetPosPercent().y+10), 20, con.TEXTCOLOR, bgColor=con.INPUTUICOLOR, underItems=[infoSave])
            self.UIs["SaveBlock"] = Text("You cannot name a preset \"Name\"", self.UIs["SaveAttributesButton"].GetPosPercent()-Vector2(6,4), 10, (255,0,0), state=False)
            
            self.UIs["SaveAndQuitText"] = Text("Apply and Exit", Vector2(UI.GetEdgeXPercentage()-20, UI.GetEdgeYPercentage()-5), 10, (0,0,0), bgColor=(0,255,0,255))
            
            self.RecreateGridUIs()
            
            self.inputUIs = {name: ui for name, ui in self.UIs.items() if name.startswith("Input")}
            
            self.underAndItems = self.GetUnderItems()
        
        def Stop(self):
            if self.looping:
                self.looping = False