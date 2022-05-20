import pygame as pg
import game

pg.init()
pg.mixer.init()
game = game.Game()
game.start_screen()
running = True
while running:
    game.game_loop()
    running = game.end_screen()
pg.quit()
quit()
