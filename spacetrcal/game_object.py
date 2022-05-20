import pygame as pg
from settings import *


class Game_object():
    obj_count = 0

    def __init__(self, x, y, w, h):
        self.background_img = pg.image.load("assets/imgs/bgimgs/desert.png").convert()
        self.img = pg.transform.scale(self.background_img, (WIDTH, HEIGHT))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.obj_count += 1

    def update(self):
        pass