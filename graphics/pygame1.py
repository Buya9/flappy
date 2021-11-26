import pygame
pygame.init()
screen = pygame.display.set_mode((240,380))
imgSurface= pygame.image.load("picture.jpeg").convert_alpha()
screen.blit(imgSurface,(0,0))
pygame.display.update()