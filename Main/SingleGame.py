'''
Created on 14 abr. 2017

@author: Konstanza
'''
import Maps
import Misc
import pygame
from Players import Player1

class SingleGame(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        Maps.generate_world(1)
        
        self.p1 = Player1(Misc.display, 400, 400, Misc.blueShip)
        Maps.maps[0].add_player(self.p1)
        
    def update(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Misc.done=True
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
        
        Maps.update()
        
    def draw(self):
        self.p1.draw()
            
        