import pygame
import Constants as con
from enum import Enum, auto
from pygame.math import *

class State(Enum):
    DEAD = auto()
    ALIVE = auto()
    PRIZE = auto()

class Cell():
    def __init__(self, pos: Vector2, state:State=State.DEAD):
        self.pos = pos
        self.state = state
        self.color = (0,0,0)
        
        if self.state == State.ALIVE:
            self.color = (255,255,255)
        if self.state == State.PRIZE:
            self.color = (255,255,0)
        
        self.rect = pygame.Rect(pos.x, pos.y, con.CELLSIZE.x, con.CELLSIZE.y)
        self.basePos = pos
        self.baseScale = Vector2(self.rect.w, self.rect.h)
        
        self.Move()
    
    def SetState(self, state:State):
        self.state = state
        if self.state == State.ALIVE:
            self.color = (255,255,255)
        elif self.state == State.PRIZE:
            self.color = (255,255,0)
        else:
            self.color = (0,0,0)

    def CheckMouseCollide(self, mousePos):
        return self.rect.collidepoint(mousePos)
    
    def Move(self):
        self.rect.x = (self.basePos.x + con.CELLOFFSETT.x)
        self.rect.y = (self.basePos.y + con.CELLOFFSETT.y)
        
        self.rect.w = self.baseScale.x + con.CELLSCALE
        self.rect.h = self.baseScale.y + con.CELLSCALE

    def Draw(self):
        pygame.draw.rect(con.SCREEN,
                        self.color,
                        self.rect)