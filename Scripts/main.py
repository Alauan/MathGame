import pygame as pg
from pygame.locals import *
import sys
from math import sin, cos, tan, atan, pi
from typing import List, Tuple, Union
import math_functions as mf

clock = pg.time.Clock()
pg.init()

# colors
WHITE = pg.Color(255, 250, 245)
TRANSPARENT_RED = pg.Color(255, 50, 50, 160)
TRANSPARENT_GREEN = pg.Color(10, 220, 10, 160)
TRANSPARENT_YELLOW = pg.Color(255, 255, 160, 160)
RED = pg.Color(255, 40, 40)
GREEN = pg.Color(10, 190, 10)
YELLOW = pg.Color(255, 255, 0)
BLACK = pg.Color(0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)

# fonts
font_enunciado = pg.font.SysFont('Calibri', 20)

# surfaces
WINDOWSIZE = 900, 600
screen = pg.display.set_mode(WINDOWSIZE)
levelSurf = pg.Surface(WINDOWSIZE, flags=SRCALPHA)
clickSurf = pg.Surface(WINDOWSIZE, flags=SRCALPHA)
highlights = pg.Surface(WINDOWSIZE, flags=SRCALPHA)


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
Enunciado = ['1- Os pontos B e F são extremidades da circunferência de equação x² + y² = 81 e o segmento ',
             'DE é tangente à circunferência dada no ponto C(0, 9)']
for index, linha in enumerate(Enunciado):
    levelSurf.blit(font_enunciado.render(linha, True, BLACK), (60, 25*index+40))

# variables
mouse = {'buttons': [False, False, False], 'pos_rect': (0, 0), 'just_pressed': [False, False, False]}
ini_mouse = mouse['pos_rect']
user_input = ''
contar = []
contador = {}


# classes
class Polygon:
    def __init__(self, window_size, points, position, right_point=(0, 0), rotation=0, color=RED):
        self.surface = pg.Surface(window_size, flags=SRCALPHA)
        self.position = list(position)
        self.rotation = rotation  # In degrees
        self.barycentre = mf.barycentre(points, get_round=True)  # Center point to make rotations
        self.points = tuple(points)
        self.rel_pts = list(points)  # Points relative to position and rotation
        self.transform((0, 0), (0, 0))

        self.color = pg.Color(color)
        self.right_point = list(right_point)  # The point witch the polygon will stick
        self.n_sides = len(points)
        self.is_hold = [0, 0, 0]  # holds a list containing mouse buttons that were pressed inside the polygon

    def update(self, clicou_agora: Union[List, Tuple], cursor: List, ini_cursor: List, segurando: Union[List, Tuple]):
        """ This function must be executed every loop """
        """ Exceptionally, self.draw() is not inside update() because there are some cases that I want to 
        draw the polygons and not be able to move them"""
        self.surface.fill(TRANSPARENT)
        if any(clicou_agora):
            if self.is_within(cursor):
                self.is_hold = clicou_agora
        if self.is_hold[0]:
            if segurando[0]:
                self.transform(ini_cursor, cursor, move=True)
            else:
                self.is_hold[0] = False
                if abs(self.position[0] - self.right_point[0]) < 15 and \
                        abs(self.position[1] - self.right_point[1]) < 15:
                    self.transform(self.position, self.right_point, move=True)
        if self.is_hold[2]:
            if segurando[2]:
                self.transform(ini_cursor, cursor, rotate=True)
            else:
                self.is_hold[2] = False

    def is_within(self, cursor) -> bool:
        """ Tells if a point is within the polygon """
        odd_nodes = False
        for index in range(len(self.rel_pts)):
            if (self.rel_pts[index][1] > cursor[1] > self.rel_pts[index - 1][1] or self.rel_pts[index][1]
                < cursor[1] < self.rel_pts[index - 1][1]) \
                    and (cursor[0] >= self.rel_pts[index][0] or cursor[0] >= self.rel_pts[index - 1][0]):
                if (((self.rel_pts[index][0] - self.rel_pts[index - 1][0]) * (cursor[1] - self.rel_pts[index][1])) /
                        (self.rel_pts[index - 1][1] - self.rel_pts[index][1])) > self.rel_pts[index][0] - cursor[0]:
                    odd_nodes = not odd_nodes
        return odd_nodes

    def transform(self, ini_cursor, fin_cursor, move=False, rotate=False):
        """ Moves or rotates the polygon """
        """ Unfortunately I couldn't make two separate functions"""
        if rotate:
            self.rotation += fin_cursor[1] - ini_cursor[1]
        if move:
            self.position = [self.position[0] + fin_cursor[0] - ini_cursor[0],
                             self.position[1] + fin_cursor[1] - ini_cursor[1]]
        rotated = []
        for index in range(len(self.points)):
            hip = mf.distance(self.barycentre, self.points[index])
            tangente = (self.points[index][1] - self.barycentre[1]) / (self.points[index][0] - self.barycentre[0])
            angle = atan(tangente)

            if angle > 0 and self.points[index][0] - self.barycentre[0] < 0:
                angle += pi
            elif angle < 0 and self.points[index][0] - self.barycentre[0] < 0:
                angle += pi

            angle += self.rotation / 57.29
            co = round(sin(angle) * hip)
            ca = round(cos(angle) * hip)
            rotated.append((self.barycentre[0] + co, self.barycentre[1] + ca))
        print(rotated)
        self.rel_pts = [(self.position[0] + point[0], self.position[1] + point[1]) for point in rotated]

    def is_in_right_point(self):
        return self.position == self.right_point

    def draw(self):
        """ Draws the polygon onto its surface """
        pg.draw.polygon(self.surface, (0, 0, 0, 30), self.rel_pts)
        pg.draw.lines(self.surface, self.color, True, self.rel_pts, 2)


