# The title for the application of the game
import os.path

TITLE = "shmup"
# The window width and height
WIDTH = 600
HEIGHT = 900
# The tick speed for the game clock
FPS = 30
# the difficulty of the game
difficulty = "Easy"
# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
cfBlue = (100, 149, 237)

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, 'assets')
img_folder = os.path.join(assets_folder, 'imgs')
audio_folder = os.path.join(assets_folder, 'audio')
ambiant_folder = os.path.join(audio_folder, 'ambiant')
fx_folder = os.path.join(audio_folder, 'fx')
music_folder = os.path.join(audio_folder, 'music')
