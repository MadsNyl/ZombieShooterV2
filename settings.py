import pygame as pg
vec = pg.math.Vector2


# settings
# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (128, 0, 0)
BLOODRED = (138, 3, 3)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 100, 0)
BLUE = (0, 0, 255)
BRIGHTBLUE = (0, 150, 255)
BABYBLUE = (137, 207, 240)

# screen
WIDTH = 1024
HEIGHT = 608
TILESIZE = 32
TITLE = 'ZombieShooter v.2'
FPS = 60

#pg.display.set_caption(TITLE)
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
dt = clock.tick(FPS) / 1000

# game settings
zombie_wave_length = 2
boss_wave_length = 1
particle_num = 50
wave_num = 1


# radar settings
RADAR_WIDTH = 150
RADAR_HEIGHT = 90
RADAR_COLOR = (0, 0, 0)
BLIP_RADIUS = 2

# player settings
PLAYERSPEED = 200
RUNSPEED = 350
HANDGUN_IMG = pg.image.load('img/player_handgun.png')
UZI_IMG = pg.image.load('img/player_uzi.png')
MGUN_IMG = pg.image.load('img/player_machinegun.png')
SHOTGUN_IMG = pg.image.load('img/player_shotgun.png')
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100

# weapon settings
BULLET_IMG = pg.image.load('img/bullet.png')
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 600,
                    'bullet_rate': 900,
                    'bullet_lifetime': 2000,
                    'dmg': 25,
                    'spread': 5,
                    'count': 1,
                    'kickback': 200,
                    'img': HANDGUN_IMG}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                    'bullet_rate': 1200,
                    'bullet_lifetime': 400,
                    'dmg': 10,
                    'spread': 20,
                    'count': 12,
                    'kickback': 400,
                    'img': SHOTGUN_IMG}
WEAPONS['uzi'] = {'bullet_speed': 800,
                    'bullet_rate': 200,
                    'bullet_lifetime': 500,
                    'dmg': 5,
                    'spread': 15,
                    'count': 1,
                    'kickback': 50,
                    'img': UZI_IMG}
WEAPONS['machine'] = {'bullet_speed': 1000,
                    'bullet_rate': 100,
                    'bullet_lifetime': 500,
                    'dmg': 10,
                    'spread': 12,
                    'count': 1,
                    'kickback': 150,
                    'img': MGUN_IMG}

BARREL_OFFSET = vec(20, 2)

# zombie settings
ZOMBIE_IMG = [pg.image.load('img/zombie1.png'), pg.image.load('img/zombie2.png'), pg.image.load('img/zombie3.png'), pg.image.load('img/zombie4.png')
            ,pg.image.load('img/zombie5.png'), pg.image.load('img/zombie6.png'), pg.image.load('img/zombie7.png'), pg.image.load('img/zombie8.png'),]
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 32, 32)
ZOMBIE_SPEED = [50, 75, 100, 150]
ZOMBIE_HEALTH = [25, 50, 100, 150, 200]
ZOMBIE_KNOCKBACK = 25
ZOMBIE_DMG = 20
AVOID_RADIUS = 250

# boss settings
BOSS_IMG = pg.image.load('img/boss.png')
BOSS_HIT_RECT = pg.Rect(0, 0, 74, 68)
BOSS_SPEED = 50
BOSS_HEALTH = 500
BOSS_KNOCKBACK = 60
BOSS_DMG = 50
