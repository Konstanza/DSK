import pygame
import os
import Misc
import math

class BasicWeapon():
    def __init__(self, player):
        self.shotImageId = 0
        self.shotPower = 10
        self.shotSpeed = 10
        self.time = 30
        self.count = 0
        self.player = player
    
    def shoot(self):
        if self.count == 0:
            self.count = 1
            x = self.player.rotatedShipRect.centerx
            y = self.player.rotatedShipRect.centery
            
            self.player.map.add_shot(ProjectilHost(self.player, x, y, self.player.deg, self.shotImageId,self.shotPower,self.shotSpeed))
            
    def update(self):
        if self.count > 0:
            self.count += 1
            if self.count == self.time:
                self.count = 0

class ProjectilData():
    def __init__(self, projectil):
        self.imageId = projectil.imageId
        self.x = projectil.x
        self.y = projectil.y
        self.deg = projectil.deg
    
    def __str__(self):
        return str(self.imageId, self.x, self.y, self.deg)

class ProjectilClient(pygame.sprite.Sprite):
    def __init__(self, projectil):
        pygame.sprite.Sprite.__init__(self)
        
        self.imageId = projectil.imageId
        self.image = pygame.image.load(Misc.shots[self.imageId])
        self.rect = self.image.get_rect()
        self.rotatedRect = self.rect
        self.radius = int(math.hypot(self.rect.x-self.rect.centerx, self.rect.y-self.rect.centery))
        
        self.x = projectil.x
        self.y = projectil.y
        self.deg = projectil.deg

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, self.deg)
        self.rotatedRect = rotated.get_rect(centerx = self.x, centery= self.y)
        surface.blit(rotated, self.rotatedRect)
        
        if Misc.debug:
            pygame.draw.rect(surface, Misc.WHITE, self.rotatedRect, 1)
            pygame.draw.circle(surface, Misc.YELLOW, self.rotatedRect.center, self.radius, 1)
        
class ProjectilHost(pygame.sprite.Sprite):

    def __init__(self, player, x, y, deg, imageId, power, speed):

        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.image.load(os.path.join(IMAGE_PATH, 'projectil.png'))
        self.imageId = imageId
        self.image = pygame.image.load(Misc.shots[self.imageId])
        
        self.rect = self.image.get_rect()
        self.rotatedRect = self.rect
        self.radius = int(math.hypot(self.rect.x-self.rect.centerx, self.rect.y-self.rect.centery))
        self.x = x
        self.y = y
        self.deg = deg+180
        
        self.power = power
        self.speed = speed
        
        self.player = player
        self.initX = self.x
        self.initY = self.y
        self.initRadius = player.radius
        self.mapId = player.mapId
        self.map = player.map
        
        self.out = False
        
    def getData(self):
        return ProjectilData(self)
        
    def detect_borders(self):
        backRect = self.map.background.get_rect()
        
        if not self.rotatedRect.colliderect(backRect):
            self.map.remove_shot(self)
    
    def move(self):
        rad = math.radians(self.deg)
        self.x += math.sin(rad)*self.speed
        self.y += math.cos(rad)*self.speed
        
    def update(self):
        self.move()
        self.detect_borders()
        
        for key in self.map.players:
            player = self.map.players[key]
            if player.playerId != self.player.playerId:
                playerRect = player.rotatedShipRect
                if self.rotatedRect.colliderect(playerRect):
                    self.map.remove_shot(self)
        
        for portal in self.map.portals:
            if self.rotatedRect.colliderect(portal.rect):
                self.map.remove_shot(self)
                
                    
    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, self.deg)
        self.rotatedRect = rotated.get_rect(centerx = self.x, centery= self.y)
        surface.blit(rotated, self.rotatedRect)
        
        if Misc.debug:
            pygame.draw.rect(surface, Misc.WHITE, self.rotatedRect, 1)
            pygame.draw.circle(surface, Misc.YELLOW, self.rotatedRect.center, self.radius, 1)
        