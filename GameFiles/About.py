import pygame
import json
import random
from pygame.locals import *
from pygame.math import *
import Constants as con
from UI import *
from Text import *
from Grid import *
from SandboxLevel import SandBoxLVL
from Settings import Settings

class About():
    def __init__(self):
        self.looping = False
        
        self.UIs = {}
        
        self.currCursor = None
        
        self.Start()
    
    def Start(self):
        self.looping = True
        
        self.ResetScreen()
        
        self.Update()
    
    def Update(self):
        while self.looping:
            currTime = pygame.time.get_ticks()

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
                    if event.button == 1:
                        if self.UIs["ExitText"].CheckCollidePoint(mousePos):
                            self.Stop()
                if event.type == QUIT:
                        con.HANDLER.QuitGame()
            
            self.DrawEverything()
    
    def DrawEverything(self):
        con.SCREEN.fill(con.BACKGROUNDCOLOR)
        
        con.HANDLER.DrawUI(self, self.UIs)
        
        pygame.display.update()
    
    def ResetScreen(self):
        self.UIs["HowToPlay"] = Text("How To Play:", Vector2(30,5), 20, con.TEXTCOLOR)
        self.UIs["HowToPlaySteps"] = Text(" 1. Drag the cursor around the grid, each Left click will awaken a cell. \n 2. Drag the cursor around the grid, each Right click will kill a cell. \n 3. Press the top left arrow to play the scene. Watch the cells interact! \n 4. Holding the Middle Mouse Button and moving the mouse will move \n the perspective. \n 5. Scrolling will zoom in and out. \n 6. Pressing the grey button on the top right will show the grid options.", self.UIs["HowToPlay"].GetBgRectCentrePercent()+Vector2(0,self.UIs["HowToPlay"].GetRectSize().y), 10, con.TEXTCOLOR, bgColor=(70,70,70))
        self.UIs["HowToPlaySteps"].MoveAdd(Vector2(self.UIs["HowToPlaySteps"].GetBgRectSize().x,0)*-0.5)
        
        self.UIs["KeyShortcuts"] = Text("Key Shortcuts:", Vector2(UI.GetEdgeXPercentage()-40, 5), 20, con.TEXTCOLOR)
        self.UIs["KeyShortcuts"].MoveAdd(Vector2(self.UIs["KeyShortcuts"].GetBgRectSize().x,0)*-0.5)
        self.UIs["KeyShortcutsSteps"] = Text(" P. Turns play mode on or off. \n S. Hotkey to the Grid Settings. \n R. Resets the grid. \n Q. Quits the current screen (works on all screens). \n C. Selects the centre Cell as Alive. \n U. Selects a random Cell as Alive.", self.UIs["KeyShortcuts"].GetBgRectCentrePercent()+Vector2(0,self.UIs["KeyShortcuts"].GetRectSize().y), 10, con.TEXTCOLOR, bgColor=(70,70,70))
        self.UIs["KeyShortcutsSteps"].MoveAdd(Vector2(self.UIs["KeyShortcutsSteps"].GetBgRectSize().x,0)*-0.5)

        self.UIs["ExitText"] = Text("Exit", Vector2(UI.GetEdgeXPercentage(),UI.GetEdgeYPercentage()) - Vector2(2.5,3), 15, (0,0,0), bgColor=(255,0,0,255))
        self.UIs["ExitText"].MoveAdd(UI.RealSizeToPercent(Vector2(*self.UIs["ExitText"].GetRect().size))*-1)
        
    def Stop(self):
        if self.looping:
            self.looping = False