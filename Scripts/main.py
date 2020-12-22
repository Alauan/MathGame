import pygame as pg
from pygame.locals import *
import sys
from time import sleep
from typing import List

clock = pg.time.Clock()
pg.init()

# surfaces
WINDOWSIZE = 800, 500
screen = pg.display.set_mode(WINDOWSIZE)

# variables
mouse = {'buttons': [False, False, False], 'pos': (0, 0), 'just_pressed': [False, False, False]}
segurando = False
ini_mouse = mouse['pos']

# colors
WHITE = pg.Color(248, 251, 255)
TRANSPARENT_RED = pg.Color(255, 50, 50, 160)


# classes
class Polygon:
    def __init__(self, window_size, points: List[List[int]], color=(255, 50, 50, 140)):
        self.surface = pg.Surface(window_size, flags=SRCALPHA)
        self.ini_points = points
        self.points = points
        self.color = pg.Color(color)
        self.n_sides = len(points)
        self.is_hold = False

    def is_within(self, cursor) -> bool:
        odd_nodes = False
        for index in range(len(self.points)):
            if (self.points[index][1] > cursor[1] > self.points[index - 1][1] or self.points[index][1] < cursor[1] <
                self.points[index - 1][1]) \
                    and (cursor[0] >= self.points[index][0] or cursor[0] >= self.points[index - 1][0]):
                if (((self.points[index][0] - self.points[index - 1][0]) * (cursor[1] - self.points[index][1])) /
                      (self.points[index - 1][1] - self.points[index][1])) > self.points[index][0] - cursor[0]:
                    odd_nodes = not odd_nodes
        return odd_nodes

    def move(self, ini_cursor, fin_cursor):
        self.points = [[self.ini_points[p][0] + fin_cursor[0] - ini_cursor[0],
                        self.ini_points[p][1] + fin_cursor[1] - ini_cursor[1]] for p in range(self.n_sides)]

    def end_move(self):
        self.is_hold = False
        self.ini_points = self.points

    def draw(self):
        pg.draw.aalines(self.surface, self.color, True, self.points)
        pg.draw.polygon(self.surface, self.color, self.points)


polygons = [Polygon(WINDOWSIZE, [[10, 10], [10, 150], [250, 150]]),
            Polygon(WINDOWSIZE, [[10, 10], [10, 150], [250, 150], [300, 50], [100, 100]])]

# main loop
while True:
    screen.fill(WHITE)
    for poly in polygons:
        poly.surface.fill((0, 0, 0, 0))

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button <= 3:
                mouse['buttons'][event.button - 1] = True
                mouse['just_pressed'][event.button - 1] = True
        elif event.type == MOUSEBUTTONUP:
            if event.button <= 3:
                mouse['buttons'][event.button - 1] = False
        elif event.type == MOUSEMOTION:
            mouse['pos'] = event.pos

    if mouse['just_pressed'][0]:
        for poly in polygons:
            if poly.is_within(mouse['pos']):
                ini_mouse = mouse['pos']
                poly.is_hold = True

    for poly in polygons:
        if poly.is_hold:
            poly.move(ini_mouse, mouse['pos'])
            if mouse['buttons'][0] is False:
                poly.end_move()

    for poly in polygons:
        poly.draw()
        screen.blit(poly.surface, (0, 0))

    # screen update
    clock.tick(60)
    pg.display.update()

    # variable updates
    mouse['just_pressed'] = [False, False, False]
