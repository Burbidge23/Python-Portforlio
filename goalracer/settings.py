import pygame as pg
vec = pg.math.Vector2

# Game Settings
WIDTH = 1056
HEIGHT = 480
FPS = 60
font_name = pg.font.match_font('Comic Sans MS')

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
CF_BLUE = (100,149,237)
BROWN = (106, 55, 5)

# Tile Settings
TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player Settings
PLAYER_SPEED = 300
BOOST_SPEED = 600
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'car.png'
P2IMG = 'car2.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BAll_FRICTION = -0.01

PLAYER1START = vec(7, 7)
PLAYER2START = vec(28, 7)

# Gun Settings
BULLET_IMG = 'bullet.png'
BALL_HIT_RECT = pg.Rect(0, 0, 18, 18)
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150

# Mob Settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)