import pygame as pg
import sys
from os import path
import random
import math
import time
from settings import *
from tilemap import *
from ui import *
from functions import *
vec = pg.math.Vector2

# init pygame
pg.init()




# classes

# player class
class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.weapon = 'pistol'
        self.image = WEAPONS[self.weapon]['img'].convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.stamina = PLAYER_STAMINA
        self.running = False
        self.exp = 0
        self.lvl = 0
        self.lvl_cap = 1000

    def update(self):
        self.rotate()
        self.get_keys()
        if self.running:
            self.stamina -= 0.5
            if self.stamina <= 0:
                self.running = False
                self.stamina = 0
        else:
            self.stamina += 0.2
            if self.stamina >= 100:
                self.stamina = 100

        self.pos += self.vel * dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, obstacles, 'y')
        self.rect.center = self.hit_rect.center
        self.outer_map_collision()
        self.exp_gain()

    def exp_gain(self):
        if self.exp >= self.lvl_cap:
            self.lvl += 1
            self.lvl_cap += 100
            self.max_health += 5
            self.health = self.max_health
            self.exp = 0


    def rotate(self):
        screen_pos = self.pos + camera.camera.topleft
        _, self.angle = (pg.mouse.get_pos() - screen_pos).as_polar()
        self.orig_img = WEAPONS[self.weapon]['img'].convert_alpha()
        self.image = pg.transform.rotozoom(self.orig_img, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def outer_map_collision(self):
        self.rect.center = self.pos
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= map.width:
            self.rect.right = map.width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= map.height:
            self.rect.bottom = map.height

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYERSPEED
            self.running = False
            if keys[pg.K_e]:
                if self.stamina > 0:
                    self.running = True
                    self.vel.x = -RUNSPEED
                else:
                    self.running = False
                    self.vel.x = -PLAYERSPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYERSPEED
            self.running = False
            if keys[pg.K_e]:
                if self.stamina > 0:
                    self.running = True
                    self.vel.x = RUNSPEED
                else:
                    self.running = False
                    self.vel.x = PLAYERSPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYERSPEED
            self.running = False
            if keys[pg.K_e]:
                if self.stamina > 0:
                    self.running = True
                    self.vel.y = -RUNSPEED
                else:
                    self.running = False
                    self.vel.y = -PLAYERSPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYERSPEED
            self.running = False
            if keys[pg.K_e]:
                if self.stamina > 0:
                    self.running = True
                    self.vel.y = RUNSPEED
                else:
                    self.running = False
                    self.vel.y = PLAYERSPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > WEAPONS[self.weapon]['bullet_rate']:
                self.last_shot = now
                self.shoot()

        if keys[pg.K_1]:
            self.weapon = 'pistol'
        elif keys[pg.K_2]:
            if self.lvl >= 5:
                self.weapon = 'uzi'
        elif keys[pg.K_3]:
            if self.lvl >= 10:
                self.weapon = 'shotgun'
        elif keys[pg.K_4]:
            if self.lvl >= 15:
                self.weapon = 'machine'

    def shoot(self):
        dir = vec(1, 0).rotate(self.angle)
        pos = self.pos + BARREL_OFFSET.rotate(self.angle)
        self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(self.angle)
        for i in range(WEAPONS[self.weapon]['count']):
            spread = random.uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
            bullet = Bullet(pos, dir.rotate(spread))
            all_sprites.add(bullet)
            bullets.add(bullet)


# bullet class
class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, dir):
        pg.sprite.Sprite.__init__(self)
        self.image = BULLET_IMG.convert_alpha()
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = random.uniform(-BULLET_SPREAD, BULLET_SPREAD)
        self.vel = dir * WEAPONS[player.weapon]['bullet_speed'] * random.uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, obstacles):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[player.weapon]['bullet_lifetime']:
            self.kill()



