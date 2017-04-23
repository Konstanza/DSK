'''
Created on 18 mar. 2017

@author: Konstanza
'''
import random
import Misc
import pygame
from random import randint
import pyganim
from Players import PlayerEnemyClient
from Weapons import ProjectilHost, ProjectilClient

maps = []
portals = []
planets = []

class Planet():
    
    def __init__(self, x, y, imageId, mapId, playerId = None):
        self.mapId = mapId
        self.playerId = playerId
        self.imageId = imageId
        self.image = pygame.image.load(Misc.planets[self.imageId])
        self.rect = self.image.get_rect(centerx = x, centery = y)
        
        self.x = x
        self.y = y
    
    def draw(self, surface):
        if Misc.debug:
            pygame.draw.rect(surface, Misc.WHITE, self.rect, 1)
            
        surface.blit(self.image, self.rect)
    
    def getDataInit(self):
        data = [self.x, self.y, self.imageId, self.mapId, self.playerId]
        return data
    
    def update(self):
        pass

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
        self.background = pygame.image.load(Misc.backgrounds[self.backgroundId])
        self.players = {}
        self.objects = []
        self.portals = []
        self.planets = []
        self.shots = []
    
    def add_portal(self, portal):
        self.portals.append(portal)
        
    def add_planet(self, planet):
        self.planets.append(planet)

    def add_shot(self, shot):
        self.shots.append(shot)

    def getDataInit(self):
        data = [self.mapId, self.backgroundId]
        return data
    
    def loadMap(self, data):
        if data is not None:
            players = data[1]["Player"]
            shots = data[2]["Shot"]
            
            self.players = {}
            for key in players:
                playerData = players[key]
                self.add_player(PlayerEnemyClient(playerData, data[0]))
            
            self.shots = []
            for shot in shots:
                self.add_shot(ProjectilClient(shot))
                
                
    def getMap(self, player):
        data = {"Map": []}
        args = data["Map"]
        
        args.append(self.mapId)
        
        players = {}
        shots = []
        
        args.append({"Player": players})
        args.append({"Shot": shots})
        
        for key in self.players:
            if key != player.playerId:
                player = self.players[key]
                players[key] = player.getEnemyDataForClientMap()
        
        for shot in self.shots:
            shots.append(shot.getData())
            
        return data
    
    def draw(self, p1):
        
        back = self.background.copy()
        
        for obj in self.objects:
            obj.draw(back)
            
        for portal in self.portals:
            portal.draw(back)
            
        for planet in self.planets:
            planet.draw(back)
        
        for shot in self.shots:
            shot.draw(back)
            
        for key in self.players:
            player = self.players[key]
            if player != p1:
                player.draw(back)
        
        if Misc.debug:
            pygame.draw.rect(back, Misc.WHITE, p1.rotatedRect, 1)
            pygame.draw.rect(back, Misc.RED, p1.shipRect, 1)
            pygame.draw.circle(back, Misc.YELLOW, p1.rotatedRect.center, p1.radius, 1)
        
        return back
            
    def update(self):
        
        for key in self.players:
            player = self.players[key]
            player.update()
        
        for planet in self.planets:
            planet.update()
            
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
        
    def remove_shot(self, shot):
        self.shots.remove(shot)
    
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
        self.image = pygame.image.load(Misc.portalImage)
        
        if exitId is not None:
            self.exit = portals[exitId]
        else:
            self.exit = None
            
        self.rect = self.image.get_rect(centerx = self.x, centery = self.y)
        self.radius = 50
        
        l = []
        for i in range(1,Misc.portalAnim["max"]):
            l.append((Misc.portalAnim["path"]+str(i)+Misc.portalAnim["type"], 0.1))
        
        self.anim = pyganim.PygAnimation(l)
        self.anim.play()
    
    def getDataInit(self):
        data = [self.x, self.y, self.map1Id, self.mX, self.mY, self.map2Id, self.exitId]
        return data
    
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
        if self.rect.colliderect(player.rotatedRect):
            return True
        return False
        
    def draw(self, surface):
        if Misc.debug:
            pygame.draw.rect(surface, Misc.WHITE, self.rect, 1)
            pygame.draw.circle(surface, Misc.YELLOW, (self.x, self.y), self.radius, 5)
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
    global maps, portals, planets
    if maxim is None:
        maxim = minim
    maps = []
    portals = []
    planets = []
    
    mapsCount = random.randint(minim,maxim)
    print(mapsCount, "maps")
    
    for i in range(mapsCount):
        maps.append(Map(i, random.randint(0,len(Misc.backgrounds)-1)))
    
    for i in range(mapsCount-1):
        portalRect = Misc.portalImageRect
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
    
    for i in range(mapsCount):
        planetImageId = random.randint(0, len(Misc.planets)-1)
        planetRect = pygame.image.load(Misc.planets[planetImageId]).get_rect()
        map1 = maps[i]
        map1Rect = map1.background.get_rect()
        
        col = True
        while col:
            col = False
            p1 = Planet(random.randint(planetRect.centerx, map1Rect.width-planetRect.centerx), random.randint(planetRect.centery, map1Rect.height-planetRect.centery), planetImageId, i)
         
            for portal in map1.portals:
                if portal.rect.colliderect(p1):
                    col = True
            
            for planet in map1.planets:
                if planet.rect.colliderect(p1):
                    col = True
        
        map1.add_planet(p1)
        planets.append(p1)
        
    
def get_world():
    global maps, portals, planets
    
    remote = {"World": []}
    
    remoteMaps = []
    remotePortals = []
    remotePlanets = []
    
    remote["World"].append({"Map": remoteMaps})
    remote["World"].append({"Portal": remotePortals})
    remote["World"].append({"Planet": remotePlanets})
    
    for map1 in maps:
        remoteMaps.append(map1.getDataInit())
    
    for portal in portals:
        remotePortals.append(portal.getDataInit())
    
    for planet in planets:
        remotePlanets.append(planet.getDataInit())
    
    print(remote)
    return remote


def load_world(remote):
    global maps, portals, planets
    maps = []
    portals = []
    planets = []
    
    remoteMaps = remote["World"][0]["Map"]
    remotePortals = remote["World"][1]["Portal"]
    remotePlanets = remote["World"][2]["Planet"]
    
    mapsCount = len(remoteMaps)
    print(mapsCount, "maps")
    
    for map1 in remoteMaps:
        print(map1)
        maps.append(Map(map1[0], map1[1]))
        
    for portal in remotePortals:
        p1 = Portal(portal[0], portal[1], portal[2], portal[3], portal[4], portal[5])
        maps[portal[2]].add_portal(p1)
        portals.append(p1)
    
    for i in range(len(remotePortals)):
        remotePortal = remotePortals[i]
        if remotePortal[6] is not None:
            portal = portals[i]
            portal.exitId = remotePortal[6]
            portal.exit = portals[portal.exitId]
    
    for planet in remotePlanets:
        p1 = Planet(planet[0], planet[1], planet[2], planet[3], planet[4])
        maps[planet[3]].add_planet(p1)
        planets.append(p1)
        
def update():
    for ma in maps:
        ma.update()       
