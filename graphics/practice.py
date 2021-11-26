import pygame, sys
from pygame.locals import *
pygame.init()
x,y = 0,0
background = pygame.image.load("background1.jpeg")
screen = pygame.display.set_mode((background.get_width(), background.get_height()))
pygame.display.set_caption("animation")
bird = pygame.image.load("picture.jpeg").convert_alpha()
sound= pygame.mixer.Sound("The Beatles - Let It be lyrics 2.mp4")
pygame.mixer.Channel(5).play(sound)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0,0))
    screen.blit(bird, (x,y))
    pygame.display.update()
    x +=1
    pygame.time.wait(50)

