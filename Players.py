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
        elif pressed[pygame.K_s]:
            self.x += self.dirX*self.speed
            self.y += self.dirY*self.speed
        elif pressed[pygame.K_d]:
            self.y += self.dirY*self.speed
            self.x -= self.dirX*self.speed
        elif pressed[pygame.K_a]:
            self.y -= self.dirY*self.speed
            self.x += self.dirX*self.speed
            
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
        
        cX = surface.get_width()/2
        cY = surface.get_height()/2
    
        if debug:
            pygame.draw.polygon(surface, (255,255,255), [(cX,cY),(mouseX, cY),(mouseX,mouseY)], 1)
            pygame.draw.line(surface, (255,0,0), (cX, cY),(cX+self.dirX*self.speed, cY+self.dirY*self.speed), 1)