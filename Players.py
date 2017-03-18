'''
Created on 17 mar. 2017

@author: Konstanza
'''

import pygame
import math

class Player1():
    '''
    classdocs
    '''

    def __init__(self, x, y, ship, power = 0, shield = 0):
        '''
        Constructor
        '''
        
        "Posibles variables"
        self.ship = ship
        self.power = power
        self.shield = shield
        
        self.x = x
        self.y = y
        self.deg = 0     
        self.dirX = 0
        self.dirY = -1   
        self.speed = 5     
        
    def update(self, superficie, mouseX, mouseY):
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.x -= self.dirX*self.speed
            self.y -= self.dirY*self.speed
        if pressed[pygame.K_s]:
            self.x += self.dirX*self.speed
            self.y += self.dirY*self.speed
        if pressed[pygame.K_d]:
            rad = math.pi*(self.deg-90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
        if pressed[pygame.K_a]:
            rad = math.pi*(self.deg+90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
            
        oc = -mouseY+(superficie.get_height()/2)
        ac = mouseX-(superficie.get_width()/2)
        h = math.sqrt(oc*oc+ac*ac)
        self.deg = math.atan2(oc, ac)*180/math.pi
        self.deg -= 90
        self.dirX = ac/h
        self.dirY = -oc/h
        
    def draw(self, surface, mouseX, mouseY, debug):
        rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        rotatedShipRect = rotatedShip.get_rect()
        rotatedShipRect.center = (surface.get_width() / 2, surface.get_height() / 2)
        surface.blit(rotatedShip, rotatedShipRect)
      
        if debug:
            r = 50
            cX = surface.get_width()/2
            cY = surface.get_height()/2
            
            pF = (cX+self.dirX*r, cY+self.dirY*r)
            
            rad = math.pi*(self.deg-90)/180
            pR = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
        
            rad = math.pi*(self.deg+90)/180
            pL = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            pygame.draw.polygon(surface, (255,255,255), [(cX,cY),(mouseX, cY),(mouseX,mouseY)], 1)
            pygame.draw.line(surface, (255,0,0), (cX, cY), pF, 1)
            pygame.draw.line(surface, (0,255,0), (cX, cY), pR, 1)
            pygame.draw.line(surface, (0,0,255), (cX, cY), pL, 1)
