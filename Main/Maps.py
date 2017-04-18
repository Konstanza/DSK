'''
Created on 18 mar. 2017

@author: Konstanza
'''
import random
import Misc
import pygame
from pygame import surface
from Vector import Vector
import os
from random import randint
import pyganim
from Players import PlayerEnemyClient

maps = []
portals = []

class RemoteWorld(object):
    
    def __init__(self):
        self.maps = []
        self.portals = []
        
    def __str__(self):
        string = "( maps: "
        
        for map1 in self.maps:
            string += "("+str(map1)+") "
        
        string += ", portals: "
        
        for portal in self.portals:
            string += "("+str(portal)+") "
        
        string += ")"
        return string

class RemotePortal(object):
    
    def __init__(self, x, y, map1Id, mX, mY, map2Id, exitId):
        self.x = x
        self.y = y
        self.mX = mX 
        self.mY = mY
        self.map1Id = map1Id
        self.map2Id = map2Id
        self.exitId = exitId
    
    def __str__(self):
        return str((self.x, self.y, self.map1Id, self.mX, self.mY, self.map2Id, self.exitId))
    
class RemoteMap(object):
    
    def __init__(self, mapId, backgroundId):
        self.mapId = mapId
        self.backgroundId = backgroundId
        
    def __str__(self):
        return str((self.mapId, self.backgroundId))

class RemoteMapForClient(object):
    
    def __init__(self, map1, playerId):
        self.mapId = map1.mapId
        self.players = {}
        
        for key in map1.players:
            if key != playerId:
                player = map1.players[key]
                self.players[player.playerId] = player.getEnemyDataForClientMap()
        
    def __str__(self):
        return str((self.mapId, str(self.players)))
    
class Map(object):
    '''
    classdocs
    '''

    def __init__(self, mapId, backgroundId):
        '''
        Constructor
        '''
        self.mapId = mapId
        self.backgroundId = backgroundId
        self.background = Misc.backgrounds[self.backgroundId]
        self.players = {}
        self.objects = []
        self.portals = []
        self.shots = []
    
    def add_portal(self, portal):
        self.portals.append(portal)

    def loadMap(self, data):
        if data is not None:
            for key in data.players:
                playerData = data.players[key]
                
                if key in self.players:
                    self.players[key].loadData(playerData, data.mapId)
                else:
                    self.add_player(PlayerEnemyClient(playerData, data.mapId))
                
    def getMap(self, player):
        return RemoteMapForClient(self, player.playerId)
    
    def draw(self, p1):
        
        back = self.background.copy()
        
        for obj in self.objects:
            obj.draw(back)
            
        for portal in self.portals:
            portal.draw(back)
            
        for key in self.players:
            player = self.players[key]
            if player != p1:
                player.draw(back)
        
        for shot in self.shots:
            shot.draw(back, Misc.debug)
        
        if Misc.debug:
            pygame.draw.rect(back, Misc.WHITE, p1.rotatedShipRect, 1)
            pygame.draw.rect(back, Misc.RED, p1.shipRect, 1)
            
            """
            u = Vector(p1.dirX*p1.speed, p1.dirY*p1.speed)
            v = Vector(100,100)
            pv = u.vectorProyeccionSobre(v)
            
            pygame.draw.line(back, YELLOW, (p1.x,p1.y), (p1.x+u.x, p1.y+u.y), 1)
            pygame.draw.line(back, MAGENTA, (p1.x,p1.y), (p1.x+v.x, p1.y+v.y), 1)
            pygame.draw.line(back, GREEN, (p1.x,p1.y), (p1.x+pv.x, p1.y+pv.y), 1)"""
        
        return back
            
    def update(self):
            
        for key in self.players:
            player = self.players[key]
            player.update()
        
        for obj in self.objects:
            obj.update()
            
        for portal in self.portals:
            portal.update()
            
        for shot in self.shots:
            shot.update()
    
    def add_player(self, player):
        self.players[player.playerId] = player
        player.setMap(self)
    
    def remove_player(self, player):
        del self.players[player.playerId]
    
