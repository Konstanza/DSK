'''
Created on 17 mar. 2017

@author: Konstanza
'''

import pygame
import math
import Misc
import Weapons
from Control import Keyboard, Mouse
from Control import RemoteKeyboard, RemoteMouse
import Maps

class PlayerEnemyClient():
    def __init__(self, playerData, mapId):
        self.playerId = playerData[0]
        self.x = playerData[1]
        self.y = playerData[2]
        
        self.deg = playerData[3]
    
        self.mapId = mapId
        self.map = Maps.maps[self.mapId]
        
        self.ship = pygame.image.load(Misc.players[self.playerId])
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        self.radius = int(math.hypot(self.shipRect.x-self.shipRect.centerx, self.shipRect.y-self.shipRect.centery))
    
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId
        
    def loadData(self, data, mapId):
        if data is not None:
            self.x = data[1]
            self.y = data[2]
            self.deg = data[3]
            
            if mapId != self.mapId:
                self.map.remove_player(self)
        
    def draw(self, surface):
        surface.blit(self.rotatedShip, self.rotatedRect)
    
    def update(self):
        self.shipRect.center = (self.x, self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        
        
class PlayerEnemyHost():
    def __init__(self, playerId, x, y, mapId):
        self.playerId = playerId
        self.x = x
        self.y = y
        
        self.deg = 0
        self.score = 0
        self.speed = 5
        self.energy = 100
        self.shield = 100
        self.weapon = Weapons.BasicWeapon(self)
        
        self.mapId = mapId
        self.map = Maps.maps[self.mapId]
        self.planet = self.map.planets[0]
        
        self.keyboard = RemoteKeyboard()
        self.mouse = RemoteMouse()
        
        self.ship = pygame.image.load(Misc.players[self.playerId])
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        self.radius = int(math.hypot(self.shipRect.x-self.shipRect.centerx, self.shipRect.y-self.shipRect.centery))
        
        self.inPortal = None
        self.inRect = False
        
        self.direction = ''
    
    def getEnemyDataForClientMap(self):
        data = [self.playerId, self.x, self.y, self.deg]
        return data
    
    def getPlayerDataForClient(self):
        args = [self.playerId, self.x, self.y, self.mapId, self.energy, self.shield]
        data = {"PlayerDataForClient": args}
        return data
    
    def loadDataFromClient(self, data):
        if data is not None:
            self.keyboard.keyPressed = data[1]
            self.mouse.buttonPressed = data[2]
            self.inRect = data[3]
            self.deg = data[4]
            self.direction = data[5]
        
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId
    
    def setDirection(self, direction):
        self.direction = direction
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self, surface):
        surface.blit(self.rotatedShip, self.rotatedRect)
    
    def move_w(self):
        rad = math.pi*(self.deg+180)/180
        self.x += math.sin(rad)*self.speed
        self.y += math.cos(rad)*self.speed
        self.detect_borders()
        
    def move_s(self):
        rad = math.radians(self.deg)
        self.x += math.sin(rad)*self.speed
        self.y += math.cos(rad)*self.speed
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
            
    def update(self):
        if self.direction == 'w':
            self.move_w()
        elif self.direction == 's':
            self.move_s()
        elif self.direction == 'd':
            self.move_d()
        elif self.direction == 'a':
            self.move_a()
        elif self.keyboard.keyPressed["moveW"]:
            self.move_w()
            self.direction = 'w'
        elif self.keyboard.keyPressed["moveS"]:
            self.move_s()
            self.direction = 's'
        elif self.keyboard.keyPressed["moveD"]:
            self.move_d()
            self.direction = 'd'
        elif self.keyboard.keyPressed["moveA"]:
            self.move_a()
            self.direction = 'a'
        
        if self.inRect:
            if self.mouse.buttonPressed["shoot"]:
                self.weapon.shoot()
            
        self.weapon.update()
        
        self.direction = ''
        
        self.shipRect.center = (self.x, self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        
class PlayerHost():
    def __init__(self, playerId, x, y, mapId):
        self.playerId = playerId
        self.x = x
        self.y = y
        
        self.deg = 0
        self.score = 0
        self.speed = 5
        self.energy = 100
        self.shield = 100
        self.weapon = Weapons.BasicWeapon(self)
        
        self.mapId = mapId
        self.map = Maps.maps[self.mapId]
        self.planet = self.map.planets[0]
        self.planet.playerId = self.playerId
        
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        
        self.ship = pygame.image.load(Misc.players[self.playerId])
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        self.radius = int(math.hypot(self.shipRect.x-self.shipRect.centerx, self.shipRect.y-self.shipRect.centery))
        
        self.display = Misc.gameSurface
        self.disRect = Misc.gameRect
        self.inRect = False
        self.inPortal = None
        
        self.direction = ''
    
    def getEnemyDataForClientMap(self):
        data = [self.playerId, self.x, self.y, self.deg]
        return data
    
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId 
        
    def setMousePosition(self, mouseX, mouseY):
        if self.disRect.collidepoint((mouseX, mouseY)):
            self.inRect = True
            self.mouse.setPosition(mouseX, mouseY)
        else:
            self.inRect = False
    
    def setDirection(self, direction):
        self.direction = direction
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
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
        
        mouseX = self.mouse.remote.mouseX-self.disRect.x
        mouseY = self.mouse.remote.mouseY-self.disRect.y
        oc = -mouseY+(y)
        ac = mouseX-(x)
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
        rad = math.pi*(self.deg+180)/180
        self.x += math.sin(rad)*self.speed
        self.y += math.cos(rad)*self.speed
        self.detect_borders()
        
    def move_s(self):
        rad = math.pi*(self.deg)/180
        self.x += math.sin(rad)*self.speed
        self.y += math.cos(rad)*self.speed
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
        
        self.rotatedRect = rotatedShip.copy()
        self.rotatedRect = rotatedShip.get_rect(centerx = self.x, centery = self.y)
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
            back.blit(rotatedShip, self.rotatedRect)
            self.display.blit(back, (x, y))
        else:
            self.display.blit(back, (self.display.get_width()/2-self.x, self.display.get_height()/2-self.y))
            self.display.blit(rotatedShip, rotatedShipRect)
            
        if Misc.debug:
            r = 50
            cX = self.display.get_width()/2
            cY = self.display.get_height()/2
            mouseX = self.mouse.remote.mouseX-self.disRect.x
            mouseY = self.mouse.remote.mouseY-self.disRect.y
            
            pF = (cX+self.dirX*r, cY+self.dirY*r)
            
            rad = math.pi*(self.deg-90)/180
            pR = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
        
            rad = math.pi*(self.deg+90)/180
            pL = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            pygame.draw.polygon(self.display, Misc.WHITE, [(cX,cY),(mouseX, cY),(mouseX,mouseY)], 1)
            pygame.draw.line(self.display, Misc.RED, (cX, cY), pF, 1)
            pygame.draw.line(self.display, Misc.GREEN, (cX, cY), pR, 1)
            pygame.draw.line(self.display, Misc.BLUE, (cX, cY), pL, 1)
    
    def updateMouseButtons(self):
        self.mouse.updateButtons()
    
    def updateKeyboard(self):
        self.keyboard.update()
        
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
        
        if self.inRect:
            if self.mouse.isButtonPressed("shoot"):
                self.weapon.shoot()
            
        self.weapon.update()
        
        self.direction = ''
        
        self.shipRect.center = (self.x, self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)

class PlayerClient():
    def __init__(self, playerData):
        self.playerId = playerData[0]
        self.x = playerData[1]
        self.y = playerData[2]
        
        self.deg = 0
        
        self.speed = 5
        
        self.mapId = playerData[3]
        self.map = Maps.maps[self.mapId]
        
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        
        self.ship = pygame.image.load(Misc.players[self.playerId])
        self.shipRect = self.ship.get_rect(centerx = self.x, centery = self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        self.radius = int(math.hypot(self.shipRect.x-self.shipRect.centerx, self.shipRect.y-self.shipRect.centery))
        
        self.display = Misc.gameSurface
        self.disRect = Misc.gameRect
        self.inRect = False
        self.inPortal = None
        
        self.direction = ''
    
    def loadData(self, data):
        if data is not None:
            self.x = data[1]
            self.y = data[2]
            
            Maps.maps[data[3]].add_player(self)
        
    def getData(self):
        args = [ self.playerId, self.keyboard.remote.keyPressed, self.mouse.remote.buttonPressed, self.inRect, self.deg, self.direction]
        data = {"PlayerDataForHost": args}
        return data
    
    def setMap(self, map1):
        self.map = map1
        self.mapId = map1.mapId 
        
    def setMousePosition(self, mouseX, mouseY):
        if self.disRect.collidepoint((mouseX, mouseY)):
            self.inRect = True
            self.mouse.setPosition(mouseX, mouseY)
        else:
            self.inRect = False
    
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
            
        mouseX = self.mouse.remote.mouseX-self.disRect.x
        mouseY = self.mouse.remote.mouseY-self.disRect.y
        oc = -mouseY+(y)
        ac = mouseX-(x)
        h = math.sqrt(oc*oc+ac*ac)
        if h >= 20:
            self.deg = math.atan2(oc, ac)*180/math.pi
            self.deg -= 90
    
    def draw(self):
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
            back.blit(self.rotatedShip, self.rotatedRect)
            self.display.blit(back, (x, y))
        else:
            rotatedShipRect = self.rotatedShip.get_rect()
            rotatedShipRect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
            self.display.blit(back, (self.display.get_width()/2-self.x, self.display.get_height()/2-self.y))
            self.display.blit(self.rotatedShip, rotatedShipRect)
            
        if Misc.debug:
            r = 50
            cX = self.display.get_width()/2
            cY = self.display.get_height()/2
            mouseX = self.mouse.remote.mouseX-self.disRect.x
            mouseY = self.mouse.remote.mouseY-self.disRect.y
            
            rad = math.pi*(self.deg+180)/180
            pF = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            rad = math.pi*(self.deg-90)/180
            pR = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
        
            rad = math.pi*(self.deg+90)/180
            pL = (cX+math.sin(rad)*r, cY+math.cos(rad)*r)
            
            pygame.draw.polygon(self.display, Misc.WHITE, [(cX,cY),(mouseX, cY),(mouseX,mouseY)], 1)
            pygame.draw.line(self.display, Misc.RED, (cX, cY), pF, 1)
            pygame.draw.line(self.display, Misc.GREEN, (cX, cY), pR, 1)
            pygame.draw.line(self.display, Misc.BLUE, (cX, cY), pL, 1)
    
    def update(self):
        self.change_dir()
        self.shipRect.center = (self.x, self.y)
        self.rotatedShip = pygame.transform.rotate(self.ship, self.deg)
        self.rotatedRect = self.rotatedShip.get_rect(centerx = self.x, centery = self.y)
        
        
        
        