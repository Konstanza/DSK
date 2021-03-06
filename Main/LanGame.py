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
        
        self.playerHost = playerHost
        self.players = players
    
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
                if event.key == pygame.K_w:
                    self.playerHost.direction = 'w'
                elif event.key == pygame.K_s:
                    self.playerHost.direction = 's'
                elif event.key == pygame.K_a:
                    self.playerHost.direction = 'a'
                elif event.key == pygame.K_d:
                    self.playerHost.direction = 'd'
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
        self.loadMap()
        self.loadPlayer()
        
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
        
        if Misc.drawFps:
            Misc.drawMs = True
            
        self.player.update()
        
        threading.Thread(target = self.sendData).start()
    
    def loadMap(self):
        mapData = self.client.mapData
        if mapData is not None:
            Maps.maps[mapData[0]].loadMap(mapData)
        
    def loadPlayer(self):
        self.player.loadData(self.client.playerData)
        
    def sendData(self):
        self.client.send(self.player.getData())

        
