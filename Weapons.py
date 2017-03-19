import pygame
import os
from Misc import *
import math

class Weapon():
    
    def __init__(self, tup):
        self.shotImage = tup[0]
        self.shotImageRect = self.shotImage.get_rect()
        self.shotPower = tup[1]
        self.shotSpeed = tup[2]
        self.time = tup[3]
        self.count = 0
    
    def shoot(self, player):
        if self.count == 0:
            self.count = 1
            x = player.rotatedShipRect.centerx
            y = player.rotatedShipRect.centery
            
            return Projectil(x,y,player.dirX,player.dirY, player.deg, self.shotImage.copy(),self.shotPower,self.shotSpeed)
        return None
        
    def update(self):
        if self.count > 0:
            self.count += 1
            if self.count == self.time:
                self.count = 0


class Projectil(pygame.sprite.Sprite):

    def __init__(self, x, y, dirX, dirY, deg, image, power, speed):

        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'projectil.png'))
        self.image = image
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.deg = deg
        
        self.power = power
        self.speed = speed
        self.dirX = dirX
        self.dirY = dirY

    def update(self):
        self.x += self.dirX*self.speed
        self.y += self.dirY*self.speed

    def draw(self, surface, debug):
        #print("drawing")
        rotated = pygame.transform.rotate(self.image, self.deg)
        rotatedRect = rotated.get_rect(centerx = self.x, centery= self.y)
        surface.blit(rotated, rotatedRect)
        
        if debug:
            pygame.draw.rect(surface, WHITE, rotatedRect, 1)
        #surface.blit(self.image, (self.x, self.y))
        