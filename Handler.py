import sys
import os
import json
import pygame
import itertools
import Constants as con
from pygame.math import Vector2
from UI import *
from Text import *

class Handler():
    def __init__(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
        
        con.ATTRIBUTESSAVEPATH = Handler.GetResourcePath(con.ATTRIBUTESSAVEPATH)
        con.LOADDATASAVEPATH = Handler.GetResourcePath(con.LOADDATASAVEPATH)
        con.COLORPRESETSSAVEPATH = Handler.GetResourcePath(con.COLORPRESETSSAVEPATH)
    
    def DrawUI(self, main, UIList):
        Handler.CheckColourFormat()
        
        if self.screenWidth != pygame.display.get_surface().get_size()[0] or self.screenHeight != pygame.display.get_surface().get_size()[1]:
            self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
            con.WINDOW_WIDTH = con.SCREENRECT.w = self.screenWidth
            con.WINDOW_HEIGHT = con.SCREENRECT.h = self.screenHeight
            main.ResetScreen()
            
            allItems = list(UIList.values())

            allItems += [
                ui.GetUnderItem()
                for ui in UIList.values()
                if ui.GetUnderItem() is not None
            ]
            allItems = list(itertools.chain.from_iterable([item if isinstance(item, list) else [item] for item in allItems]))

            for ui in sorted(allItems, key=lambda u: u.GetZDist(), reverse=False):
                ui.ResetRect()
                ui.Draw()

        else:
            allItems = list(UIList.values())

            allItems += [
                ui.GetUnderItem()
                for ui in UIList.values()
                if ui.GetUnderItem() is not None
            ]
            
            allItems = list(itertools.chain.from_iterable([item if isinstance(item, list) else [item] for item in allItems]))

            for ui in sorted(allItems, key=lambda u: u.GetZDist(), reverse=False):
                ui.Draw()
    
    def QuitGame(self):
        pygame.quit()
        sys.exit()
        
    @staticmethod
    def CheckColourFormat():
        if Handler.IsTupleClose(tuple(con.BACKGROUNDCOLOR), (0,0,0), 200):
            con.TEXTCOLOR = (255,255,255)
            con.SELECTEDUICOLOR = (10,10,10,255)
            con.INPUTUICOLOR = (30,30,30,255)
        else:
            con.TEXTCOLOR = (0,0,0)
            con.SELECTEDUICOLOR = (50,50,50,255)
            con.INPUTUICOLOR = ((70,70,70,255))
    
    @staticmethod
    def TupleMagnitude(pos: tuple[float, float]) -> float:
        numA, numB = pos
        
        return Vector2(numA, numB).magnitude()

    @staticmethod
    def Clamp(arg:int|float, minArg:int|float, maxArg:int|float) -> int|float:
        return min(max(arg, minArg), maxArg)
    
    @staticmethod
    def Vector2Clamp(arg:Vector2, minArg:Vector2, maxArg:Vector2) -> Vector2:
        return Vector2(Handler.Clamp(arg.x, minArg.x, maxArg.x),Handler.Clamp(arg.y, minArg.y, maxArg.y))
    
    @staticmethod
    def IsTupleClose(t1, t2, tolerance=1) -> bool:
        return all(math.isclose(a, b, abs_tol=tolerance) for a, b in zip(t1, t2))
    
    @staticmethod
    def IsColorPresetClose(p1: dict, p2: dict, tolerance=5) -> bool:
        keys = ["CELLALIVECOLOR", "CELLDEADCOLOR", "CELLUNTOUCHCOLOR", "BACKGROUNDCOLOR"]
        return all(
            key in p1 and key in p2 and Handler.IsTupleClose(p1[key], p2[key], tolerance)
            for key in keys
        )
    
    @staticmethod
    def GetResourcePath(relPath):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relPath)
        return os.path.join(os.path.abspath("."), relPath)