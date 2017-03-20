import pygame
import os
import sys
from Players import Player1, Player2
from Misc import *
import Maps
import random

random.seed(a=None)

def main():
    
    global clock, done
    
    
    initGame()

    while done == False:
        update()
    
        draw()
    
        clock.tick(FPS)
        
    terminate()


def initGame():
    global clock, display, p1, mouseX, mouseY, done, debug, map1
    
    pygame.init()

    display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption('DSK GAME')
    
    clock = pygame.time.Clock()

    #p1 = Player1(display, display.get_width()/2-bluShipRect.width/2, display.get_height()/2-bluShipRect.height/2, blueShip)
    p1 = Player1(display, 400, 400, blueShip)
    
    p2 = Player2(display, 300, 300, redShip)
     
    
    Maps.generate_world()
    Maps.maps[0].add_player(p1)
    Maps.maps[0].add_player(p2)
    map1 = Maps.maps[0]
    
    p1.map = map1
    p2.map = map1
    
    mouseX = 0  
    mouseY = 0

    done = False
    debug = False

    pygame.key.set_repeat(True)
    
    
def draw():
    display.fill(BLACK)
    
    p1.draw()
    
    pygame.display.flip()
    
    #pygame.display.update()


def update():
    global done, mouseX, mouseY, debug
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                p1.switchDebug()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p1.direction = 'w'
            elif event.key == pygame.K_s:
                p1.direction = 's'
            elif event.key == pygame.K_a:
                p1.direction = 'a'
            elif event.key == pygame.K_d:
                p1.direction = 'd'
        elif event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            p1.setMousePosition(mouseX,mouseY)
                
    #p1.update(display, mouseX, mouseY)
    Maps.update()
    
    
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
