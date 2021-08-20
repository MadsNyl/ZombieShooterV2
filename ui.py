import pygame as pg
from settings import *


def draw_player_bar(surf, x, y, pct, length, height, col_full, col_med, col_low):
    if pct < 0:
        pct = 0
    BAR_LENGTH = length
    BAR_HEIGHT = height
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = col_full
    elif pct > 0.3:
        col = col_med
    else:
        col = col_low
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, col, outline_rect, 2)

def draw_text(text, font_name, size, color, x, y, align='nw'):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "nw":
        text_rect.topleft = (x, y)
    if align == "ne":
        text_rect.topright = (x, y)
    if align == "sw":
        text_rect.bottomleft = (x, y)
    if align == "se":
        text_rect.bottomright = (x, y)
    if align == "n":
        text_rect.midtop = (x, y)
    if align == "s":
        text_rect.midbottom = (x, y)
    if align == "e":
        text_rect.midright = (x, y)
    if align == "w":
        text_rect.midleft = (x, y)
    if align == "center":
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)
