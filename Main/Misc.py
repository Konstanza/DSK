'''
Created on 18 mar. 2017

@author: Konstanza
'''

import os
import sys
from os.path import dirname
import pygame
import time
import errno


view = None

#Server-Client
host = 'localhost'
hostPort = 9999
ip = 'localhost'
port = 9999
nickname = 'Kons'
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

if getattr( sys, 'frozen', False ) :
        # Running in a bundle
        BASE_PATH = sys._MEIPASS
        IMAGE_PATH = BASE_PATH
        REC_PATH = os.path.join(os.path.dirname(sys.executable), "Frames")
        FONT_PATH = BASE_PATH
else :
        # Running live
        BASE_PATH = dirname(__file__)
        IMAGE_PATH = os.path.join(BASE_PATH, "Images")
        REC_PATH = os.path.join(BASE_PATH, "Frames")
        FONT_PATH = os.path.join(BASE_PATH, "Fonts")
        
try:
    os.mkdir(REC_PATH)
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

i = 0
while True:
    try:
        REC_PATH_N = os.path.join(REC_PATH, "Frames-"+str(i))
        os.mkdir(REC_PATH_N)
        break
    except OSError as exception:
        i += 1
        if exception.errno != errno.EEXIST:
            raise    
        
# Images
backgrounds = [os.path.join(IMAGE_PATH, 'space-1.png'), 
               os.path.join(IMAGE_PATH, 'space-2.png'),
               os.path.join(IMAGE_PATH, 'background_2.jpg'),
               os.path.join(IMAGE_PATH, 'background_3.jpg'),
               os.path.join(IMAGE_PATH, 'Space.png')
               ]

players = [
    os.path.join(IMAGE_PATH, 'playerShip1_blue.png'),
    os.path.join(IMAGE_PATH, 'playerShip1_red.png'),
    os.path.join(IMAGE_PATH, 'playerShip1_green.png'),
    os.path.join(IMAGE_PATH, 'playerShip1_purple.png')
    ]

portalImage = os.path.join(IMAGE_PATH, 'black-hole-warp128-1.png')
portalImageRect = pygame.image.load(portalImage).get_rect()
portalAnim = {
    "path": os.path.join(IMAGE_PATH, 'black-hole-warp128-'),
    "max": 9,
    "type": '.png'
    }

# Weapons
shots = [
    os.path.join(IMAGE_PATH, 'laserBlue04.png')
    ]

#Fonts
font = 'HappyKiller.ttf'

def getCurrentTimeMs():
    return int(round(time.time() * 1000))
    
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
        
