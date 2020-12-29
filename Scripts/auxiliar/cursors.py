import pygame as pg


move_cursor = pg.cursors.compile((
    "       XX       ",
    "      XXXX      ",
    "     XX  XX     ",
    "                ",
    "       XX       ",
    "  X    XX    X  ",
    " XX    XX    XX ",
    "XX  XXXXXXXX  XX",
    "XX  XXXXXXXX  XX",
    " XX    XX    XX ",
    "  X    XX    X  ",
    "       XX       ",
    "                ",
    "     XX  XX     ",
    "      XXXX      ",
    "       XX       "
), black='X', white='.', xor='o')

rotate_cursor = pg.cursors.compile((
    "    XXXXXXXX    ",
    "   XXXXXXXXXX   ",
    "  XXX      XXX  ",
    " XXX        XXX ",
    " XX          XX ",
    " XX          XX ",
    " XX          XX ",
    " XX          XX ",
    " XX          XX ",
    " XX     XX  XXX ",
    " XXX    XX XXX  ",
    "  XXX   XX XX   ",
    "   XXX  XX      ",
    "    XX  XXXXXX  ",
    "        XXXXXX  ",
    "                ",
), black='X', white='.', xor='o')