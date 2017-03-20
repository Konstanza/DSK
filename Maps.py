'''
Created on 18 mar. 2017

@author: Konstanza
'''
import random
from Misc import *
import pygame
from pygame import surface
from pygame.rect import Rect
from random import randint

maps = []

class Map(object):
    '''
    classdocs
    '''

    def __init__(self, background):
        '''
        Constructor
        '''
        self.background = background
        self.players = []
        self.objects = []
        self.portals = []
    
    def add_portal(self, portal):
        self.portals.append(portal)
        
    def draw(self, p1):
        
        back = self.background.copy()
        
        for obj in self.objects:
            obj.draw(back)
            
        for portal in self.portals:
            portal.draw(back)
            
        for player in self.players:
            if player != p1:
                player.draw(back)
        
        for shot in p1.shots:
            shot.draw(back, p1.debug)
        
        if p1.debug:
            pygame.draw.rect(back, WHITE, p1.rotatedShipRect, 1)
            pygame.draw.rect(back, RED, p1.shipRect, 1)
        
        p1.display.blit(back, (p1.display.get_width()/2-p1.x, p1.display.get_height()/2-p1.y))
        
    def update(self):
            
        for player in self.players:
            player.update()
        
        for obj in self.objects:
            obj.update()
            
        for portal in self.portals:
            portal.update(self.players)
    
    def add_player(self, player):
        self.players.append(player)
    
    def remove_player(self, player):
        self.players.remove(player)
    
class Portal():
    def __init__(self, x, y, map1, mX, mY, map2, exit = None):
        self.x = x
        self.y = y
        self.mX = mX 
        self.mY = mY
        self.map1 = map1
        self.map2 = map2
        self.image = portalImage
        self.exit = exit
        self.rect = self.image.get_rect(centerx = self.x, centery = self.y)
    
    def update(self, players):
        # DETECT COLLISION
        for player in players:
            if self.exit != None:
                if player.inPortal != self.exit:
                    if self.collision(player):
                        player.inPortal = self
                        players.remove(player)
                        self.map2.add_player(player)
                
                        player.map = self.map2
                        player.direction = ''
                        player.x = self.mX
                        player.y = self.mY
                else:
                    if not self.collision(player):
                        player.inPortal = None
            else:
                if self.collision(player):
                    player.inPortal = self
                    players.remove(player)
                    self.map2.add_player(player)
                
                    player.map = self.map2
                    player.direction = ''
                    player.x = self.mX
                    player.y = self.mY
                
    
    def collision(self, player):
        if self.rect.colliderect(player.shipRect):
            return True
        return False
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        #pygame.draw.circle(surface, YELLOW, (self.x, self.y), 50, 5)
        
        
def generate_world():
    global maps
    maps = []
    mapsCount = random.randint(2,5)
    print(mapsCount, "maps")
    
    for i in range(mapsCount):
        maps.append(Map(random.choice(backgrounds)))
    
    for i in range(mapsCount-1):
        portalRect = portalImage.get_rect()
        map1 = maps[i]
        map2 = maps[i+1]
        map1Rect = map1.background.get_rect()
        map2Rect = map2.background.get_rect()
        
        col = True
        while col:
            col = False
            p1 = Portal(random.randint(portalRect.centerx, map1Rect.width-portalRect.centerx), random.randint(portalRect.centery, map1Rect.height-portalRect.centery), map1, randint(70, map2Rect.width-70), randint(70, map2Rect.height-70), map2)
         
            for portal in map1.portals:
                if portal.rect.colliderect(p1):
                    col = True
            
        p2 = Portal(p1.mX, p1.mY, map2, p1.x, p1.y, map1, p1)
        p1.exit = p2
        map1.add_portal(p1)
        map2.add_portal(p2)
    
def update():
    for ma in maps:
        ma.update()       
