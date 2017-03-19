'''
Created on 18 mar. 2017

@author: Konstanza
'''
import random
from Misc import *
import pygame


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
        
        #pygame.draw.rect(back, WHITE, p1.rotatedShipRect, 1)
        
        p1.display.blit(back, (p1.display.get_width()/2-p1.x, p1.display.get_height()/2-p1.y))
        
    def update(self):
        
        for player in self.players:
            player.update()
        
        for obj in self.objects:
            obj.update()
    
    def add_player(self, player):
        self.players.append(player)
    

def generate_world():
    global maps
    mapsCount = 1
    
    for i in range(mapsCount):
        maps.append(Map(random.choice(backgrounds)))
    
def update():
    for ma in maps:
        ma.update()       