'''
Created on 17 mar. 2017

@author: Konstanza
'''

import pygame
import math
import Misc
from Weapons import Weapon
from Control import Keyboard, Mouse
from Control import RemoteKeyboard, RemoteMouse
import Maps

class Player1():
    '''
    classdocs
    '''

    def __init__(self, display, x, y, ship, power = 0, shield = 0):
        '''
        Constructor
        '''
        
        "Posibles variables"
        self.weapon = Weapon(Misc.basicWeapon)
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
        
    def setMap(self, map1):
        self.map = map1

    def switchDebug(self):
        self.debug = not self.debug
    
    def setDirection(self, direction):
        self.direction = direction
        
    def setMousePosition(self, x, y):
        self.mouseX = x
        self.mouseY = y
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def update(self):
        
        
        pressed = pygame.key.get_pressed()
        
        if self.direction == 'w':
            self.move_w()
        elif self.direction == 's':
            self.move_s()
        elif self.direction == 'd':
            self.move_d()
        elif self.direction == 'a':
            self.move_a()
        elif pressed[pygame.K_w]:
            self.move_w()
            self.direction = 'w'
        elif pressed[pygame.K_s]:
            self.move_s()
            self.direction = 's'
        elif pressed[pygame.K_d]:
            self.move_d()
            self.direction = 'd'
        elif pressed[pygame.K_a]:
            self.move_a()
            self.direction = 'a'
            
        
        self.change_dir()
        
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            shot = self.weapon.shoot(self)
            
            if shot is not None:
                #print(shot.x, shot.y)
                self.map.shots.append(shot)
        
        self.weapon.update()
        
        self.direction = ''
        
        self.shipRect.center = (self.x, self.y)
    
    def change_dir(self):
        backRect = self.map.background.get_rect()
        disRect = self.display.get_rect()
        
        if self.x > backRect.width - disRect.width/2:
            x = self.x-(backRect.width-disRect.width)
        elif self.x < disRect.width/2:
            x = self.x
        else:
            x = self.display.get_width()/2
        
        if self.y > backRect.height - disRect.height/2:
            y = self.y-(backRect.height-disRect.height)
        elif self.y < disRect.height/2:
            y = self.y
        else:
            y = self.display.get_height()/2
            
        oc = -self.mouseY+(y)
        ac = self.mouseX-(x)
        h = math.sqrt(oc*oc+ac*ac)
        if h >= 20:
            self.deg = math.atan2(oc, ac)*180/math.pi
            self.deg -= 90
            self.dirX = ac/h
            self.dirY = -oc/h
            
    def detect_borders(self):
        backRect = self.map.background.get_rect()
        
        if self.x > backRect.width - self.shipRect.width/2:
            self.x = backRect.width - self.shipRect.width/2
        elif self.x < self.shipRect.width/2:
            self.x = self.shipRect.width/2
        
        if self.y > backRect.height - self.shipRect.height/2:
            self.y = backRect.height - self.shipRect.height/2
        elif self.y < self.shipRect.height/2:
            self.y = self.shipRect.height/2
    
    def move_w(self):
        self.x += self.dirX*self.speed
        self.y += self.dirY*self.speed
        
        self.detect_borders()
         
    def move_s(self):
        self.x -= self.dirX*self.speed
        self.y -= self.dirY*self.speed
        self.detect_borders()
    
    def move_d(self):
        rad = math.pi*(self.deg+90)/180
        self.y += math.cos(rad)*self.speed
        self.x += math.sin(rad)*self.speed
        self.detect_borders()
    
    def move_a(self):
        rad = math.pi*(self.deg-90)/180
        self.y += math.cos(rad)*self.speed
        self.x += math.sin(rad)*self.speed
        self.detect_borders()
        
    def draw(self):
        
        rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        rotatedShipRect = rotatedShip.get_rect()
        rotatedShipRect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
        
        self.rotatedShipRect = rotatedShip.copy()
        self.rotatedShipRect = rotatedShip.get_rect(centerx = self.x, centery = self.y)
        back = self.map.draw(self)
        backRect = back.get_rect()
        disRect = self.display.get_rect()
        
        
        b = False
        if self.x > backRect.width - disRect.width/2:
            x = -(backRect.width - disRect.width)
            b = True
        elif self.x < disRect.width/2:
            x = 0
            b = True
        else:
            x = self.display.get_width()/2-self.x
            
        if self.y > backRect.height - disRect.height/2:
            y = -(backRect.height - disRect.height)
            b = True
        elif self.y < disRect.height/2:
            y = 0
            b = True
        else:
            y = self.display.get_height()/2-self.y
            
            
        if b:
            back.blit(rotatedShip, self.rotatedShipRect)
            self.display.blit(back, (x, y))
        else:
            self.display.blit(back, (self.display.get_width()/2-self.x, self.display.get_height()/2-self.y))
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
            
            pygame.draw.polygon(self.display, Misc.WHITE, [(cX,cY),(self.mouseX, cY),(self.mouseX,self.mouseY)], 1)
            pygame.draw.line(self.display, Misc.RED, (cX, cY), pF, 1)
            pygame.draw.line(self.display, Misc.GREEN, (cX, cY), pR, 1)
            pygame.draw.line(self.display, Misc.BLUE, (cX, cY), pL, 1)