# mobs
class Zombie(pg.sprite.Sprite):
    def __init__(self, x, y, health, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = random.choice(ZOMBIE_IMG).convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=(x,y))
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.max_health = health
        self.health = self.max_health
        self.speed = speed

    def update(self):
        self.rotate()
        self.acc = vec(1, 0).rotate(self.angle)
        self.avoid_mobs()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * dt
        self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, obstacles, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = DARKGREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = DARKRED
        width = int(self.rect.width * self.health / self.max_health)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < self.max_health:
            pg.draw.rect(self.image, col, self.health_bar)

    def rotate(self):
        _, self.angle = (player.pos - self.pos).as_polar()
        self.image = pg.transform.rotozoom(self.orig_img, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def avoid_mobs(self):
        for zombie in zombies:
            if zombie != self:
                dist = self.pos - zombie.pos
                if 0 < dist.length_squared() < AVOID_RADIUS:
                    self.acc += dist.normalize()

class Boss(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = BOSS_IMG.convert_alpha()
        self.orig_img = self.image
        self.rect = self.image.get_rect(center=(x,y))
        self.hit_rect = BOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.health = BOSS_HEALTH
        self.speed = BOSS_SPEED

    def update(self):
        self.rotate()
        self.acc = vec(1, 0).rotate(self.angle)
        self.avoid_self()
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * dt
        self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, obstacles, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, obstacles, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 60:
            col = DARKGREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = DARKRED
        width = int(self.rect.width * self.health / BOSS_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < BOSS_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def rotate(self):
        _, self.angle = (player.pos - self.pos).as_polar()
        self.image = pg.transform.rotozoom(self.orig_img, -self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def avoid_self(self):
        for boss in boss_sprites:
            if boss != self:
                dist = self.pos - boss.pos
                if 0 < dist.length_squared() < AVOID_RADIUS:
                    self.acc += dist.normalize()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        self.groups = obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Particle(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        self.orig_img = self.image
        pg.draw.circle(self.image, BLOODRED, (5, 5,), 2)
        self.rect = self.image.get_rect(center=pos)
        self.vel = vec(20, 0).rotate(random.randrange(360))
        self.pos = vec(pos)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > 500:
            _, self.angle = (player.pos - self.pos).as_polar()
            self.acc = vec(400, 0).rotate(self.angle)
            self.acc += self.vel * -1
            self.vel += self.acc * dt
            self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
            self.rect.center = self.pos




# load data
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
map_folder = path.join(game_folder, 'maps')
map = TiledMap(path.join(map_folder, 'map.tmx'))
map_img = map.make_map()
map_rect = map_img.get_rect()
zombie_font = path.join(img_folder, 'ZOMBIE.TTF')
dim_screen = pg.Surface(screen.get_size()).convert_alpha()
dim_screen.fill((0, 0, 0, 100))

for tile_object in map.tmxdata.objects:
    if tile_object.name == 'Obj':
        Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)



def draw_mob_rader(surf, x, y):
    radar_screen = pg.Surface((RADAR_WIDTH, RADAR_HEIGHT))
    radar_rect = radar_screen.get_rect()
    radar_screen.fill(RADAR_COLOR)
    pg.draw.rect(radar_screen, WHITE, radar_rect, 1)
    blip_x = int(player.rect.centerx * RADAR_WIDTH / map.width)
    blip_y = int(player.rect.centery * RADAR_HEIGHT / map.height)
    pg.draw.circle(radar_screen, GREEN, (blip_x, blip_y), BLIP_RADIUS)
    for zombie in zombies:
        blip_x = int(zombie.rect.centerx * RADAR_WIDTH / map.width)
        blip_y = int(zombie.rect.centery * RADAR_HEIGHT / map.height)
        pg.draw.circle(radar_screen, RED, (blip_x, blip_y), BLIP_RADIUS)
    for boss in boss_sprites:
        blip_x = int(boss.rect.centerx * RADAR_WIDTH / map.width)
        blip_y = int(boss.rect.centery * RADAR_HEIGHT / map.height)
        pg.draw.circle(radar_screen, YELLOW, (blip_x, blip_y), BLIP_RADIUS)
    surf.blit(radar_screen, (x, y))


player = Player(map.width / 2, map.height / 2)
all_sprites.add(player)
camera = Camera(map.width, map.height)


mob_spawn(Zombie, zombie_wave_length, ZOMBIE_HEALTH[0], ZOMBIE_SPEED[0])
#boss = Boss(random.randint(45, 50), random.randint(45, 50))
#all_sprites.add(boss)
#boss_sprites.add(boss)

# game loop
run_game = True
while run_game:
    clock.tick(FPS)
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    #screen.fill(BLACK)
    screen.blit(map_img, camera.apply_rect(map_rect))
    screen.blit(dim_screen, (0, 0))
    #draw_screen_grid()
    draw_player_bar(screen, 30, HEIGHT - 85, player.health / player.max_health, 200, 20, DARKGREEN, YELLOW, RED)
    draw_player_bar(screen, 30, HEIGHT - 60, player.stamina / player.max_stamina, 200, 10, BLUE, BRIGHTBLUE, BABYBLUE)
    draw_player_bar(screen, 30, HEIGHT - 30, player.exp / player.lvl_cap, 200, 10, BLOODRED, DARKRED, RED)
    draw_mob_rader(screen, 0, 0)
    draw_text(f"{player.lvl}", zombie_font, 20, DARKRED, 240, HEIGHT - 32, align='nw')
    draw_text(f"Wave {wave_num}", zombie_font, 30, DARKRED, WIDTH - 100, 50, align='center')

    for sprite in all_sprites:
        if isinstance(sprite, Zombie):
            sprite.draw_health()
        if isinstance(sprite, Boss):
            sprite.draw_health()
        screen.blit(sprite.image, camera.apply(sprite))


    all_sprites.update()
    camera.update(player)

    if len(zombies) == 0 and len(boss_sprites) == 0:
        wave_num += 1
        zombie_wave_length += 2

        if wave_num <= 5:
            mob_spawn(Zombie, zombie_wave_length, ZOMBIE_HEALTH[0], ZOMBIE_SPEED[0])
        elif wave_num <= 10:
            mob_spawn(Zombie, zombie_wave_length, ZOMBIE_HEALTH[1], ZOMBIE_SPEED[1])
            particle_num = 60
        elif wave_num <= 20:
            mob_spawn(Zombie, zombie_wave_length, ZOMBIE_HEALTH[2], ZOMBIE_SPEED[2])
            dim_screen.fill((0, 0, 0, 140))
            particle_num = 75
        elif wave_num <= 30:
            dim_screen.fill((0, 0, 0, 200))
            boss_wave_length += 1
            mob_spawn(Zombie, zombie_wave_length, ZOMBIE_HEALTH[2], ZOMBIE_SPEED[2])
            if boss_wave_length >= 3:
                boss_wave_length = 3
            if len(boss_sprites) <= 3:
                for i in range(boss_wave_length):
                    boss = Boss(random.randint(45, 50), random.randint(45, 50))
                    all_sprites.add(boss)
                    boss_sprites.add(boss)



    # bullet collision
    hits = pg.sprite.groupcollide(zombies, bullets, False, True)
    for hit in hits:
        hit.health -= WEAPONS[player.weapon]['dmg'] * len(hits[hit])
        hit.vel = vec(0, 0)

    hits = pg.sprite.groupcollide(boss_sprites, bullets, False, True)
    for hit in hits:
        hit.health -= WEAPONS[player.weapon]['dmg'] * len(hits[hit])

    # particle collisioon
    hits = pg.sprite.spritecollide(player, particles, False)
    for hit in hits:
        hit.kill()
        player.exp += 1

    # mob collision
    hits = pg.sprite.spritecollide(player, zombies, False, collide_hit_rect)
    for hit in hits:
        player.health -= ZOMBIE_DMG
        hit.vel = vec(0, 0)
        if player.health <= 0:
            run_game = False
    if hits:
        player.pos += vec(ZOMBIE_KNOCKBACK, 0).rotate(-hits[0].rot)

    hits = pg.sprite.spritecollide(player, boss_sprites, False, collide_hit_rect)
    for hit in hits:
        player.health -= BOSS_DMG
        hit.vel = vec(0, 0)
        if player.health <= 0:
            run_game = False
    if hits:
        player.pos += vec(BOSS_KNOCKBACK, 0).rotate(-hits[0].rot)


    for zombie in zombies:
        if zombie.health <= 0:
            for i in range(particle_num):
                particle = Particle(zombie.pos)
                all_sprites.add(particle)
                particles.add(particle)

    for boss in  boss_sprites:
        if boss.health <= 0:
            for i in range(200):
                particle = Particle(boss.pos)
                all_sprites.add(particle)
                particles.add(particle)


    events()

    pg.display.flip()