class Click:
    def __init__(self, symbol: str, pos, surface, right_value, rect=None):
        self.symbol = symbol
        self.pos = pos
        self.surface = surface
        self.right_value = right_value
        self.rect = rect
        self.box = pg.Rect((pos[0], pos[1], 30, 30))
        self.value = ''
        self.is_getting_input = False

        self.font = pg.font.SysFont('Corbel', 30)
        self.symbol_surf = self.font.render(self.symbol, True, BLACK)

    def update(self, clicou_agora: bool, cursor: List, caractere: str):
        """ This function must be updated every loop """
        terminou = False
        if clicou_agora:
            if self.is_within(cursor):
                self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, RED)
                self.is_getting_input = True
            else:
                terminou = True
        if caractere == 'RETURN':
            terminou = True
        if terminou:
            if self.value.strip() == self.right_value:
                cor = GREEN
            else:
                cor = BLACK
            if self.value not in '':
                self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, cor)
            else:
                self.symbol_surf = self.font.render(self.symbol, True, cor)
            self.is_getting_input = False

        if self.is_getting_input:
            self.open(caractere)
            if self.rect:
                pg.draw.rect(self.surface, YELLOW, self.rect)
        self.blit()

    def is_value_right(self):
        return self.value.strip() == self.right_value and not self.is_getting_input

    def is_within(self, cursor):
        return self.box.collidepoint(cursor)

    def open(self, text):
        if text != '':
            if text == 'BACKSPACE':
                self.value = self.value[:-1]
            else:
                self.value += text
            self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, RED)

    def blit(self):
        self.surface.blit(self.symbol_surf, self.pos)


