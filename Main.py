import pygame
import os
import sys
from os.path import dirname
from Players import Player1

BLACK = (0,0,0)
FPS = 60
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

# Images
IMAGE_PATH = os.path.join(dirname(__file__), "Images")

background = pygame.image.load(os.path.join(IMAGE_PATH, 'space-1.png'))
blueShip = pygame.image.load(os.path.join(IMAGE_PATH, 'playerShip1_blue.png'))
bluShipRect = blueShip.get_rect()


def main():
    
    global clock, done
    
    initGame()

    while done == False:
        update()
    
        draw()
    
        clock.tick(FPS)
        
    terminate()


def initGame():
    global clock, display, p1, mouseX, mouseY, done, debug
     
    pygame.init()

    display = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
    pygame.display.set_caption('DSK GAME')
    
    clock = pygame.time.Clock()

    p1 = Player1(display.get_width()/2-bluShipRect.width/2, display.get_height()/2-bluShipRect.height/2, blueShip)

    mouseX = 0  
    mouseY = 0

    done = False
    debug = False

    pygame.key.set_repeat(True)
    
    
def draw():
    display.fill(BLACK)
    
    display.blit(background, (p1.x, p1.y))
    
    p1.draw(display, mouseX, mouseY, debug)
    
    pygame.display.flip()
    
    #pygame.display.update()


def update():
    global done, mouseX, mouseY, debug
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done=True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                debug = not debug
        elif event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
                
    p1.update(display, mouseX, mouseY)
    
    
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

