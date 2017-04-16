'''
Created on 25 mar. 2017

@author: Konstanza
'''
import pygame
import Misc
from LanGame import LanGameHost, LanGameClient
from SingleGame import SingleGame
from Players import PlayerClient, PlayerData, PlayerHost
from Client import Client
from Server import Server
import threading
import random
import Maps

server = None

class MenuView(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.buttons = []
        
        selectedColor = Misc.RED
        notSelectedColor = Misc.BLUE
        
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2, 'play', Misc.font, 20,selectedColor,notSelectedColor, self.play))
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2+30, 'options', Misc.font, 20,selectedColor,notSelectedColor, self.options))
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2+60, 'quit', Misc.font, 20,selectedColor,notSelectedColor, self.quit))
        
    
    def play(self):
        Misc.view = PlayMenuView()
    def options(self):
        pass
    def quit(self):
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
                
        for button in self.buttons:
            button.update()
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        for button in self.buttons:
            button.draw(Misc.display)
            
class PlayMenuView(object):
    
    def __init__(self):
        self.buttons = []
        
        selectedColor = Misc.RED
        notSelectedColor = Misc.BLUE
        
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2, 'single', Misc.font, 20,selectedColor,notSelectedColor, self.single))
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2+30, 'create', Misc.font, 20,selectedColor,notSelectedColor, self.create))
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT/2+60, 'join', Misc.font, 20,selectedColor,notSelectedColor, self.join))
        self.buttons.append(Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT-30, 'return', Misc.font, 20,selectedColor,notSelectedColor, self.ret))
    
    def single(self):
        Misc.view = SingleGame()
    def join(self):
        Misc.view = JoinGame()
    def create(self):
        Misc.view = WaitingView()    
    def ret(self):
        Misc.view = MenuView()
    def quit(self):
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
                
        for button in self.buttons:
            button.update()
    
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        for button in self.buttons:
            button.draw(Misc.display)
        
class WaitingView(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        selectedColor = Misc.RED
        notSelectedColor = Misc.BLUE
        
        self.buttons = []
        
        startButton = Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT-60, 'start', Misc.font, 20,selectedColor,notSelectedColor, self.start)
        returnButton = Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT-30, 'return', Misc.font, 20,selectedColor,notSelectedColor, self.ret)
        
        self.buttons.append(startButton)
        self.buttons.append(returnButton)
        
        global server
        if server is not None: 
            server.terminate()
        server = Server(Misc.minPlayers, Misc.maxPlayers, Misc.host, Misc.hostPort)
        
        self.server = server
        print("Server started")
        threading.Thread(target = self.server.state_waitForPlayers).start()
        print("Waiting for players")
        
    def start(self):
        Misc.view = CreatingView(self.server)
        
    def accept(self):
        pass
    def kick(self):
        pass
    def ret(self):
        self.server.terminate()
        Misc.view = PlayMenuView()
        
    def quit(self):
        self.server.terminate()
        Misc.done = True
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
                
        for button in self.buttons:
            button.update()
            
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        for button in self.buttons:
            button.draw(Misc.display)

