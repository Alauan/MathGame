import pygame as pg
from pygame.locals import *
import sys
from math import sin, cos, tan, atan, pi
from typing import List, Tuple, Union
import math_functions as mf
import cursors

clock = pg.time.Clock()
pg.init()

# colors
WHITE = pg.Color(255, 250, 245)
TRANSPARENT_RED = pg.Color(255, 50, 50, 160)
TRANSPARENT_GREEN = pg.Color(10, 220, 10, 160)
TRANSPARENT_YELLOW = pg.Color(255, 255, 160, 160)
LIGHT_BLUE = (70, 100, 220)
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
surf = []
for i in range(6):
    surf.append(pg.Surface(WINDOWSIZE, flags=SRCALPHA))


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


surf[2].fill(TRANSPARENT)
pg.draw.circle(surf[2], BLACK, ref((400, 250)), 150, 1)
pg.draw.aalines(surf[2], BLACK, True, ref(((250, 250), (550, 250), (809, 100), (164, 100))))
pg.draw.aaline(surf[2], BLACK, ref((400, 450)), ref((400, 50)))
Enunciado = ['1- Os pontos B e F são extremidades da circunferência de equação x² + y² = 81 e o segmento ',
             'DE é tangente à circunferência dada no ponto C(0, 9)']
for index, linha in enumerate(Enunciado):
    surf[2].blit(font_enunciado.render(linha, True, BLACK), (60, 25 * index + 40))

# variables
mouse = {'buttons': [False, False, False], 'pos_rect': (0, 0), 'just_pressed': [False, False, False]}
ini_mouse = mouse['pos_rect']
user_input = ''
contar = []
contador = {}  # this dictionary will be used for animations, the key will be a string containing p for polygons and
# c for clickables + ' ' + index, ex.: 'p 1' for the polygon with index 1. The value is the counter.


# classes
class Polygon:
    def __init__(self, surface, points, position, right_point=(0, 0), rotation=0, right_rotation=0, color=BLACK):
        self.surface = surface
        self.pre_surface = pg.Surface(WINDOWSIZE, flags=SRCALPHA)  # this surface is needed to make transparency
        # between polygons
        self.position = list(position)
        self.rotation = rotation  # In degrees
        self.right_rotation = right_rotation
        self.barycentre = mf.barycentre(points, get_round=True)  # Center point to make rotations
        self.points = tuple(points)
        self.rel_pts = list(points)  # Points relative to position and rotation
        self.transform()

        self.color = pg.Color(color)
        self.fill_color = (0, 0, 0, 30)
        self.right_point = list(right_point)  # The point witch the polygon will stick
        self.n_sides = len(points)
        self.is_hold = [0, 0, 0]  # holds a list containing mouse buttons that were pressed inside the polygon

    def update(self, clicou_agora: Union[List, Tuple], cursor: List, ini_cursor: List, segurando: Union[List, Tuple]):
        """ Exceptionally, self.draw() is not inside update() because there are some cases that I want to
        draw the polygons and not be able to move them"""
        soltou_agora = False
        if any(clicou_agora):
            if mf.is_within(self.rel_pts, cursor):
                self.is_hold = clicou_agora
        if self.is_hold[0]:
            if segurando[0]:
                self.transform(ini_cursor, cursor, move=True)
            else:
                soltou_agora = True
                self.is_hold[0] = False
        if self.is_hold[2]:
            if segurando[2]:
                self.transform(ini_cursor, cursor, rotate=True)
            else:
                soltou_agora = True
                self.is_hold[2] = False

        ang_tolerance = 10
        lin_tolerance = 15
        """ goes into right position and angle if inside tolerances """
        if soltou_agora:
            if abs(self.position[0] - self.right_point[0]) < lin_tolerance \
                    and abs(self.position[1] - self.right_point[1]) < lin_tolerance:
                if (self.right_rotation < ang_tolerance and
                    (self.rotation > 360 - ang_tolerance - self.right_rotation
                     or self.rotation < self.right_rotation + ang_tolerance)) or \
                        (self.right_rotation > ang_tolerance and
                         self.right_rotation - ang_tolerance < self.rotation < self.right_rotation + ang_tolerance):
                    self.position = self.right_point
                    self.rotation = self.right_rotation
                    self.transform()

    def transform(self, ini_cursor=(0, 0), fin_cursor=(0, 0), move=False, rotate=False):
        """ Moves or rotates the polygon """
        """ Unfortunately I couldn't make two separate auxiliar"""
        global mouse_cursor
        self.rotation = self.rotation % 360
        if rotate:
            mouse_cursor = 'ROTATE'
            self.rotation += (fin_cursor[1] - ini_cursor[1] - fin_cursor[0] + ini_cursor[0]) / 2
        if move:
            mouse_cursor = 'MOVE'
            self.position = [self.position[0] + fin_cursor[0] - ini_cursor[0],
                             self.position[1] + fin_cursor[1] - ini_cursor[1]]

        rotated = mf.rotate(self.points, self.barycentre, self.rotation)
        self.rel_pts = [(self.position[0] + point[0], self.position[1] + point[1]) for point in rotated]

    def is_in_right_point(self):
        return self.position == self.right_point

    def draw(self):
        """ Draws the polygon onto its surface """
        self.pre_surface.fill(TRANSPARENT)
        pg.draw.polygon(self.pre_surface, self.fill_color, self.rel_pts)
        pg.draw.lines(self.pre_surface, self.color, True, self.rel_pts, 2)
        self.surface.blit(self.pre_surface, (0, 0))


