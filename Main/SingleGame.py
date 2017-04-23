'''
Created on 14 abr. 2017

@author: Konstanza
'''
import Maps
import Misc
import pygame
from Players import PlayerHost

class SingleGame(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        Maps.generate_world(2)
        
        self.player = PlayerHost(0,300, 300, 0)
        Maps.maps[0].add_player(self.player)
        
    def update(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Misc.done=True
            elif event.type == pygame.KEYDOWN:
                self.player.updateKeyboard()
                if event.key == pygame.K_w:
                    self.player.direction = 'w'
                elif event.key == pygame.K_s:
                    self.player.direction = 's'
                elif event.key == pygame.K_a:
                    self.player.direction = 'a'
                elif event.key == pygame.K_d:
                    self.player.direction = 'd'
            elif event.type == pygame.KEYUP:
                self.player.updateKeyboard()
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                self.player.setMousePosition(mouseX,mouseY)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.player.updateMouseButtons()
        
        Maps.update()
        
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        self.player.draw()
            
        