'''
Created on 13 abr. 2017

@author: Konstanza
'''

import socket
import cPickle as pickle
import threading
from Maps import RemoteWorld, RemoteMapForClient
from Players import PlayerDataForClient, PlayersNames
import Maps
from Misc import getCurrentTimeMs

class Client(object):
    '''
    classdocs
    '''


    def __init__(self, name="Konstanza", serverIp = "localhost", serverPort = 9999):
        '''
        Constructor
        '''
        self.name = name
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        
        self.serverAddr = (serverIp, serverPort)
        
        self.open = True
        self.downloading = False
        self.worldLoaded = False
        self.playerData = None
        self.mapData = None
        self.playersNames = None
        
        self.lastTime = getCurrentTimeMs()
        self.ms = 0
        
    def state_sendName(self):
        self.send(self.name)
        
    def state_loop(self):
        while self.open:
            
            try:
                data, addr = self.socket.recvfrom(1024)
            
                data = pickle.loads(data)
                
                if data == "Sending game data":
                    self.downloading = True
                    self.send("Waiting for data")
                    print(str(data), addr)
                    print("Waiting for data")
                elif isinstance(data, RemoteWorld):
                    Maps.load_world(data)
                    self.worldLoaded = True
                    self.send("World loaded")
                    print(str(data), addr)
                    print("World loaded")
                elif isinstance(data, PlayerDataForClient):
                    if self.playerData is None:
                        self.send("Player loaded")
                        print(str(data), addr)
                        print("Player loaded")
                    self.playerData = data
                elif isinstance(data, PlayersNames):
                    self.playersNames = data.players
                    self.send("Players names loaded")
                    print(str(data), addr)
                    print("Players names loaded")
                elif isinstance(data, RemoteMapForClient):
                    self.mapData = data
                
                currentTime = getCurrentTimeMs()
                self.ms = currentTime - self.lastTime
                self.lastTime = currentTime
            except socket.error:
                pass

    def send(self, data):
        data = pickle.dumps(data)
        self.socket.sendto(data, self.serverAddr)
    
    def terminate(self):
        self.socket.close()
        self.open = False
        
if __name__ == "__main__":
    client = Client("Kris")
    
    client.state_sendName()
    threading.Thread(target= client.state_loop).start()     
        