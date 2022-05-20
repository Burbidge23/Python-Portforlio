import os
import pygame as pg

# Settings
WIDTH = 1000
HEIGHT = 800
FPS = 40
TITLE = 'Twisted Hunter'
font_name = pg.font.match_font('Comic Sans MS')


RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
CF_BLUE = (100,149,237)

# files

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, 'assets')
img_folder = os.path.join(assets_folder, 'imgs')
audio_folder = os.path.join(assets_folder, 'audio')
ambient_folder = os.path.join(audio_folder, 'ambient')
fx_folder = os.path.join(audio_folder, 'fx')
music_folder = os.path.join(audio_folder, 'music')
sprite_folder = os.path.join(img_folder, 'sprites')
enemy_folder = os.path.join(sprite_folder, 'enemy')
objects_folder = os.path.join(sprite_folder, 'objects')
player_folder = os.path.join(sprite_folder, 'player')
background_folder = os.path.join(img_folder, 'bgimgs')