class CreatingView(object):
    
    def __init__(self, server):
        self.server = server
        self.server.waiting = False
        self.state = None
    
    class preparingClients(object):
        def __init__(self, view):
            self.view = view
            print('Preparing clients...')
            threading.Thread(target = self.view.server.state_loop).start()
            self.view.server.sendtoall("Sending game data")
            
        def update(self):
            if self.view.server.sending:
                self.view.state = self.view.generateWorld(self.view)
        
    class generateWorld(object):
        def __init__(self, view):
            self.view = view
            print('Clients waiting for data...')
            print('Generating world...')
            Maps.generate_world(self.view.server.numPlayers()+1)
            
            print("Sending world data")
            self.view.server.sendtoall(Maps.get_world())
        
        def update(self):
            if self.view.server.worldLoaded:
                self.view.state = self.view.generatePlayers(self.view)
    
    class generatePlayers(object):
        def __init__(self, view):
            self.view = view
            print("World loaded")
            print("Generating players...")
            
            takenMaps = []
            players = []
            
            for m in Maps.maps:
                takenMaps.append(m)
            
            takenMaps.sort()
            
            for playerId in range(self.view.server.numPlayers()+1):
                m = takenMaps[playerId]
                mBack = m.background
                mRect = mBack.get_rect()
                im = Misc.players[playerId]
                
                col = True
                while col:
                    col = False
                    
                    imRect = im.get_rect()
                    x = imRect.centerx = random.randint(imRect.centerx, mRect.width-imRect.centerx)
                    y = imRect.centery = random.randint(imRect.centery, mRect.height-imRect.centery)
                    
                    for portal in m.portals:
                        if portal.rect.colliderect(imRect):
                            col = True
                
                p = PlayerData(playerId, x, y, 0, m.mapId)
                
                print('Player '+str(playerId)+' created: '+ str(p))
                
                if playerId > 0:
                    players.append((p, playerId-1))
                    Maps.maps[m.mapId].add_player(PlayerClient(p))
                else:
                    self.view.playerHost = PlayerHost(p)
                    Maps.maps[m.mapId].add_player(self.view.playerHost)
            
            print("Sending players data...")
            for player in players:
                self.view.server.sendtoIndex(player[0], player[1])
        
        def update(self):
            if self.view.server.playersLoaded:
                self.view.startGame()
    
    def startGame(self):
        Misc.view = LanGameHost(self.server, self.playerHost)
        
    def quit(self):
        self.server.terminate()
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            
        if self.state == None:
            self.state = self.preparingClients(self)
        else:
            self.state.update()
                
            
    def draw(self):
        Misc.display.fill(Misc.BLACK)

class DownloadingView(object):
    
    def __init__(self, client):
        self.client = client
        self.state = None
    
    class preparing(object):
        def __init__(self, view):
            self.view = view
            print("Preparing...")
        
        def update(self):
            if self.view.client.downloading:
                self.view.state = self.view.downloadWorld(self.view)
                
    class downloadWorld(object):
        def __init__(self, view):
            self.view = view
            print("Downloading world...")
        
        def update(self):
            if self.view.client.worldLoaded:
                self.view.state = self.view.downloadPlayer(self.view)
    
    class downloadPlayer(object):
        def __init__(self, view):
            self.view = view
            print("Downloading player...")
        
        def update(self):
            if self.view.client.playerData is not None:
                self.view.startGame()
                
    def startGame(self):
        Misc.view = LanGameClient(self.client)
        
    def quit(self):
        self.client.terminate()
        Misc.done = True
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            
        if self.state == None:
            self.state = self.preparing(self)
        else:
            self.state.update()
            
    def draw(self):
        Misc.display.fill(Misc.BLACK)
    
class JoinGame(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        selectedColor = Misc.RED
        notSelectedColor = Misc.BLUE
        
        self.buttons = []
        
        returnButton = Misc.TextButton(Misc.DISPLAY_WIDTH/2, Misc.DISPLAY_HEIGHT-30, 'return', Misc.font, 20,selectedColor,notSelectedColor, self.ret)
        
        self.buttons.append(returnButton)
        
        self.client = Client(Misc.nickname, Misc.ip, Misc.port)
    
        self.client.state_sendName()
        threading.Thread(target= self.client.state_loop).start() 
        
    def ret(self):
        self.client.terminate()
        Misc.view = PlayMenuView()
        
    def quit(self):
        self.client.terminate()
        Misc.done = True
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
                
        for button in self.buttons:
            button.update()
        
        if self.client.downloading:
            Misc.view = DownloadingView(self.client)
            
    def draw(self):
        Misc.display.fill(Misc.BLACK)
        for button in self.buttons:
            button.draw(Misc.display)
        