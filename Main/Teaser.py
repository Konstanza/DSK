'''
Created on 25 mar. 2017

@author: Konstanza
'''
import Maps
from Players import Player1, Player2
from Misc import *
from Main import display, mouseX, mouseY
import pygame

class Teaser(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        global redShip2, blueShip, display, mouseX, mouseY
        
    
        #p1 = Player1(display, display.get_width()/2-bluShipRect.width/2, display.get_height()/2-bluShipRect.height/2, blueShip)
        self.p1 = Player1(display, 400, 400, blueShip)
    
        self.enemys = [Player2(display, 300, 400, redShip2),Player2(display, 350, 300, redShip2),Player2(display, 400, 200, redShip2)]
        
        Maps.generate_world_teaser()
        map1 = Maps.maps[0]
        map2 = Maps.maps[2]
    
        map1.add_player(self.p1)
    
        for enemy in self.enemys:
            map2.add_player(enemy)
    
        mouseX = 0  
        mouseY = 0
    
    
    def update(self):
        global done, mouseX, mouseY, debug
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done=True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.p1.direction = 'w'
                elif event.key == pygame.K_s:
                    self.p1.direction = 's'
                elif event.key == pygame.K_a:
                    self.p1.direction = 'a'
                elif event.key == pygame.K_d:
                    self.p1.direction = 'd'
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                self.p1.setMousePosition(mouseX,mouseY)
        
        for enemy in self.enemys:
            enemy.setMousePosition(self.p1.x,self.p1.y)
        #p1.update(display, mouseX, mouseY)
        Maps.update()
        
    def draw(self):
        global display
        display.fill(BLACK)
            
        self.p1.draw()
            
        pygame.display.flip()
            
        #pygame.display.update()
    
        