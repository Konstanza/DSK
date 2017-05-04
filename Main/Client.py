'''
Created on 13 abr. 2017

@author: Konstanza
'''

import socket
import msgpack
import Maps
import errno
from Misc import getCurrentTimeMs
import Misc

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
        
        Misc.ms = 0
        
    def state_sendName(self):
        self.send(self.name)
        
    def state_loop(self):
        while self.open:
            
            try:
                data, addr = self.socket.recvfrom(16384)
                
                data = msgpack.loads(data)
                
                if data == "Sending game data":
                    self.downloading = True
                    self.send("Waiting for data")
                    print(str(data), addr)
                    print("Waiting for data")
                elif isinstance(data, dict):
                    dataType = data.keys()[0]
                    if dataType == "World":
                        Maps.load_world(data)
                        self.worldLoaded = True
                        self.send("World loaded")
                        print(str(data), addr)
                        print("World loaded")
                    elif dataType == "PlayerDataForClient":
                        if self.playerData is None:
                            self.send("Player loaded")
                            print(str(data), addr)
                            print("Player loaded")
                        self.playerData = data["PlayerDataForClient"]
                    elif dataType == "PlayersNames":
                        self.playersNames = data["PlayersNames"]
                        self.send("Players names loaded")
                        print(str(data), addr)
                        print("Players names loaded")
                    elif dataType == "Map":
                        self.mapData = data["Map"]
                
                currentTime = getCurrentTimeMs()
                Misc.ms = currentTime - self.lastTime
                self.lastTime = currentTime
            except socket.error as e:
                if e.errno == errno.WSAEMSGSIZE:
                    raise(e)
                if e.errno != errno.WSAEWOULDBLOCK:
                    print(e)
                
            
    def send(self, data):
        data = msgpack.dumps(data)
        self.socket.sendto(data, self.serverAddr)
    
    def terminate(self):
        self.socket.close()
        self.open = False   
        