class Angle:
    def __init__(self, comeco, grau, pos, surface, num_pos=None, tamanho=50):
        self.comeco_rad = comeco / 57.29
        self.grau_rad = grau / 57.29
        self.grau = grau
        self.pos_rect = (pos[0] - tamanho // 2, pos[1] - tamanho // 2)
        self.pos = pos
        self.surface = surface
        self.num_pos = num_pos
        self.tamanho = tamanho

        if num_pos:
            font = pg.font.SysFont('Calibri', 20)
            self.num_surf = font.render(str(grau) + '°', True, RED)
        else:
            self.num_surf = None

    def draw(self):
        if self.grau != 90:
            pg.draw.arc(self.surface, RED, (self.pos_rect[0], self.pos_rect[1], self.tamanho, self.tamanho),
                        self.comeco_rad, self.comeco_rad + self.grau_rad, 1)
        else:
            pg.draw.aalines(self.surface, RED, False,
                            [(self.pos[0] + self.tamanho // 2 * cos(self.comeco_rad),
                              self.pos[1] + -self.tamanho // 2 * sin(self.comeco_rad)),
                             (self.pos[0] + self.tamanho * 1.41 // 2 * cos(self.comeco_rad + 0.78),
                              self.pos[1] + -self.tamanho * 1.41 // 2 * sin(self.comeco_rad + 0.78)),
                             (self.pos[0] + self.tamanho // 2 * cos(self.comeco_rad + 1.57),
                              self.pos[1] + -self.tamanho // 2 * sin(self.comeco_rad + 1.57))])
            pg.draw.circle(self.surface, RED,
                           (self.pos[0] + self.tamanho * 0.7 // 2 * cos(self.comeco_rad + 0.78),
                            self.pos[1] + -self.tamanho * 0.7 // 2 * sin(self.comeco_rad + 0.78)), 2, 3)
        if self.num_surf:
            self.surface.blit(self.num_surf, self.num_pos)


polygons = [Polygon(WINDOWSIZE, [[0, 0], [0, 148], [298, 148], [298, 0]], [600, 400], (171, 201)),
            Polygon(WINDOWSIZE, [[0, 0], [259, 0], [0, 150]], [450, 400], (471, 200), color=GREEN),
            Polygon(WINDOWSIZE, [[0, 0], [85, 150], [85, 0]], [350, 400], (85, 200), color=YELLOW)]
polygons_update = []  # these polygons will be updated
polygons_show = []  # these polygons will be shown
polygons_update.extend((0, 1, 2))
polygons_show.extend((0, 1, 2))

clicaveis = [Click('α', (346, 218), clickSurf, '90', [57, 62, 253, 23]),
             Click('R', (340, 285), clickSurf, '9', [595, 37, 96, 23])]
clicaveis_update = [0, 1]  # these clicaveis will be shown and updated

angles = [[Angle(270, 89, (320, 200), clickSurf)],
          [Angle(0, 120, (170, 350), clickSurf, (195, 310))],
          [Angle(30, 150, (470, 350), clickSurf, (398, 307))]]
angles_update = [0, 1, 2]  # these angles will be shown and updated

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
                print(mouse['pos_rect'])
        elif event.type == MOUSEBUTTONUP:
            if event.button <= 3:
                mouse['buttons'][event.button - 1] = False
        elif event.type == MOUSEMOTION:
            mouse['pos_rect'] = event.pos

        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                user_input = 'BACKSPACE'
            elif event.key == K_RETURN:
                user_input = 'RETURN'
            else:
                user_input = event.unicode

    # processing
    for index in polygons_update:
        polygons[index].update(mouse['just_pressed'], mouse['pos_rect'], ini_mouse, mouse['buttons'])
    for index in polygons_show:
        polygons[index].draw()
    for index in clicaveis_update:
        clicaveis[index].update(mouse['just_pressed'][0], mouse['pos_rect'], user_input)
    for index in angles_update:
        for angulo in angles[index]:
            angulo.draw()

    if polygons_show:
        # splitting the angles according to the polygons
        if len(angles[1]) == 1:
            if polygons[0].is_in_right_point() or polygons[2].is_in_right_point():
                angles[1] = [Angle(0, 90, (170, 350), clickSurf, (195, 310)),
                             Angle(90, 30, (170, 350), clickSurf, (142, 284), tamanho=70)]
        if len(angles[2]) == 1:
            if polygons[0].is_in_right_point() or polygons[1].is_in_right_point():
                angles[2] = [Angle(30, 60, (470, 350), clickSurf, (480, 301)),
                             Angle(90, 90, (470, 350), clickSurf, (412, 310))]

        # stopping to update polygons that are already on the right spot
        for index in polygons_update:
            if polygons[index].is_in_right_point():
                polygons_update.remove(index)

    else:
        if 0 in clicaveis_update:
            if clicaveis[0].is_value_right():
                angles[0][0].grau = 90
                clicaveis_update.remove(0)

        if all([clicavel.is_value_right() for clicavel in clicaveis]):
            polygons_update.extend((0, 1, 2))
            polygons_show.extend((0, 1, 2))

    for key in contador:
        contador[key] -= 1

    # screen assembly
    screen.blit(clickSurf, (0, 0))
    screen.blit(levelSurf, (0, 0))
    for poly in polygons:
        screen.blit(poly.surface, (0, 0))

    # screen update
    clock.tick(60)
    pg.display.update()

    # variable updates
    ini_mouse = mouse['pos_rect']
    user_input = ''
    mouse['just_pressed'] = [False, False, False]
