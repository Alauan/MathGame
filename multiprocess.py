import pygame
from time import sleep

GREEN = pygame.Color('green')
RED = pygame.Color('red')

transparent_red = RED
transparent_red[3] = 125

size = (800, 400)

pygame.init()
screen = pygame.display.set_mode(size)

lowersurf = pygame.Surface(size)
lowersurf.fill(GREEN)

polysurf = pygame.Surface(size, flags=pygame.SRCALPHA)
pygame.draw.polygon(polysurf, transparent_red, ((100, 100), (600, 100), (600, 200), (350, 300), (100, 200)))

lowersurf.blit(polysurf, (0, 0))

screen.blit(lowersurf, (0, 0))
pygame.display.flip()

sleep(10)