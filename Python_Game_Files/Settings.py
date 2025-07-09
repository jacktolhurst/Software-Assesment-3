import pygame
import random
import numpy
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import *
from SandboxLevel import SandBoxLVL

class Settings():
    def __init__(self):
        self.looping = False
        
        self.UIs = {}
        self.slidersUIs = {}
        self.displayVariableList = []

        self.currCursor = None
        
        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.ResetScreen()
        
        self.Update()
    
    def Update(self):
        selectedSlider = None
        
        while self.looping:
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
                    if self.UIs["ExitText"].CheckCollidePoint(mousePos):
                        self.Stop()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if any(element.CheckCollidePoint(mousePos) for element in self.slidersUIs.keys()) and selectedSlider is None:
                        selectedElement = next((element for element in self.slidersUIs.keys() if element.CheckCollidePoint(mousePos)),None)
                        selectedElementBackground = next((background for element,background in self.slidersUIs.items() if element.CheckCollidePoint(mousePos)),None)
                        
                        if selectedElement and selectedElementBackground:
                            selectedSlider = (selectedElement, selectedElementBackground)
                        else:
                            selectedSlider = None
                        
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            if pygame.mouse.get_pressed()[0]:
                if selectedSlider:
                    clampMin = selectedSlider[1].GetPosReal().y
                    clampMax = (selectedSlider[1].GetPosReal().y+selectedSlider[1].GetSizeReal().y)-selectedSlider[0].GetSizeReal().y
                    selectedSlider[0].MoveSetRealY(con.HANDLER.Clamp(mousePos[1], clampMin, clampMax))
            else:
                selectedSlider = None
            
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
            
    def CreateRGBSlider(self, leadingStr:str, pos:Vector2, title:str, variableReference:list):
        mainBackground = UI(Quad, pos, Vector2(30,20), (100,100,100))
        self.UIs[leadingStr+"MainBackground"] = mainBackground
        
        titleText = Text(title, mainBackground.GetPosPercent()+Vector2(1,1), 10, (255,255,255))
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
        
        redSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+2,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (75,50,50))
        redSliderCursor = UI(Circle, redSliderBackground.GetPosPercent(), Vector2(redSliderBackground.GetSizePercent().x, redSliderBackground.GetSizePercent().x), (255,255,255))
        self.slidersUIs[redSliderCursor] = redSliderBackground
        self.UIs[leadingStr+"RedSliderBackground"] = redSliderBackground
        self.UIs[leadingStr+"RedSliderCursor"] = redSliderCursor
        
        greenSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+7,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (50,75,50))
        greenSliderCursor = UI(Circle, greenSliderBackground.GetPosPercent(), Vector2(greenSliderBackground.GetSizePercent().x, greenSliderBackground.GetSizePercent().x), (255,255,255))
        self.slidersUIs[greenSliderCursor] = greenSliderBackground
        self.UIs[leadingStr+"GreenSliderBackground"] = greenSliderBackground
        self.UIs[leadingStr+"GreenSliderCursor"] = greenSliderCursor
        
        blueSliderBackground = UI(Quad, Vector2(pickedColorBackgroundEndPoint.x+12,(mainBackground.GetPosPercent().y+(titleText.GetSizePercent()/2))-0.5),Vector2(3,mainBackground.GetSizePercent().y-6), (50,50,75))
        blueSliderCursor = UI(Circle, blueSliderBackground.GetPosPercent(), Vector2(blueSliderBackground.GetSizePercent().x, blueSliderBackground.GetSizePercent().x), (255,255,255))
        self.slidersUIs[blueSliderCursor] = blueSliderBackground
        self.UIs[leadingStr+"BlueSliderBackground"] = blueSliderBackground
        self.UIs[leadingStr+"BlueSliderCursor"] = blueSliderCursor
        
        listOfRef = [(redSliderCursor,redSliderBackground),(greenSliderCursor,greenSliderBackground),(blueSliderCursor,blueSliderBackground)]
        
        
        self.ColorToPos(tuple(variableReference), listOfRef)
        
        return (pickedColorMain, variableReference, listOfRef)
        
    def ResetScreen(self):
        self.displayVariableList.append(self.CreateRGBSlider("CellColor", Vector2(10,5), "Cell Colour:", con.CELLALIVECOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("DeadCellColor", Vector2(10,30), "Dead Cell Colour:", con.CELLDEADCOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("WallColor", Vector2(10,55), "Wall Colour:", con.CELLUNTOUCHCOLOR))
        self.displayVariableList.append(self.CreateRGBSlider("BackgroundColor", Vector2(10,80), "Background Colour:", con.BACKGROUNDCOLOR))
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
    def Stop(self):
        if self.looping:
            self.looping = False