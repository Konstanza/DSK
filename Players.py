'''
Created on 17 mar. 2017

@author: Konstanza
'''

import pygame
import math
from Misc import *
from Weapons import Weapon

class Player1():
    '''
    classdocs
    '''

    def __init__(self, display, x, y, ship, power = 0, shield = 0):
        '''
        Constructor
        '''
        
        "Posibles variables"
        self.weapon = Weapon(basicWeapon)
        self.ship = ship
        self.rotatedShipRect = None
        self.power = power
        self.shield = shield
        
        self.direction = 'w'
        self.display = display
        self.x = x
        self.y = y
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        self.deg = 0     
        self.dirX = 0
        self.dirY = -1   
        self.speed = 5
        self.shots = [] 
        self.mouseX = 0
        self.mouseY = 0
        self.debug = False
        self.inPortal = None
        
        
    def switchDebug(self):
        self.debug = not self.debug
        
    def setMousePosition(self, x, y):
        self.mouseX = x
        self.mouseY = y
    
    def setPosition(self, x, y):
        self.X = x
        self.Y = y
    
    def update(self):
        
        
        pressed = pygame.key.get_pressed()
        
        if self.direction == 'w':
            self.x += self.dirX*self.speed
            self.y += self.dirY*self.speed
        elif self.direction == 's':
            self.x -= self.dirX*self.speed
            self.y -= self.dirY*self.speed
        elif self.direction == 'd':
            rad = math.pi*(self.deg+90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
        elif self.direction == 'a':
            rad = math.pi*(self.deg-90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
        elif pressed[pygame.K_w]:
            self.x += self.dirX*self.speed
            self.y += self.dirY*self.speed
            self.direction = 'w'
        elif pressed[pygame.K_s]:
            self.x -= self.dirX*self.speed
            self.y -= self.dirY*self.speed
            self.direction = 's'
        elif pressed[pygame.K_d]:
            rad = math.pi*(self.deg+90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
            self.direction = 'd'
        elif pressed[pygame.K_a]:
            rad = math.pi*(self.deg-90)/180
            self.y += math.cos(rad)*self.speed
            self.x += math.sin(rad)*self.speed
            self.direction = 'a'
            
        
        oc = -self.mouseY+(self.display.get_height()/2)
        ac = self.mouseX-(self.display.get_width()/2)
        h = math.sqrt(oc*oc+ac*ac)
        self.deg = math.atan2(oc, ac)*180/math.pi
        self.deg -= 90
        self.dirX = ac/h
        self.dirY = -oc/h
        
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            shot = self.weapon.shoot(self)
            
            if shot is not None:
                #print(shot.x, shot.y)
                self.shots.append(shot)
        
        self.weapon.update()
        for shot in self.shots:
            shot.update()
        
        self.direction = ''
        
        self.shipRect.center = (self.x, self.y)
        
    def draw(self):
        
        rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        rotatedShipRect = rotatedShip.get_rect()
        rotatedShipRect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
        
        self.rotatedShipRect = rotatedShip.copy()
        self.rotatedShipRect = rotatedShip.get_rect(centerx = self.x, centery = self.y)
        self.map.draw(self)
        
        self.display.blit(rotatedShip, rotatedShipRect)
        
        if self.debug:
            r = 50
            cX = self.display.get_width()/2
            cY = self.display.get_height()/2
            
            pF = (cX+self.dirX*r, cY+self.dirY*r)
            
            rad = math.pi*(self.deg-90)/180
            pR = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
        
            rad = math.pi*(self.deg+90)/180
            pL = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            #pygame.draw.polygon(self.display, WHITE, [(cX,cY),(self.mouseX, cY),(self.mouseX,self.mouseY)], 1)
            #pygame.draw.line(self.display, RED, (cX, cY), pF, 1)
            #pygame.draw.line(self.display, GREEN, (cX, cY), pR, 1)
            #pygame.draw.line(self.display, BLUE, (cX, cY), pL, 1)

class Player2():
    '''
    classdocs
    '''

    def __init__(self, display, x, y, ship, power = 0, shield = 0):
        '''
        Constructor
        '''
        
        "Posibles variables"
        self.weapon = Weapon(basicWeapon)
        self.ship = ship
        
        self.power = power
        self.shield = shield
        
        self.display = display
        self.x = x
        self.y = y
        self.shipRect = ship.get_rect(centerx = self.x, centery = self.y)
        self.deg = 0     
        self.dirX = 0
        self.dirY = -1   
        self.speed = 5    
        self.shots = [] 
        self.mouseX = 0
        self.mouseY = 0
        self.debug = False
        self.inPortal = None
        
    def update(self):
        
        # FALTA TECLADO AQUI
        
        oc = -self.mouseY+(self.display.get_height()/2)
        ac = self.mouseX-(self.display.get_width()/2)
        h = math.sqrt(oc*oc+ac*ac)
        self.deg = math.atan2(oc, ac)*180/math.pi
        self.deg -= 90
        self.dirX = ac/h
        self.dirY = -oc/h
        
        # FALTA MOUSE AQUI
        
        self.weapon.update()
        for shot in self.shots:
            shot.update()
        
        self.shipRect.center = (self.x, self.y)
        
    def draw(self, surface):
        for shot in self.shots:
            shot.draw(surface)
            
        surface.blit(self.ship, self.shipRect)


