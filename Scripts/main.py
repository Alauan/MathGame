import pygame as pg
from pygame.locals import *
import sys
from typing import List

clock = pg.time.Clock()
pg.init()

# colors
WHITE = pg.Color(248, 251, 255)
TRANSPARENT_RED = pg.Color(255, 50, 50, 160)
RED = pg.Color(255, 40, 40)
BLACK = pg.Color(0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

# surfaces
WINDOWSIZE = 900, 600
screen = pg.display.set_mode(WINDOWSIZE)
levelSurf = pg.Surface(WINDOWSIZE, flags=SRCALPHA)
clickSurf = pg.Surface(WINDOWSIZE, flags=SRCALPHA)


# level surface
def ref(points):
    size = 1
    reference = (-80, 100)
    if type(points[0]) == int:
        return int((points[0] + reference[0]) * size), int((points[1] + reference[1]) * size)
    else:
        result = []
        for point in points:
            result.append((int((point[0] + reference[0]) * size), int((point[1] + reference[1]) * size)))
        return result


levelSurf.fill(TRANSPARENT)
pg.draw.circle(levelSurf, BLACK, ref((400, 250)), 150, 1)
pg.draw.aalines(levelSurf, BLACK, True, ref(((250, 250), (550, 250), (809, 100), (164, 100))))
pg.draw.aaline(levelSurf, BLACK, ref((400, 450)), ref((400, 50)))


# variables
mouse = {'buttons': [False, False, False], 'pos': (0, 0), 'just_pressed': [False, False, False]}
ini_mouse = mouse['pos']
user_input = ''


# classes
class Polygon:
    def __init__(self, window_size, points, color=(255, 50, 50, 140)):
        self.surface = pg.Surface(window_size, flags=SRCALPHA)
        self.ini_points = points
        self.points = points
        self.color = pg.Color(color)
        self.n_sides = len(points)
        self.is_hold = False

    def update(self, clicou_agora: bool, cursor: List, ini_cursor: List, segurando: bool):
        """ This function must be executed every loop """
        self.surface.fill(TRANSPARENT)
        if clicou_agora:
            if self.is_within(cursor):
                self.is_hold = True
        if self.is_hold:
            if not segurando:
                self.is_hold = False
            else:
                self.move(ini_cursor, cursor)

        self.draw()

    def is_within(self, cursor) -> bool:
        """ Tells if a point is within the polygon """
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
        """ Moves the polygon """
        self.points = [[self.points[p][0] + fin_cursor[0] - ini_cursor[0],
                        self.points[p][1] + fin_cursor[1] - ini_cursor[1]] for p in range(self.n_sides)]

    def draw(self):
        """ Draws the polygon onto its surface """
        pg.draw.aalines(self.surface, self.color, True, self.points)
        pg.draw.polygon(self.surface, self.color, self.points)


class Click:
    def __init__(self, symbol: str, pos, surface):
        self.symbol = symbol
        self.pos = pos
        self.surface = surface
        self.box = pg.Rect((pos[0], pos[1], 30, 30))
        self.is_getting_input = False
        self.value = ' '

        self.font = pg.font.SysFont('Corbel', 30)
        self.symbol_surf = self.font.render(self.symbol, True, BLACK)

    def update(self, clicou_agora: bool, cursor: List, caractere: str):
        """ This function must be updated every loop """
        if clicou_agora:
            if self.is_within(cursor):
                self.is_getting_input = True
            else:
                if self.value not in ' ':
                    self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, BLACK)
                else:
                    self.symbol_surf = self.font.render(self.symbol, True, BLACK)
                self.is_getting_input = False
        if caractere == 'RETURN':
            if self.value not in ' ':
                self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, BLACK)
            else:
                self.symbol_surf = self.font.render(self.symbol, True, BLACK)
            self.is_getting_input = False
        if self.is_getting_input:
            self.open(caractere)

        self.blit()

    def is_within(self, cursor):
        return self.box.collidepoint(cursor)

    def open(self, text):
        if self.value != text:
            if text == 'BACKSPACE':
                self.value = self.value[:-1]
            else:
                self.value += text
            self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, RED)

    def blit(self):
        self.surface.blit(self.symbol_surf, self.pos)


polygons = [Polygon(WINDOWSIZE, [[10, 10], [10, 150], [250, 150]]),
            Polygon(WINDOWSIZE, [[10, 10], [10, 150], [250, 150], [300, 50], [100, 100]])]

clicaveis = [Click('α', (300, 300), clickSurf), Click('β', (400, 300), clickSurf)]

# main loop
while True:
    screen.fill(WHITE)
    clickSurf.fill(TRANSPARENT)

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

        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                user_input = 'BACKSPACE'
            elif event.key == K_RETURN:
                user_input = 'RETURN'
            else:
                user_input = event.unicode

    # processamento
    for poly in polygons:
        poly.update(mouse['just_pressed'][0], mouse['pos'], ini_mouse, mouse['buttons'][0])
    for clicavel in clicaveis:
        clicavel.update(mouse['just_pressed'][0], mouse['pos'], user_input)

    for poly in polygons:
        screen.blit(poly.surface, (0, 0))
    screen.blit(clickSurf, (0, 0))
    screen.blit(levelSurf, (0, 0))

    # screen update
    clock.tick(60)
    pg.display.update()

    # variable updates
    ini_mouse = mouse['pos']
    user_input = ''
    mouse['just_pressed'] = [False, False, False]
