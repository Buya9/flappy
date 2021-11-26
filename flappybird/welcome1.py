import pygame
from pygame.locals import *
from itertools import cycle
import sys
FPS = 30
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

BASE_Y = int(SCREEN_HEIGHT * 0.8)
IMAGES, SOUNDS = {}, {}


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy bird")
    IMAGES['numbers'] = (
        pygame.image.load("assets/sprites/0.png").convert_alpha(),
        pygame.image.load("assets/sprites/1.png").convert_alpha(),
        pygame.image.load("assets/sprites/2.png").convert_alpha(),
        pygame.image.load("assets/sprites/3.png").convert_alpha(),
        pygame.image.load("assets/sprites/4.png").convert_alpha(),
        pygame.image.load("assets/sprites/5.png").convert_alpha(),
        pygame.image.load("assets/sprites/6.png").convert_alpha(),
        pygame.image.load("assets/sprites/7.png").convert_alpha(),
        pygame.image.load("assets/sprites/8.png").convert_alpha(),
        pygame.image.load("assets/sprites/9.png").convert_alpha(),
    )
    IMAGES["background"] = pygame.image.load(
        "assets/sprites/background-day.png").convert()
    IMAGES['player'] = (
        pygame.image.load(
            "assets/sprites/yellowbird-upflap.png").convert_alpha(),
        pygame.image.load(
            "assets/sprites/yellowbird-midflap.png").convert_alpha(),
        pygame.image.load(
            "assets/sprites/yellowbird-downflap.png").convert_alpha(),
    )
    IMAGES["message"] = pygame.image.load(
        "assets/sprites/message.png").convert_alpha()
    IMAGES["gameover"] = pygame.image.load(
        "assets/sprites/gameover.png").convert()
    IMAGES["base"] = pygame.image.load("assets/sprites/base.png").convert()
    print(sys.platform)
    if "win" in sys.platform:
        soundExt = ".wav"
    else:
        soundExt = ".ogg"
    SOUNDS["die"] = pygame.mixer.Sound("assets/audio/die" + soundExt)
    SOUNDS["hit"] = pygame.mixer.Sound("assets/audio/hit" + soundExt)
    SOUNDS["swoosh"] = pygame.mixer.Sound("assets/audio/swoosh" + soundExt)
    SOUNDS["wing"] = pygame.mixer.Sound("assets/audio/wing" + soundExt)
    SOUNDS["theme"] = pygame.mixer.Sound("assets/audio/theme" + soundExt)
    show_welcome_screen()
    # play_game()
    # show_score()


def show_welcome_screen():
    """Ehleliin delgets"""
    playerModel = cycle((0, 1, 2, 1))
    modelNumber = 0
    messageX = int((SCREEN_WIDTH-IMAGES["message"].get_width()) / 2)
    messageY = int(SCREEN_HEIGHT*0.12)
    playerY = int((SCREEN_HEIGHT-IMAGES["player"][0].get_height()) / 2)
    baseMaxShift = IMAGES["base"].get_width() - SCREEN_WIDTH
    baseX = 0
    currentAlt ={"alt" :0, "dir":1}
    fpsCount =0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(IMAGES["background"], (0, 0))
        SCREEN.blit(IMAGES["base"], (-(baseX % baseMaxShift), BASE_Y))
        SCREEN.blit(IMAGES["message"], (messageX, messageY))
        SCREEN.blit(IMAGES["player"][modelNumber], (70, set_alt(currentAlt)))

        pygame.display.update()
        baseX += 4
        fpsCount +=1
        if fpsCount %5==0:
            modelNumber =next(playerModel)
        FPSCLOCK.tick(FPS)

def set_alt(currentAlt):
    playerY = int((SCREEN_HEIGHT-IMAGES["player"][0].get_height()) / 2)
    
    if abs(currentAlt["alt"]) ==16: 
        currentAlt["dir"]*=-1
    if currentAlt["dir"]==1:
        currentAlt["alt"]+=1
    else:
        currentAlt["alt"]-=1
        
    alt=playerY + currentAlt["alt"]
    return alt
        
if __name__ == "__main__":
    main()
