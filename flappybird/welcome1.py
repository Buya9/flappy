
import pygame, random, sys
from pygame.locals import *
from itertools import cycle

FPS = 30
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
PIPE_GAP =100
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
    
    IMAGES['pipe'] = (
        pygame.transform.flip(
            pygame.image.load("assets/sprites/pipe-green.png").convert_alpha(),
                              False,True),
        pygame.image.load(
            "assets/sprites/pipe-green.png").convert_alpha(),
        
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
    info = show_welcome_screen()
    play_game(info)
    # show_score()


def show_welcome_screen():
    """Ehleliin delgets"""
    global SPEED, BASE_MAX_SHIFT
    SPEED =4
    playerModel = cycle((0, 1, 2, 1))
    modelNumber = 0
    messageX = int((SCREEN_WIDTH-IMAGES["message"].get_width()) / 2)
    messageY = int(SCREEN_HEIGHT*0.12)
    playerY = int((SCREEN_HEIGHT-IMAGES["player"][0].get_height()) / 2)
    BASE_MAX_SHIFT = IMAGES["base"].get_width() - SCREEN_WIDTH
    baseX = 0
    currentAlt ={"alt" :0, "dir":1}
    fpsCount =0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key ==K_SPACE:
                SOUNDS["wing"].play()
                return {
                    'playerY':  set_alt(currentAlt),
                    'baseX'  : baseX 
                    }

        SCREEN.blit(IMAGES["background"], (0, 0))
        SCREEN.blit(IMAGES["base"], (-(baseX % BASE_MAX_SHIFT), BASE_Y))
        SCREEN.blit(IMAGES["message"], (messageX, messageY))
        SCREEN.blit(IMAGES["player"][modelNumber], (70, set_alt(currentAlt)))

        pygame.display.update()
        baseX += SPEED
        fpsCount +=1
        if fpsCount %5==0:
            modelNumber =next(playerModel)
        FPSCLOCK.tick(FPS)


def play_game(info):
    ###
    playerVelY = -9  #playeriin shiljih hurd
    FLAP_ACC = -9    #dalavch deveh huch
    MAX_VEL = 10    # dooshoo unah max hurd
    ROT_VEL =3   #player iin dooshoo ergeh hurd
    gravity = 1    # gazriin tatah hucgnii hurdatgal
    ROT_THRESH = 20  # deeshee ergeh max ontsog
    MAX_ROT = 45    # deeshee ergeh hayzgaar
    MIN_ROT = -90   # doodhoo ergeh hayzgaar
    ###
    
    baseX =info['baseX']
    playerModel = cycle((0, 1, 2, 1))
    modelNumber = 0
    fpsCount =0
    playerX, playerY = 70, info['playerY']
    playerHeight = IMAGES['player'][modelNumber].get_height()
    player_angle = MAX_ROT 
    pipes =[]
    pipes.append(get_pipe())
    pipes.append(get_pipe())
    pipes[0]['x'] = SCREEN_WIDTH /2 +200
    pipes[1]['x'] = SCREEN_WIDTH +200
      
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key ==K_SPACE:
                
                if playerY > -2*playerHeight:
                    SOUNDS["wing"].play()
                    playerVelY =FLAP_ACC
                    player_angle = MAX_ROT
        # Hurdnii hayzgaariig dawaagui bol unah hurdatgaliin nem            
        if playerVelY < MAX_VEL:   
            playerVelY +=gravity
        
        if pipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            del(pipes[0]) 
        if 0 < pipes[0]['x'] <5:
            pipes.append(get_pipe())
        #ergeltiin hyzgaariig dawagui bol ergeh angliig nem
        if player_angle > MIN_ROT:
            player_angle -= ROT_VEL;
        angle = min(player_angle, ROT_THRESH)
        playerY +=min( playerVelY, BASE_Y - playerY -  playerHeight )  
        # Animation heseg
        SCREEN.blit(IMAGES["background"], (0, 0))
        
        for pipe in pipes:
            pipe['x'] -= SPEED
            SCREEN.blit(IMAGES["pipe"][0], (pipe['x'], pipe['uUpper']))
            SCREEN.blit(IMAGES["pipe"][1], (pipe['x'], pipe['uLower']))

            
        SCREEN.blit(IMAGES["base"], (-(baseX % BASE_MAX_SHIFT), BASE_Y))
        playerSurface =pygame.transform.rotate(IMAGES["player"][modelNumber], angle)
        SCREEN.blit( playerSurface, (playerX, playerY))

        pygame.display.update()
        baseX += SPEED
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

def get_pipe():
    pipe_height =IMAGES['pipe'][0].get_height()
    x = SCREEN_WIDTH +10
    yLower = random.randint(int(SCREEN_HEIGHT *0.4), int(SCREEN_HEIGHT*0.6))
    yUpper = yLower - PIPE_GAP-pipe_height
    
    return {'x' :x, 'yLower': yLower, 'yUpper': yUpper }
if __name__ == "__main__":
    main()
