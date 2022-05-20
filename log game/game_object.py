import pygame as pg


class Game_object():
    obj_count = 0

    def __init__(self, x, y, w, h, path):
        self.img = pg.image.load(path)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pg.transform.scale(self.img,(w,h))
        self.obj_count += 1

    def update(self):
        pass
