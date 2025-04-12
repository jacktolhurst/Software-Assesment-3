import pygame
import numpy
import Constants as con

class Camera:
    def __init__(self):
        self.offest = (0,0)
        self.pos = pygame.Vector2(0, 0)
        
        self.zoom = 1.0
        
        self.rect = pygame.Rect(0, 0, con.WINDOW_WIDTH, con.WINDOW_HEIGHT)
        
        self.panning = False
        self.initialClickPos = None
    
    def Apply(self, targetRect):
        adjustedRect = targetRect.copy()
        adjustedRect.x = (targetRect.x - self.rect.x) * self.zoom
        adjustedRect.y = (targetRect.y - self.rect.y) * self.zoom
        adjustedRect.width *= self.zoom
        adjustedRect.height *= self.zoom
        return adjustedRect
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.zoom += event.y * 0.1
                self.zoom = max(0.2, min(self.zoom, 5))
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.panning = True
                    self.initialClickPos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.panning = False
                    self.initialClickPos = None
        
        if self.panning:
            currentMousePos = pygame.mouse.get_pos()
            
            difference = pygame.Vector2(self.initialClickPos) - pygame.Vector2(currentMousePos)
            
            self.rect.x += difference.x
            self.rect.y += difference.y
            
            self.initialClickPos = currentMousePos
            