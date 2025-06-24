import sys
import pygame
import Constants as con

class Handler():
    def ResetScreen(self):
        con.CURRSCREEN.ResetScreen()
    
    def QuitGame(self):
        pygame.quit()
        sys.exit()