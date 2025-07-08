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

        self.currCursor = None
        
        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.UIs["ColorPickerBackground"] = UI(Quad, Vector2(20,20), Vector2(60,20), (100,100,100))
        self.UIs["ColorPickerCurrColor"] = UI(Quad, self.UIs["ColorPickerBackground"].GetPosPercentCenter()-Vector2(self.UIs["ColorPickerBackground"].GetSizePercent().x/2,0), Vector2(10,10), (0,0,0))
        self.UIs["ColorPickerCurrColor"].MoveAdd((self.UIs["ColorPickerCurrColor"].GetSizePercent()*-0.5) + Vector2((self.UIs["ColorPickerCurrColor"].GetSizePercent().x/2)+1,0))
        
        self.UIs["RedSliderBackground"], self.UIs["RedSliderCursor"] = self.CreateSlider(self.UIs["ColorPickerBackground"].GetPosPercent()+Vector2(15,1), Vector2(3,self.UIs["ColorPickerBackground"].GetSizePercent().y-2), (75,50,50))
        self.UIs["GreenSliderBackground"], self.UIs["GreenSliderCursor"] = self.CreateSlider(self.UIs["ColorPickerBackground"].GetPosPercent()+Vector2(20,1), Vector2(3,self.UIs["ColorPickerBackground"].GetSizePercent().y-2), (50,75,50))
        self.UIs["BlueSliderBackground"], self.UIs["BlueSliderCursor"] = self.CreateSlider(self.UIs["ColorPickerBackground"].GetPosPercent()+Vector2(25,1), Vector2(3,self.UIs["ColorPickerBackground"].GetSizePercent().y-2), (50,50,75))
        
        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
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
            
            self.UIs["ColorPickerCurrColor"].ChangeColor(self.ColorPicker([{self.UIs["RedSliderCursor"],self.UIs["RedSliderBackground"]},{self.UIs["GreenSliderCursor"],self.UIs["GreenSliderBackground"]},{self.UIs["BlueSliderCursor"],self.UIs["BlueSliderBackground"]}]))
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
    
    def ColorPicker(self, RGBSliders):
        curr = []
        for slider, bg in RGBSliders:
            offset = slider.GetPosReal().y - bg.GetPosReal().y
            travel = bg.GetSizeReal().y - slider.GetSizeReal().y
            ratio = con.HANDLER.Clamp(offset / travel, 0,1)
            ratio = 1.0 - ratio
            curr.append(int(ratio * 255))
        return tuple(curr)
    
    def CreateSlider(self, pos:Vector2, size:Vector2, color:tuple) -> UI:
        background = UI(Quad, pos, size, color)
        slider = UI(Circle, Vector2(background.GetPosPercent().x, background.GetPosPercentCenter().y), Vector2(background.GetSizePercent().x, background.GetSizePercent().x), (255,255,255))
        slider.MoveAdd(Vector2(0,slider.GetSizePercent().y)*-0.5)
        
        self.slidersUIs[slider] = background
        
        return background, slider
        
    def ResetScreen(self):
        pass
        
    def Stop(self):
        if self.looping:
            self.looping = False