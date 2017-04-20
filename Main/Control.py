'''
Created on 13 abr. 2017

@author: Konstanza
'''
import pygame

class RemoteKeyboard(object):

    def __init__(self):
        self.keyPressed = {
            "moveW": False, 
            "moveA": False, 
            "moveS": False, 
            "moveD": False}
    
    def __str__(self):
        return str(self.keyPressed)
        
class Keyboard(object):
    
    def __init__(self):
        self.remote = RemoteKeyboard()
        
        self.keyCodes = {
            "moveW": pygame.K_w, 
            "moveA": pygame.K_a, 
            "moveS": pygame.K_s, 
            "moveD": pygame.K_d}
    
    def changeKeyCode(self, key, keyCode):
        self.keyCodes[key] = keyCode
    
    def update(self):
        pressed = pygame.key.get_pressed()
        codes = self.keyCodes
        
        for key in codes:
            self.updateKey(key, pressed[codes[key]])
    
    def isKeyPressed(self, keyCode):
        return self.remote.keyPressed[keyCode]
    
    def updateKey(self, key, state):
        self.remote.keyPressed[key] = state

class Mouse(object):
    
    def __init__(self):
        self.remote = RemoteMouse()
        
        self.buttonCodes = {
            "shoot": 0
            }
    
    def changeButtonCode(self, button, buttonCode):
        self.buttonCodes[button] = buttonCode
    
    def updateButtons(self):
        pressed = pygame.mouse.get_pressed()
        
        codes = self.buttonCodes
        
        for button in codes:
            self.updateButton(button, pressed[codes[button]])
            
    def updatePosition(self):
        self.remote.mouseX, self.remote.mouseY = pygame.mouse.get_pos()
    
    def isButtonPressed(self, buttonCode):
        return self.remote.buttonPressed[buttonCode]

    def updateButton(self, button, state):
        self.remote.buttonPressed[button] = state
    
    def setPosition(self, mouseX, mouseY):
        self.remote.mouseX = mouseX
        self.remote.mouseY = mouseY


class RemoteMouse(object):

    def __init__(self):
        self.buttonPressed = {
            "shoot": False}
        
        self.mouseX = 0
        self.mouseY = 0
    
    def __str__(self):
        return str(self.buttonPressed)
            
            
            
            
            
        