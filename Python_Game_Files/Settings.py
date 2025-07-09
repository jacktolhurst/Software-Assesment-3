import pygame
import json
import numpy
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import *

class Settings():
    def __init__(self):
        self.looping = False
        
        self.displayVariableList = []
        
        self.UIs = {}
        self.slidersUIs = {}
        self.underAndItems = {}
        self.inputUIs = {}
        self.savedRulesUI = {}

        self.currCursor = None
        
        try:
            with open(con.COLORPRESETSSAVEPATH, 'r') as file:
                self.colorPresetsData = json.load(file)
        except:
            self.colorPresetsData = {}
        
        self.Start() 
    
    def Start(self):
        self.looping = True
        
        self.ResetScreen()
        
        self.Update()
    
    def Update(self):
        inputText = None
        selectedSlider = None
        
        while self.looping:
            mousePos = pygame.mouse.get_pos()
            
            if inputText is not None:
                desired = con.IBEAMCURSOR
            elif self.UIs["ExitText"].CheckCollidePoint(mousePos):
                desired = con.HANDCURSOR
            elif self.UIs["SaveButton"].CheckCollidePoint(mousePos):
                desired = con.HANDCURSOR
            elif any(element.CheckCollidePoint(mousePos) for element in self.inputUIs.values()):
                desired = con.HANDCURSOR
            elif any(element.CheckCollidePoint(mousePos) for element in self.savedRulesUI.values()):
                desired = con.HANDCURSOR
            else:
                desired = con.ARROWCURSOR
            
            found = False
            for element in self.displayVariableList:
                for underElement in element[2]:
                    if underElement[0].CheckCollidePoint(mousePos):
                        desired = con.HANDCURSOR
                        found = True
                        break
                if found:
                    break
            
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
                    else:
                        if event.key == pygame.K_q:
                            self.Stop()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.UIs["ExitText"].CheckCollidePoint(mousePos):
                            self.Stop()
                        elif self.UIs["SaveButton"].CheckCollidePoint(mousePos):
                            with open(con.COLORPRESETSSAVEPATH, 'r') as f:
                                self.colorPresetsData = json.load(f)
                            
                            with open(con.COLORPRESETSSAVEPATH, 'w') as file:
                                
                                self.colorPresetsData[self.UIs["InputEnterName"].GetText()] = {
                                    "CELLALIVECOLOR":    con.CELLALIVECOLOR.copy(),
                                    "CELLDEADCOLOR":     con.CELLDEADCOLOR.copy(),
                                    "CELLUNTOUCHCOLOR":  con.CELLUNTOUCHCOLOR.copy(),
                                    "BACKGROUNDCOLOR":   con.BACKGROUNDCOLOR.copy()
                                }

                                json.dump(self.colorPresetsData, file, indent=4)

                                self.RecreateGridUIs()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if any(element.CheckCollidePoint(mousePos) for element in self.slidersUIs.keys()) and selectedSlider is None:
                            selectedElement = next((element for element in self.slidersUIs.keys() if element.CheckCollidePoint(mousePos)),None)
                            selectedElementBackground = next((background for element,background in self.slidersUIs.items() if element.CheckCollidePoint(mousePos)),None)

                            if selectedElement and selectedElementBackground:
                                selectedSlider = (selectedElement, selectedElementBackground)
                            else:
                                selectedSlider = None
                        elif any(element.CheckCollidePoint(mousePos) for element in self.savedRulesUI.values()):
                            saveName = None
                            for name, element in self.savedRulesUI.items():
                                if element.CheckCollidePoint(mousePos):
                                    saveName = name
                                    break
                                
                            with open(con.COLORPRESETSSAVEPATH, 'r') as file:
                                data = json.load(file)

                            for name, valueData in data.items():
                                if saveName.lower() in name.lower():
                                    innerData = valueData
                                    break
                            
                            for name, color in innerData.items():
                                if name == "CELLALIVECOLOR":
                                    con.CELLALIVECOLOR = color
                                elif name == "CELLDEADCOLOR":
                                    con.CELLDEADCOLOR = color
                                elif name == "CELLUNTOUCHCOLOR":
                                    con.CELLUNTOUCHCOLOR = color
                                elif name == "BACKGROUNDCOLOR":
                                    con.BACKGROUNDCOLOR = color
                                

                            self.ResetScreen()

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
                                with open(con.COLORPRESETSSAVEPATH, 'r') as file:
                                    self.colorPresetsData = json.load(file)
                        
                                keysToRemove = [key for key in self.colorPresetsData.keys() if clickedElementName.lower() in key.lower()]
                                for key in keysToRemove:
                                    self.colorPresetsData.pop(key)
                        
                                with open(con.COLORPRESETSSAVEPATH, 'w') as file:
                                    json.dump(self.colorPresetsData, file, indent=4)

                                self.RecreateGridUIs()
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            if pygame.mouse.get_pressed()[0]:
                if selectedSlider:
                    clampMin = selectedSlider[1].GetPosReal().y
                    clampMax = (selectedSlider[1].GetPosReal().y+selectedSlider[1].GetSizeReal().y)-selectedSlider[0].GetSizeReal().y
                    selectedSlider[0].MoveSetRealY(con.HANDLER.Clamp(mousePos[1]-(selectedSlider[0].GetSizeReal().y/2), clampMin, clampMax))
            else:
                selectedSlider = None
            
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
            
            self.ApplySliderToDisplay(self.displayVariableList)
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
    
    def PosToColor(self, RGBSliders) -> tuple[int,int,int]:
        curr = []
        for slider, bg in RGBSliders:
            offset = slider.GetPosReal().y - bg.GetPosReal().y
            travel = bg.GetSizeReal().y - slider.GetSizeReal().y
            ratio = con.HANDLER.Clamp(offset / travel, 0,1)
            ratio = 1.0 - ratio
            curr.append(int(ratio * 255))
        return tuple(curr)
    
    def ColorToPos(self, color:tuple[int,int,int], RGBSliders):
        for value, (slider, bg) in zip(color, RGBSliders):
            norm = value / 255.0
            ratio = 1.0 - norm
            travel = bg.GetSizeReal().y - slider.GetSizeReal().y
            offset = ratio * travel
            y = bg.GetPosReal().y + offset
            slider.MoveSetRealY(y)

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

    def ApplySliderToDisplay(self, list:list):
        for item in list:
            display = item[0]
            variable = item[1]
            references = item[2]
            
            newColor = self.PosToColor(references)
            display.ChangeColor(newColor)
            
            variable[0] = newColor[0]
            variable[1] = newColor[1]
            variable[2] = newColor[2]
    
    def RecreateGridUIs(self):
        for name in self.savedRulesUI.keys():
            self.UIs.pop(name)

        self.savedRulesUI = {}
        
        for name in self.colorPresetsData.keys():
            underItem = Text("Right Click to delete.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
            element = Text(name, Vector2(UI.GetEdgeXPercentage()-20,15+(5*len(self.savedRulesUI))), 15, (255,255,255), bgColor=(20,30,40,255), underItems=[underItem])
            self.savedRulesUI[name] = element
            self.UIs[name] = element
            self.underAndItems = self.GetUnderItems()

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

    
    def CreateRGBSlider(self, leadingStr:str, pos:Vector2, title:str, variableReference:list):
        mainBackground = UI(Quad, pos, Vector2(30,20), (100,100,100))
        self.UIs[leadingStr+"MainBackground"] = mainBackground
        
        titleText = Text(title, mainBackground.GetPosPercent()+Vector2(1,1), 10, con.TEXTCOLOR)
        self.UIs[leadingStr+"TitleText"] = titleText
        titleTextEndPoint = titleText.GetPosPercent()+(UI.RealPosToPercent(Vector2(titleText.GetRect().size)))
        
        mainBackground.SizeSet(Vector2(con.HANDLER.Clamp((titleTextEndPoint.x - mainBackground.GetPosPercent().x) + 1, mainBackground.GetSizePercent().x, 100), mainBackground.GetSizePercent().y))
        
        pickedColorBackground = UI(Quad,mainBackground.GetPosPercentCenter()-Vector2(mainBackground.GetSizePercent().x/2,0), Vector2(12,12), (50,50,50))
        pickedColorBackground.MoveAdd((pickedColorBackground.GetSizePercent()*-0.5) + Vector2((pickedColorBackground.GetSizePercent().x/2)+1,titleText.GetRectSize().y-1))
        self.UIs[leadingStr+"PickedColorBackground"] = pickedColorBackground
        pickedColorBackgroundEndPoint = pickedColorBackground.GetPosPercent()+(UI.RealPosToPercent(Vector2(pickedColorBackground.GetRect().size)))
        
        pickedColorMain = UI(Quad, pickedColorBackground.GetPosPercentCenter(), pickedColorBackground.GetSizePercent()-Vector2(2,2), (0,0,0))
        pickedColorMain.MoveAdd(pickedColorMain.GetSizePercent()*-0.5)
        self.UIs[leadingStr+"PickedColorMain"] = pickedColorMain
        
        redText = Text("Red", Vector2(0,0), 5, (145,120,120), bgColor=(70,70,70,255), zDist=2)
        redSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+2,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (75,50,50))
        redSliderCursor = UI(Circle, redSliderBackground.GetPosPercent(), Vector2(redSliderBackground.GetSizePercent().x, redSliderBackground.GetSizePercent().x), (255,255,255), underItems=[redText])
        self.slidersUIs[redSliderCursor] = redSliderBackground
        self.UIs[leadingStr+"RedSliderBackground"] = redSliderBackground
        self.UIs[leadingStr+"RedSliderCursor"] = redSliderCursor
        
        greenText = Text("Green", Vector2(0,0), 5, (120,145,120), bgColor=(70,70,70,255), zDist=2)
        greenSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+7,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (50,75,50))
        greenSliderCursor = UI(Circle, greenSliderBackground.GetPosPercent(), Vector2(greenSliderBackground.GetSizePercent().x, greenSliderBackground.GetSizePercent().x), (255,255,255), underItems=[greenText])
        self.slidersUIs[greenSliderCursor] = greenSliderBackground
        self.UIs[leadingStr+"GreenSliderBackground"] = greenSliderBackground
        self.UIs[leadingStr+"GreenSliderCursor"] = greenSliderCursor
        
        blueText = Text("Blue", Vector2(0,0), 5, (120,120,145), bgColor=(70,70,70,255), zDist=2)
        blueSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+12,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (50,50,75))
        blueSliderCursor = UI(Circle, blueSliderBackground.GetPosPercent(), Vector2(blueSliderBackground.GetSizePercent().x, blueSliderBackground.GetSizePercent().x), (255,255,255), underItems=[blueText])
        self.slidersUIs[blueSliderCursor] = blueSliderBackground
        self.UIs[leadingStr+"BlueSliderBackground"] = blueSliderBackground
        self.UIs[leadingStr+"BlueSliderCursor"] = blueSliderCursor
        
        listOfRef = [(redSliderCursor,redSliderBackground),(greenSliderCursor,greenSliderBackground),(blueSliderCursor,blueSliderBackground)]
        
        self.ColorToPos(tuple(variableReference), listOfRef)
        
        return (pickedColorMain, variableReference, listOfRef)
        
    def ResetScreen(self):
        if con.HANDLER.IsTupleClose(tuple(con.BACKGROUNDCOLOR), (0,0,0), 200):
            con.TEXTCOLOR = (255,255,255)
        else:
            con.TEXTCOLOR = (0,0,0)
        
        self.displayVariableList.append(self.CreateRGBSlider("CellColor", Vector2(5,5), "Cell Colour:", con.CELLALIVECOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("DeadCellColor", Vector2(40,5), "Dead Cell Colour:", con.CELLDEADCOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("WallColor", Vector2(5,30), "Wall Colour:", con.CELLUNTOUCHCOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("BackgroundColor", Vector2(40,30), "Background Colour:", con.BACKGROUNDCOLOR))
        
        infoEnterName = Text("The name of the preset.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
        self.UIs["EnterNameText"] = Text("Preset Name:", Vector2(5,55), 15, con.TEXTCOLOR, underItems=[infoEnterName])
        self.UIs["InputEnterName"] = Text("Name", self.UIs["EnterNameText"].GetPosPercent() + Vector2(self.UIs["EnterNameText"].GetRectSize().x+2,0), 15, con.TEXTCOLOR, bgColor=(20,30,40,255), maxStrLength=12, underItems=[infoEnterName], defaultStr="Name")
        
        infoSave = Text("Save the values to a preset.", Vector2(0,0), 5, (120,120,120), bgColor=(70,70,70,255), zDist=2)
        self.UIs["SaveButton"] = Text("Save Preset", Vector2(22,65), 20, con.TEXTCOLOR, bgColor=(20,30,40,255), underItems=[infoSave])
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
        self.underAndItems = self.GetUnderItems()
        self.inputUIs = {name: ui for name, ui in self.UIs.items() if name.startswith("Input")}
        
        self.RecreateGridUIs()
        
    def Stop(self):
        if self.looping:
            
            self.looping = False