class Player2():
    '''
    classdocs
    '''

    def __init__(self, display, x, y, ship, power = 0, shield = 0):
        '''
        Constructor
        '''
        
        "Posibles variables"
        self.weapon = Weapon(Misc.basicWeapon)
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
    
    def change_dir(self):
        backRect = self.map.background.get_rect()
        disRect = self.display.get_rect()
        
        if self.x > backRect.width - disRect.width/2:
            x = self.x-(backRect.width-disRect.width)
        elif self.x < disRect.width/2:
            x = self.x
        else:
            x = self.display.get_width()/2
        
        if self.y > backRect.height - disRect.height/2:
            y = self.y-(backRect.height-disRect.height)
        elif self.y < disRect.height/2:
            y = self.y
        else:
            y = self.display.get_height()/2
            
        oc = -self.mouseY+(y)
        ac = self.mouseX-(x)
        h = math.sqrt(oc*oc+ac*ac)
        if h >= 20:
            self.deg = math.atan2(oc, ac)*180/math.pi
            self.deg -= 90
            self.dirX = ac/h
            self.dirY = -oc/h
            
    def setMousePosition(self, x, y):
        self.mouseX = x
        self.mouseY = y
        
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
        rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        rotatedShipRect = rotatedShip.get_rect(centerx = self.x, centery = self.y)
        
        surface.blit(rotatedShip, rotatedShipRect)

class PlayerData():
    def __init__(self, playerId, x, y, deg, mapId):
        self.playerId = playerId
        self.x = x
        self.y = y
        self.deg = deg
        self.mapId = mapId
    
    def __str__(self):
        return str((self.playerId, self.x, self.y, self.deg, self.mapId))

class PlayerClient():
    def __init__(self, playerData):
        self.playerData = playerData
        self.keyboardData = RemoteKeyboard()
        
        self.ship = Misc.players[self.playerData.playerId].copy()
        self.shipRect = self.ship.get_rect(centerx = self.playerData.x, centery = self.playerData.y)
        
        self.inPortal = None
    
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId
        
    def draw(self, surface):
        rotatedShip = pygame.transform.rotate(self.ship, self.playerData.deg)
        rotatedShipRect = rotatedShip.get_rect(centerx = self.playerData.x, centery = self.playerData.y)
        
        surface.blit(rotatedShip, rotatedShipRect)
    
    def update(self):
        pass
    
