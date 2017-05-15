import pygame
import os
import sys
import Misc
import random
import threading
from threading import Timer
import Menu
import errno

random.seed(a=None)
video = []
frames = 0
rec = False
savingThread = None
debugPressed = False
debugReleased = True
recPressed = False
recReleased = True
drawFpsPressed = False
drawFpsReleased = True
FPS = 60
fpsCounter = 0
fps = FPS
    
def main():
    
    global clock, FPS, fps, fpsCounter, timer
    
    initPygame()
    
    timer = Timer(1.0, updateFps)
    timer.start()
    
    while Misc.done == False:
        Misc.view.update()
        update()
        fpsCounter += 1
        
        Misc.view.draw()
        draw()
    
        clock.tick(FPS)
        
    terminate()


def updateFps():
    global fps, fpsCounter, timer
    fps = fpsCounter
    fpsCounter = 0
        
    timer = Timer(1.0, updateFps)
    timer.start()

def drawFps(surface):
    global fps
    color = Misc.RED
    text = "fps: "+str(fps)
    font = pygame.font.Font(os.path.join(Misc.FONT_PATH, 'HappyKiller.ttf'), 10)
    textImage = font.render(text, 1, color)
    textRect = font.render(text, 1, color).get_rect(x = 0, y = 0)
    surface.blit(textImage, textRect)
    
def initPygame():
    global clock
    
    pygame.init()

    Misc.display = pygame.display.set_mode((Misc.DISPLAY_WIDTH,Misc.DISPLAY_HEIGHT))
    pygame.display.set_caption('DSK GAME')
    Misc.gameSurface = Misc.display.subsurface(Misc.gameRect)
    
    pygame.key.set_repeat(True)
    
    clock = pygame.time.Clock()
    
    Misc.view = Menu.MenuView()

def drawMs(surface):
    color = Misc.RED
    text = "ms: "+str(Misc.ms)
    font = pygame.font.Font(os.path.join(Misc.FONT_PATH, 'HappyKiller.ttf'), 10)
    textImage = font.render(text, 1, color)
    textRect = font.render(text, 1, color).get_rect(x = 0, y = 15)
    surface.blit(textImage, textRect)
    
def draw():
    global video, savingThread, rec
    
    if rec:
        video.append(Misc.display.copy())
        pygame.draw.rect(Misc.display, Misc.RED, (0,0,Misc.DISPLAY_WIDTH-1,Misc.DISPLAY_HEIGHT-1), 2)
    
    if savingThread is not None:
        pygame.draw.rect(Misc.display, Misc.YELLOW, (0,0,Misc.DISPLAY_WIDTH-1,Misc.DISPLAY_HEIGHT-1), 2)
    
    if Misc.drawFps:
        drawFps(Misc.display)
        if Misc.drawMs:
            drawMs(Misc.display)
    
    pygame.display.flip()
    
def save_images():
    global video, frames, savingThread
    
    i = 0
    while True:
        try:
            REC_PATH_N = os.path.join(Misc.REC_PATH, "Frames-"+str(i))
            os.mkdir(REC_PATH_N)
            break
        except OSError as exception:
            i += 1
            if exception.errno != errno.EEXIST:
                raise    
            
    videoLen = len(video)
    print("Saving "+str(videoLen)+" images in "+REC_PATH_N)
    for i in range(videoLen):
        pygame.image.save(video[i], os.path.join(REC_PATH_N, 'frame_'+str(i+frames)+'.png'))
    print("Images saved")
    
    frames += videoLen
    video = []
    
    savingThread = None

def update():
    global savingThread, rec, video, debugReleased, debugPressed, recPressed, recReleased, drawFpsReleased, drawFpsPressed
    
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_F1]:
        if drawFpsReleased:
            Misc.drawFps = not Misc.drawFps
            if Misc.drawMs:
                Misc.drawMs = False
            drawFpsReleased = False
        drawFpsPressed = True
    else:
        if drawFpsPressed:
            drawFpsReleased = True

    if pressed[pygame.K_F2]:
        if debugReleased:
            Misc.debug = not Misc.debug
            debugReleased = False
        debugPressed = True
    else:
        if debugPressed:
            debugReleased = True
    
    if pressed[pygame.K_F3]:
        if recReleased:
            if not rec and savingThread is None:
                rec = True
            else:
                rec = False
            recReleased = False
        recPressed = True
    else:
        if recPressed:
            recReleased = True
        
    if pressed[pygame.K_F4]:
        if not rec and savingThread is None and len(video) > 0:
            savingThread = threading.Thread(target=save_images)
            savingThread.start()
            
    if pressed[pygame.K_F5]:
        if savingThread is None:
            video = []
        rec = False
    
                        
def terminate():
    global timer
    timer.cancel()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

