import pygame
import os
import sys
import Misc
import random
import threading
import Menu

random.seed(a=None)
video = []
frames = 0
rec = False
savingThread = None
debugPressed = False
debugReleased = True
recPressed = False
recReleased = True
FPS = 60
    
def main():
    
    global clock, FPS
    
    initPygame()
    
    while Misc.done == False:
        Misc.view.update()
        update()
        
        Misc.view.draw()
        draw()
    
        clock.tick(FPS)
        
    terminate()


def initPygame():
    global clock
    
    pygame.init()

    Misc.display = pygame.display.set_mode((Misc.DISPLAY_WIDTH,Misc.DISPLAY_HEIGHT))
    pygame.display.set_caption('DSK GAME')
    
    pygame.key.set_repeat(True)
    
    clock = pygame.time.Clock()
    
    Misc.view = Menu.MenuView()
    
def draw():
    global video, savingThread, rec
    
    if rec:
        video.append(Misc.display.copy())
        pygame.draw.rect(Misc.display, Misc.RED, (0,0,Misc.DISPLAY_WIDTH-1,Misc.DISPLAY_HEIGHT-1), 2)
    
    if savingThread is not None:
        pygame.draw.rect(Misc.display, Misc.YELLOW, (0,0,Misc.DISPLAY_WIDTH-1,Misc.DISPLAY_HEIGHT-1), 2)
        
    pygame.display.flip()
    
    
def save_images():
    global video, frames, savingThread
    
    videoLen = len(video)
    print(videoLen)
    for i in range(videoLen):
        pygame.image.save(video[i], os.path.join(Misc.REC_PATH, 'frame_'+str(i+frames)+'.png'))
    
    frames += videoLen
    video = []
    
    savingThread = None

def update():
    global savingThread, rec, video, debugReleased, debugPressed, recPressed, recReleased
    
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_F1]:
        if debugReleased:
            Misc.debug = not Misc.debug
            debugReleased = False
        debugPressed = True
        #print(Misc.debug)
    else:
        if debugPressed:
            debugReleased = True
        #print(Misc.debug)
    
    if pressed[pygame.K_F2]:
        if recReleased:
            if not rec and savingThread is None:
                rec = True
            else:
                rec = False
            recReleased = False
        recPressed = True
        #print(rec)
    else:
        if recPressed:
            recReleased = True
        
    if pressed[pygame.K_F3]:
        if not rec and savingThread is None and len(video) > 0:
            savingThread = threading.Thread(target=save_images)
            savingThread.start()
    if pressed[pygame.K_F4]:
        if savingThread is None:
            video = []
        rec = False
                        
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