class PlayerHost():
    def __init__(self, playerData):
        self.playerId = playerData.playerId
        self.x = playerData.x
        self.y = playerData.y
        
        self.deg = playerData.deg
        rad = math.pi*(self.deg)/180
        self.dirX = math.sin(rad)
        self.dirY = math.cos(rad)
        
        self.speed = 5
        
        self.mapId = playerData.mapId
        self.map = Maps.maps[self.mapId]
        
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        
        self.ship = Misc.players[self.playerId].copy()
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        
        self.display = Misc.display
        self.inPortal = None
        
        self.direction = ''
    
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId 
        
    def setMousePosition(self, mouseX, mouseY):
        self.mouse.setPosition(mouseX, mouseY)
    
    def setDirection(self, direction):
        self.direction = direction
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def updateMouseButtons(self):
        self.mouse.updateButtons()
    
    def updateKeyboard(self):
        self.keyboard.update()
        
    def change_dir(self):
        backRect = self.map.background.get_rect()
        disRect = self.display.get_rect()
        
        if self.x > backRect.width - disRect.width/2:
            x = self.x-(backRect.width-disRect.width)
        elif self.x < disRect.width/2:
            x = self.x
        else:
            x = self.display.get_width()/2
        
        if self.y > backRect.height - disRect.height/2:
            y = self.y-(backRect.height-disRect.height)
        elif self.y < disRect.height/2:
            y = self.y
        else:
            y = self.display.get_height()/2
            
        oc = -self.mouse.remote.mouseY+(y)
        ac = self.mouse.remote.mouseX-(x)
        h = math.sqrt(oc*oc+ac*ac)
        if h >= 20:
            self.deg = math.atan2(oc, ac)*180/math.pi
            self.deg -= 90
            self.dirX = ac/h
            self.dirY = -oc/h
    
    def detect_borders(self):
        backRect = self.map.background.get_rect()
        
        if self.x > backRect.width - self.shipRect.width/2:
            self.x = backRect.width - self.shipRect.width/2
        elif self.x < self.shipRect.width/2:
            self.x = self.shipRect.width/2
        
        if self.y > backRect.height - self.shipRect.height/2:
            self.y = backRect.height - self.shipRect.height/2
        elif self.y < self.shipRect.height/2:
            self.y = self.shipRect.height/2
    
    def move_w(self):
        self.x += self.dirX*self.speed
        self.y += self.dirY*self.speed
        
        self.detect_borders()
         
    def move_s(self):
        self.x -= self.dirX*self.speed
        self.y -= self.dirY*self.speed
        self.detect_borders()
    
    def move_d(self):
        rad = math.pi*(self.deg+90)/180
        self.y += math.cos(rad)*self.speed
        self.x += math.sin(rad)*self.speed
        self.detect_borders()
    
    def move_a(self):
        rad = math.pi*(self.deg-90)/180
        self.y += math.cos(rad)*self.speed
        self.x += math.sin(rad)*self.speed
        self.detect_borders()
        
    def draw(self):
        rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        rotatedShipRect = rotatedShip.get_rect()
        rotatedShipRect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
        
        self.rotatedShipRect = rotatedShip.copy()
        self.rotatedShipRect = rotatedShip.get_rect(centerx = self.x, centery = self.y)
        back = self.map.draw(self)
        backRect = back.get_rect()
        disRect = self.display.get_rect()
        
        
        b = False
        if self.x > backRect.width - disRect.width/2:
            x = -(backRect.width - disRect.width)
            b = True
        elif self.x < disRect.width/2:
            x = 0
            b = True
        else:
            x = self.display.get_width()/2-self.x
            
        if self.y > backRect.height - disRect.height/2:
            y = -(backRect.height - disRect.height)
            b = True
        elif self.y < disRect.height/2:
            y = 0
            b = True
        else:
            y = self.display.get_height()/2-self.y
            
            
        if b:
            back.blit(rotatedShip, self.rotatedShipRect)
            self.display.blit(back, (x, y))
        else:
            self.display.blit(back, (self.display.get_width()/2-self.x, self.display.get_height()/2-self.y))
            self.display.blit(rotatedShip, rotatedShipRect)
            
        if Misc.debug:
            r = 50
            cX = self.display.get_width()/2
            cY = self.display.get_height()/2
            
            pF = (cX+self.dirX*r, cY+self.dirY*r)
            
            rad = math.pi*(self.deg-90)/180
            pR = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
        
            rad = math.pi*(self.deg+90)/180
            pL = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            pygame.draw.polygon(self.display, Misc.WHITE, [(cX,cY),(self.mouse.remote.mouseX, cY),(self.mouse.remote.mouseX,self.mouse.remote.mouseY)], 1)
            pygame.draw.line(self.display, Misc.RED, (cX, cY), pF, 1)
            pygame.draw.line(self.display, Misc.GREEN, (cX, cY), pR, 1)
            pygame.draw.line(self.display, Misc.BLUE, (cX, cY), pL, 1)
    
    def update(self):
        
        if self.direction == 'w':
            self.move_w()
        elif self.direction == 's':
            self.move_s()
        elif self.direction == 'd':
            self.move_d()
        elif self.direction == 'a':
            self.move_a()
        elif self.keyboard.isKeyPressed("moveW"):
            self.move_w()
            self.direction = 'w'
        elif self.keyboard.isKeyPressed("moveS"):
            self.move_s()
            self.direction = 's'
        elif self.keyboard.isKeyPressed("moveD"):
            self.move_d()
            self.direction = 'd'
        elif self.keyboard.isKeyPressed("moveA"):
            self.move_a()
            self.direction = 'a'
            
        self.change_dir()
        
        self.direction = ''
        
        self.shipRect.center = (self.x, self.y)
        
        
        
        