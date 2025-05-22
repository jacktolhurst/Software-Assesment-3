import pygame
import random
import Constants as con
from enum import Enum, auto
from pygame.math import Vector2

class State(Enum):
    DEAD = auto()
    ALIVE = auto()
    PRIZE = auto()
    UNTOUCH = auto()

class Cell():
    def __init__(self, pos: Vector2, state:State=State.DEAD):
        self.pos = pos
        self.color = (0,0,0)
        self.state = None
        self.SetState(state)
        
        self.rect = pygame.Rect(pos.x, pos.y, con.CELLSIZE.x, con.CELLSIZE.y)
        self.basePos = pos
        
        self.onScreen = False

        self.Move()
    
    def SetState(self, state:State):
        self.state = state
        if self.state == State.ALIVE:
            self.color = (255,255,255)
        elif self.state == State.PRIZE:
            self.color = (255,255,0)
        elif self.state == State.UNTOUCH:
            rand = random.randrange(-10,10)
            self.color = (60+rand,60+rand,60+rand)
        else:
            self.color = (0,0,0)

    def CheckMouseCollide(self, mousePos):
        return self.rect.collidepoint(mousePos)

    def IsOnScreen(self):
        self.onScreen =  self.rect.colliderect(con.SCREENRECT)
        return self.onScreen
    
    def Move(self):
        self.rect.x = (self.basePos.x + con.CELLOFFSETT.x)
        self.rect.y = (self.basePos.y + con.CELLOFFSETT.y)

    def Draw(self):
        if self.onScreen:
            pygame.draw.rect(con.SCREEN,
                            self.color,
                            self.rect)