class Click:
    def __init__(self, symbol: str, pos, surface, right_value):
        self.symbol = symbol
        self.pos = pos
        self.surface = surface
        self.right_value = right_value
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
                self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, LIGHT_BLUE)
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
            self.symbol_surf = self.font.render(self.symbol + '=' + self.value, True, LIGHT_BLUE)

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


polygons = [Polygon(surf[3], [[0, 0], [0, 148], [298, 148], [298, 0]], [600, 400], (171, 200), 40),
            Polygon(surf[3], [[0, 0], [259, 0], [0, 150]], [450, 400], (471, 200), 140),
            Polygon(surf[3], [[0, 0], [85, 150], [85, 0]], [350, 400], (85, 200), 270)]
polygons_update = []  # these polygons will be updated
polygons_show = []  # these polygons will be shown
polygon_near = -1  # tells witch polygon is "near". When the value is -1, none of them are

ticks = 15
anim_info_poly = [[(100, 100), 2.4, 0], [(600, 350), 2.4, 180], [(500, 200), 4, 85]]
for index, info in enumerate(anim_info_poly):
    go_to = info[0]
    resize = info[1] - 1
    rotation = info[2]
    stepX = (go_to[0] - polygons[index].right_point[0]) / ticks
    stepY = (go_to[1] - polygons[index].right_point[1]) / ticks
    rot_step = rotation / ticks
    anim_info_poly[index] = {'steps': (stepX, stepY), 'rot_step': rot_step, 'resize': resize, 'ticks': ticks}

clicaveis = [Click('α', (346, 218), surf[1], '90'),
             Click('R', (340, 285), surf[1], '9'),
             Click('b', (419, 108), surf[-1], '18')]
clicaveis_update = [0, 1]  # these clicaveis will be shown and updated
highlights = [[57, 62, 253, 23], [595, 37, 96, 23], None]
highlines = [None, [(320, 200), (320, 350)], [(100, 100), (816, 100)]]

angles = [[Angle(270, 89, (320, 200), surf[1])],
          [Angle(0, 120, (170, 350), surf[1], (195, 310))],
          [Angle(30, 150, (470, 350), surf[1], (398, 307))],
          [Angle(270, 90, (100, 101), surf[-1]), Angle(180, 90, (814, 101), surf[-1]),
          Angle(0, 90, (100, 455), surf[-1]), Angle(90, 90, (814, 455), surf[-1])],
          [Angle(210, 60, (774, 91), surf[-1], (734, 130), 70), Angle(90, 90, (774, 450), surf[-1]),
          Angle(0, 30, (151, 450), surf[-1], tamanho=80)]]
angles_update = [0, 1, 2]  # these angles will be shown and updated

