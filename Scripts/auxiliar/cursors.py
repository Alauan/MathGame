import pygame as pg


move_cursor = pg.cursors.compile((
    "       X        ",
    "      XXX       ",
    "     XX XX      ",
    "                ",
    "       X        ",
    "  X    X    X   ",
    " XX   XXX   XX  ",
    "XX  XXX XXX  XX ",
    " XX   XXX   XX  ",
    "  X    X    X   ",
    "       X        ",
    "                ",
    "     XX XX      ",
    "      XXX       ",
    "       X        ",
    "                "
), black='X', white='.', xor='o')

rotate_cursor = pg.cursors.compile((
    "     XXXXXX     ",
    "   XXX    XXX   ",
    "  XX        XX  ",
    "  X          X  ",
    " XX          XX ",
    " X            X ",
    " X            X ",
    " X            X ",
    " X           XX ",
    " XX     X    X  ",
    "  X     X   XX  ",
    "  XX    X  XX   ",
    "   XX   X       ",
    "    XX  X       ",
    "        XXXXXX  ",
    "                ",
), black='X', white='.', xor='o')
