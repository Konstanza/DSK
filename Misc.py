'''
Created on 18 mar. 2017

@author: Konstanza
'''

import os
from os.path import dirname
import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

FPS = 60
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Images
IMAGE_PATH = os.path.join(dirname(__file__), "Images")

backgrounds = [pygame.image.load(os.path.join(IMAGE_PATH, 'space-1.png')), pygame.image.load(os.path.join(IMAGE_PATH, 'space-2.png'))]
blueShip = pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_blue.png'))
redShip = pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_red.png'))
portal = pygame.image.load(os.path.join(IMAGE_PATH, 'black_hole.png'))
bluShipRect = blueShip.get_rect()

basicShot =  pygame.image.load(os.path.join(IMAGE_PATH, 'laserBlue04.png'))

# Weapons
basicWeapon = (basicShot, 10, 10, 30) # image, power, speed, time