# main loop
while True:
    mouse_cursor = 'ARROW'
    screen.fill(WHITE)
    for index, surface in enumerate(surf):
        if index != 2:
            surface.fill(TRANSPARENT)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button <= 3:
                mouse['buttons'][event.button - 1] = True
                mouse['just_pressed'][event.button - 1] = True
                if event.button == 1:
                    print(mouse['pos_rect'])
                else:
                    print(f'\033[1;32m{mouse["pos_rect"]}\033[m')
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
    if any([b.is_within(mouse['pos_rect']) and index in clicaveis_update for index, b in enumerate(clicaveis)]):
        mouse_cursor = 'HAND'
    for index in angles_update:
        for angulo in angles[index]:
            angulo.draw()

    if polygons_show:
        # splitting the angles according to the polygons that are in place
        if len(angles[1]) == 1:
            if polygons[0].is_in_right_point() or polygons[2].is_in_right_point():
                angles[1] = [Angle(0, 90, (170, 350), surf[1], (195, 310)),
                             Angle(90, 30, (170, 350), surf[1], (142, 284), tamanho=70)]
        if len(angles[2]) == 1:
            if polygons[0].is_in_right_point() or polygons[1].is_in_right_point():
                angles[2] = [Angle(30, 60, (470, 350), surf[1], (480, 301)),
                             Angle(90, 90, (470, 350), surf[1], (412, 310))]

        # stopping to update polygons that are already on the right spot
        for index in polygons_update:
            if polygons[index].is_in_right_point():
                polygons_update.remove(index)

        # starting animations
        if mouse['just_pressed'][0]:
            if polygon_near >= 0:
                if not mf.is_within(polygons[polygon_near].rel_pts, mouse['pos_rect']):
                    polygons[polygon_near].surface = surf[3]
                    contador[f'p {polygon_near}'] = anim_info_poly[polygon_near]['ticks'] - 1
                    polygon_near = -1

            if all(poly.is_in_right_point() for poly in polygons):
                for index, poly in enumerate(polygons):
                    if mf.is_within(poly.rel_pts, mouse['pos_rect']):
                        polygon_near = index
                        polygons[index].surface = surf[4]
                        contador[f'p {index}'] = anim_info_poly[index]['ticks'] - 1

    else:
        if 0 in clicaveis_update:
            if clicaveis[0].is_value_right():
                angles[0][0].grau = 90
                clicaveis_update.remove(0)

        if all([clicavel.is_value_right() for clicavel in clicaveis[:2]]):
            polygons_update += (0, 1, 2)
            polygons_show += (0, 1, 2)

    for index, clicavel in enumerate(clicaveis):
        if clicavel.is_getting_input:
            if highlights[index]:
                pg.draw.rect(surf[0], YELLOW, highlights[index])
            if highlines[index]:
                pg.draw.line(surf[-1], RED, *highlines[index], width=3)

    # animation
    for key, n in contador.items():
        index = int(key.split()[-1])
        obj = key.split()[0]
        count_to_1 = (anim_info_poly[index]['ticks'] - n) / anim_info_poly[index]['ticks']
        count_to_0 = 1 - count_to_1
        if obj == 'p':
            if polygon_near >= 0:
                polygons[index].rotation += anim_info_poly[index]['rot_step']
                polygons[index].position = mf.add_vectors(polygons[index].position, anim_info_poly[index]['steps'])
                polygons[index].transform((0, 0), (0, 0))
                polygons[index].rel_pts = mf.resize(polygons[index].rel_pts,
                                                    count_to_1 * anim_info_poly[index]['resize'] + 1)
                polygons[index].fill_color = (count_to_1 * 255,
                                              count_to_1 * 255, count_to_1 * 255, count_to_1 * 225 + 30)
            else:
                polygons[index].rotation -= anim_info_poly[index]['rot_step']
                polygons[index].position = mf.sub_vectors(polygons[index].position, anim_info_poly[index]['steps'])
                polygons[index].transform((0, 0), (0, 0))
                polygons[index].rel_pts = mf.resize(polygons[index].rel_pts,
                                                    count_to_0 * anim_info_poly[index]['resize'] + 1)
                polygons[index].fill_color = (count_to_0 * 255,
                                              count_to_0 * 255, count_to_0 * 255, count_to_0 * 225 + 30)

        if n == 0:  # if the counting ended
            if polygon_near == -1:
                # I have to do this because they don't return correctly sometimes
                polygons[index].position = polygons[index].right_point
                polygons[index].rotation = polygons[index].right_rotation
            if polygon_near == 0:
                clicaveis_update.append(2)
                angles_update.append(3)
            elif polygon_near == 1:
                angles_update.append(4)

        if n == anim_info_poly[index]['ticks'] - 1:  # if counting started
            if key == 'p 0' and polygon_near == -1:
                clicaveis_update.remove(2)
                angles_update.remove(3)
            if key == 'p 1' and polygon_near == -1:
                angles_update.remove(4)

    # screen assembly
    for surface in surf:
        screen.blit(surface, (0, 0))

    # screen update
    clock.tick(60)
    pg.display.update()

    # variable updates
    ini_mouse = mouse['pos_rect']
    user_input = ''
    mouse['just_pressed'] = [False, False, False]
    keys_to_pop = []
    for key in contador:
        if contador[key] > 0:
            contador[key] -= 1
        else:
            keys_to_pop.append(key)
    for key in keys_to_pop:
        contador.pop(key)

    # cursor update
    if mouse_cursor == 'HAND':
        pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
    if mouse_cursor == 'ARROW':
        pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
    if mouse_cursor == 'MOVE':
        pg.mouse.set_cursor((16, 16), (0, 0), *cursors.move_cursor)
    if mouse_cursor == 'ROTATE':
        pg.mouse.set_cursor((16, 16), (0, 0), *cursors.rotate_cursor)
