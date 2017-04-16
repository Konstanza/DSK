'''
Created on 13 abr. 2017

@author: Konstanza
'''

import socket
import pickle
import threading
from Maps import RemoteWorld
from Players import PlayerData
import Maps

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
        
    def state_sendName(self):
        
        self.send(self.name)
        
    def state_loop(self):
        while self.open:
            
            try:
                data, addr = self.socket.recvfrom(1024)
            
                data = pickle.loads(data)
                
                print(str(data), addr)
                
                if data == "Sending game data":
                    self.downloading = True
                    self.send("Waiting for data")
                    print("Waiting for data")
                elif isinstance(data, RemoteWorld):
                    Maps.load_world(data)
                    self.worldLoaded = True
                    self.send("World loaded")
                    print("World loaded")
                elif isinstance(data, PlayerData):
                    self.playerData = data
                    self.send("Player loaded")
                    print("Player loaded")
                    
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
        