'''
Created on 24 mar. 2017

@author: Konstanza
'''
import pygame
import Maps
import Misc
import threading
from Players import PlayerHost, PlayerClient

class LanGameHost():
    
    def __init__(self, server, playerHost, players):
        self.server = server
        #self.server.sendtoall("Game started")
        
        self.playerHost = playerHost
        self.players = players
        #threading.Thread(target = self.server.state_startGame).start()
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        
        self.playerHost.draw()
    
    def quit(self):
        self.server.terminate()
        Misc.done = True
        
    def update(self):
        self.loadPlayers()
        
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
        
        threading.Thread(target = self.sendData).start()

    def loadPlayers(self):
        for player in self.players:
            player.loadDataFromClient(self.server.userAddr[self.server.indexAddr[player.playerId-1]].playerData)
    
    def sendData(self):
        for player in self.players:
            self.server.sendtoIndex(player.getPlayerDataForClient(), player.playerId-1)
            self.server.sendtoIndex(player.map.getMap(player), player.playerId-1)
        
class LanGameClient():
    
    def __init__(self, client):
        self.client = client
        self.player = PlayerClient(self.client.playerData)
        Maps.maps[self.player.mapId].add_player(self.player)
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
            
        self.player.draw()
    
    def quit(self):
        self.client.terminate()
        Misc.done = True
        
    def update(self):
        self.loadPlayer()
        self.loadMap()
        
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
                
        self.player.update()
        #Maps.update()
        
        threading.Thread(target = self.sendData).start()
    
    def loadMap(self):
        self.player.map.loadMap(self.client.mapData)
        
    def loadPlayer(self):
        self.player.loadDataFromHost(self.client.playerData)
        
    def sendData(self):
        self.client.send(self.player.getDataForHost())

        