class Portal():
    def __init__(self, x, y, map1Id, mX, mY, map2Id, exitId = None):
        self.x = x
        self.y = y
        self.mX = mX 
        self.mY = mY
        self.map1Id = map1Id
        self.map2Id = map2Id
        self.exitId = exitId
        self.map1 = maps[map1Id]
        self.map2 = maps[map2Id]
        self.image = Misc.portalImage.copy()
        
        if exitId is not None:
            self.exit = portals[exitId]
        else:
            self.exit = None
            
        self.rect = self.image.get_rect(centerx = self.x, centery = self.y)
        
        l = []
        for i in range(1,9):
            l.append((os.path.join(Misc.IMAGE_PATH, 'black-hole-warp128-'+str(i)+'.png'), 0.1))
        
        self.anim = pyganim.PygAnimation(l)
        self.anim.play()
    
    def update(self):
        # DETECT COLLISION
        for key in self.map1.players.keys():
            player = self.map1.players[key]
            if self.exit != None:
                if player.inPortal != self.exit:
                    if self.collision(player):
                        player.inPortal = self
                        self.map1.remove_player(player)
                        self.map2.add_player(player)
                
                        player.setDirection('')
                        player.setPosition(self.mX, self.mY)
                else:
                    if not self.collision(player):
                        player.inPortal = None
            else:
                if self.collision(player):
                    player.inPortal = self
                    self.map1.remove_player(player)
                    self.map2.add_player(player)
                
                    player.setDirection('')
                    player.setPosition(self.mX, self.mY)
                
    
    def collision(self, player):
        if self.rect.colliderect(player.shipRect):
            return True
        return False
        
    def draw(self, surface):
        #surface.blit(self.image, self.rect)
        if Misc.debug:
            pygame.draw.circle(surface, Misc.YELLOW, (self.x, self.y), 50, 5)
        self.anim.blit(surface, self.rect)
        

def generate_world_teaser():
    global maps
    maps = []
    
    maps.append(Map(0,4))
    maps.append(Map(1,2))
    maps.append(Map(2,3))
    
    p1 = Portal(400, 500, 0, 695, 240, 1)
    p2 = Portal(800, 500, 0, 100, 100, 2)
    
    p3 = Portal(695, 240, 1, 400, 500, 0, p1)
    p4 = Portal(100, 100, 2, 800, 500, 0, p2)
    
    p1.exit = p3
    p2.exit = p4
    
    maps[0].add_portal(p1)
    maps[0].add_portal(p2)
    maps[1].add_portal(p3)
    maps[2].add_portal(p4)
    
def generate_world(minim, maxim = None):
    global maps, portals
    if maxim is None:
        maxim = minim
    maps = []
    portals = []
    mapsCount = random.randint(minim,maxim)
    print(mapsCount, "maps")
    
    for i in range(mapsCount):
        maps.append(Map(i, random.randint(0,len(Misc.backgrounds)-1)))
    
    for i in range(mapsCount-1):
        portalRect = Misc.portalImage.get_rect()
        map1 = maps[i]
        map2 = maps[i+1]
        map1Rect = map1.background.get_rect()
        map2Rect = map2.background.get_rect()
        
        col = True
        while col:
            col = False
            p1 = Portal(random.randint(portalRect.centerx, map1Rect.width-portalRect.centerx), random.randint(portalRect.centery, map1Rect.height-portalRect.centery), i, randint(70, map2Rect.width-70), randint(70, map2Rect.height-70), i+1)
         
            for portal in map1.portals:
                if portal.rect.colliderect(p1):
                    col = True
        
        map1.add_portal(p1)
        portals.append(p1)
        lastPortal = len(portals)-1
        
        p2 = Portal(p1.mX, p1.mY, i+1, p1.x, p1.y, i, lastPortal)
        map2.add_portal(p2)
        portals.append(p2)
        
        p1.exitId = lastPortal+1
        p1.exit = p2
        
    
def get_world():
    global maps, portals
    
    remote = RemoteWorld()
    
    for map1 in maps:
        remote.maps.append(RemoteMap(map1.mapId, map1.backgroundId))
    
    for portal in portals:
        remote.portals.append(RemotePortal(portal.x, portal.y, portal.map1Id, portal.mX, portal.mY, portal.map2Id, portal.exitId))
    
    return remote

def load_world(remote):
    global maps, portals
    maps = []
    portals = []
    mapsCount = len(remote.maps)
    print(mapsCount, "maps")
    
    for map1 in remote.maps:
        maps.append(Map(map1.mapId, map1.backgroundId))
        
    for portal in remote.portals:
        p1 = Portal(portal.x, portal.y, portal.map1Id, portal.mX, portal.mY, portal.map2Id)
        maps[portal.map1Id].add_portal(p1)
        portals.append(p1)
    
    for i in range(len(remote.portals)):
        remotePortal = remote.portals[i]
        if remotePortal.exitId is not None:
            portal = portals[i]
            portal.exitId = remotePortal.exitId
            portal.exit = portals[portal.exitId]
        
def update():
    for ma in maps:
        ma.update()       