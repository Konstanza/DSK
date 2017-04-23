'''
Created on 13 abr. 2017

@author: Konstanza
'''
import socket
import msgpack

class Server(object):
    '''
    classdocs
    '''


    def __init__(self, minPlayers = 1,  maxPlayers = 1, host="localhost", port=9999):
        '''
        Constructor
        '''
        self.maxPlayers = maxPlayers
        self.minPlayers = minPlayers
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.socket.bind((host, port))
        self.open = True
        
        self.host = host
        self.port = port
        
        self.userAddr = {}
        self.indexAddr = []
        
        self.waiting = False
        self.sending = False
        self.worldLoaded = False
        self.playersLoaded = False
        self.playersNamesLoaded = False
        self.playing = False
        
    
    def state_waitForPlayers(self):
        self.state = self.state_waitForPlayers
        self.waiting = True
        
        while self.waiting and self.open:
            
            try:
                data, addr = self.socket.recvfrom(1024)
                
                data = msgpack.loads(data)
                
                if  not addr in self.userAddr:
                    if len(self.userAddr) < self.maxPlayers:
                        user = User(data)
                            
                        self.userAddr[addr] = user
                        self.indexAddr.append(addr)
                        
                        print(data, addr)
                    else:
                        self.sendto("Server full", addr)
                else:
                    print(data, addr)
                    
            except socket.error:
                pass
    
    
    def state_loop(self):
        self.state = self.state_loop
               
        while self.open:
            
            try:
                data, addr = self.socket.recvfrom(1024)
                
                data = msgpack.loads(data)
                
                if not addr in self.userAddr:
                    self.sendto("Game started", addr)
                else:
                    if data == "Waiting for data":
                        self.userAddr[addr].waiting = True
                        self.sending = True
                        
                        for addr in self.userAddr:
                            if not self.userAddr[addr].waiting:
                                self.sending = False
                                break
                        print("Received:",str(data), "from",addr)
                    elif data == "World loaded":
                        self.userAddr[addr].worldLoaded = True
                        self.worldLoaded = True
                        
                        for addr in self.userAddr:
                            if not self.userAddr[addr].worldLoaded:
                                self.worldLoaded = False
                                break
                        print("Received:",str(data), "from",addr)
                    elif data == "Player loaded":
                        self.userAddr[addr].playerLoaded = True
                        self.playersLoaded = True
                        
                        for addr in self.userAddr:
                            if not self.userAddr[addr].playerLoaded:
                                self.playersLoaded = False
                                break
                        print("Received:",str(data), "from",addr)
                    elif data == "Players names loaded":
                        self.userAddr[addr].playerNamesLoaded = True
                        self.playersNamesLoaded = True
                        
                        for addr in self.userAddr:
                            if not self.userAddr[addr].playerNamesLoaded:
                                self.playersNamesLoaded = False
                                break
                        print("Received:",str(data), "from",addr)
                    elif isinstance(data, dict):
                        dataType = data.keys()[0]
                        
                        if dataType == "PlayerDataForHost":
                            data = data["PlayerDataForHost"]
                            self.userAddr[self.indexAddr[data[0]-1]].playerData = data
                        
            except socket.error:
                pass  
        
    def numPlayers(self):
        return len(self.userAddr)
    
    def ready(self):
        if len(self.userAddr) >= self.minPlayers:
            return True    
        return False
    
    def sendto(self, data, addr):
        data = msgpack.dumps(data)    
        self.socket.sendto(data, addr)
    
    def sendtoall(self, data):
        for addr in self.userAddr:
            self.sendto(data, addr)
    
    def sendtoIndex(self, data, index):
        self.sendto(data, self.indexAddr[index])
    
    def terminate(self):
        self.socket.close()
        self.open = False
        print("Server closed")

class User():
    
    def __init__(self, nickname):
        self.nickname = nickname
        self.worldLoaded = False
        self.playerLoaded = False
        self.playerNamesLoaded = False
        self.waiting = False
        self.playerData = None

    