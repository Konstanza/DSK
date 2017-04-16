'''
Created on 24 mar. 2017

@author: Konstanza
'''
import pygame
import Maps
import random
import Misc
from Players import PlayerData
from Players import PlayerClient
from Players import PlayerHost
import threading

class LanGameHost():
    
    def __init__(self, server, playerHost):
        self.server = server
        #self.server.sendtoall("Game started")
        
        self.playerHost = playerHost
        #threading.Thread(target = self.server.state_startGame).start()
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        
        self.playerHost.draw()
    
    def quit(self):
        self.server.terminate()
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.playerHost.updateKeyboard()
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                self.playerHost.setMousePosition(mouseX,mouseY)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.playerHost.updateMouseButtons()
                
        Maps.update()


class LanGameClient():
    
    def __init__(self, client):
        self.client = client
        self.player = PlayerHost(self.client.playerData)
        Maps.maps[self.player.mapId].add_player(self.player)
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        
        self.player.draw()
    
    def quit(self):
        self.client.terminate()
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.player.updateKeyboard()
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                self.player.setMousePosition(mouseX,mouseY)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.player.updateMouseButtons()
                
        Maps.update()
            
    

        