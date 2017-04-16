'''
Created on 18 mar. 2017

@author: Konstanza
'''

import os
from os.path import dirname
import pygame


view = None

#Server-Client
host = 'localhost'
hostPort = 9999
ip = 'localhost'
port = 9999
nickname = 'Kons2'
minPlayers = 1
maxPlayers = 2

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
GREEN = (0,255,0)
BLUE = (0,0,255)

DISPLAY_WIDTH = 640 #1100
DISPLAY_HEIGHT = 480 #800
display = None
done = False
debug = False
view = None

# Images
IMAGE_PATH = os.path.join(dirname(__file__), "Images")
REC_PATH = os.path.join(dirname(__file__), "Frames")

backgrounds = [pygame.image.load(os.path.join(IMAGE_PATH, 'space-1.png')), 
               pygame.image.load(os.path.join(IMAGE_PATH, 'space-2.png')),
               pygame.image.load(os.path.join(IMAGE_PATH, 'background_2.jpg')),
               pygame.image.load(os.path.join(IMAGE_PATH, 'background_3.jpg')),
               pygame.image.load(os.path.join(IMAGE_PATH, 'Space.png'))
               ]

players = [
    pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_blue.png')),
    pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_red.png')),
    pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_green.png')),
    pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_purple.png'))
    ]

blueShip = pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_blue.png'))
redShip = pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_red.png'))
redShip2 = pygame.image.load(os.path.join(IMAGE_PATH, 'enemyRed2.png'))
portalImage = pygame.image.load(os.path.join(IMAGE_PATH, 'black-hole-warp128-1.png'))
bluShipRect = blueShip.get_rect()


# Weapons
basicShot =  pygame.image.load(os.path.join(IMAGE_PATH, 'laserBlue04.png'))
basicWeapon = (basicShot, 10, 10, 30) # image, power, speed, time

#Fonts
FONT_PATH = os.path.join(dirname(__file__), "Fonts")
font = 'HappyKiller.ttf'


class TextButton():
    
    released = True
    
    def __init__(self, x, y, text, fontName, size, selectedColor, notSelectedColor,function):
        self.font = pygame.font.Font(os.path.join(FONT_PATH, fontName), size)
        self.text = text
        self.function = function
        self.selectedColor = selectedColor
        self.notSelectedColor = notSelectedColor
        self.color = self.selectedColor
        self.x = x
        self.y = y
        self.textRect = self.font.render(self.text, 1, self.color).get_rect(centerx = self.x, centery = self.y)
        self.clickReleased = True
        self.clickPressed = False
        
    
    def draw(self, surface):
        textImage = self.font.render(self.text, 1, self.color)
        surface.blit(textImage, self.textRect)

    def update(self):
        
        mouseX, mouseY = pygame.mouse.get_pos()
        
        if self.textRect.collidepoint(mouseX, mouseY):
            self.color = self.selectedColor
            
            if pygame.mouse.get_pressed()[0]:
                if self.clickReleased and TextButton.released:
                    self.function()
                    self.clickReleased = False
                    TextButton.released = False
                    self.clickPressed = True
                else:
                    if self.clickPressed:
                        self.clickReleased = True
                        TextButton.released = True
            else:
                self.clickReleased = True
                TextButton.released = True
                self.clickPressed = False
        else:
            self.color = self.notSelectedColor
        
