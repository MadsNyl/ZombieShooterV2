import pygame as pg
import sys
from os import path
import random
import math
import time
from settings import *
vec = pg.math.Vector2


# sprite groups
all_sprites = pg.sprite.Group()
bullets = pg.sprite.Group()
zombies = pg.sprite.Group()
boss_sprites = pg.sprite.Group()
obstacles = pg.sprite.Group()
particles = pg.sprite.Group()


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def mob_spawn(Mob, wave_length, health, speed):
    for i in range(wave_length):
        loc = random.choice(['top', 'right', 'bottom', 'left'])
        if loc == 'top':
            mob = Mob(random.randint(0, 100), random.randint(-2, -1), health, speed)
            all_sprites.add(mob)
            zombies.add(mob)
        if loc == 'right':
            mob = Mob(random.randint(101, 105), random.randint(0, 100), health, speed)
            all_sprites.add(mob)
            zombies.add(mob)
        if loc == 'bottom':
            mob = Mob(random.randint(0, 100), random.randint(101, 105), health, speed)
            all_sprites.add(mob)
            zombies.add(mob)
        if loc == 'left':
            mob = Mob(random.randint(-2, -1), random.randint(0, 100), health, speed)
            all_sprites.add(mob)
            zombies.add(mob)




def events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()
            if event.key == pg.K_p:
                paused = not paused


def draw_screen_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGREY, (0, y), (WIDTH, y))

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)
