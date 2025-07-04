import sys
import pygame
import Constants as con
from pygame.math import Vector2

class Handler():
    def __init__(self):
        self.screenWidth, self.screenHeight = pygame.display.get_surface().get_size()
    
    def DrawUI(self, main, UIList):
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

            for ui in sorted(allItems, key=lambda u: u.GetZDist(), reverse=False):
                ui.Draw()
    
    def QuitGame(self):
        pygame.quit()
        sys.exit()
    
    @staticmethod
    def TupleMagnitude(pos: tuple[float, float]) -> float:
        numA, numB = pos
        
        return Vector2(numA, numB).magnitude()

    @staticmethod
    def Clamp(arg:int|float, minArg:int|float, maxArg:int|float) -> int|float:
        return min(max(arg, minArg), maxArg)