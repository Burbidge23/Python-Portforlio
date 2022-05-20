import random
from settings import *
import pygame as pg

class Pow(pg.sprite.Sprite):
    def __init__(self, center, pow_img):
        super(Pow, self).__init__()
        self.type = random.choice(["shield","gun"])
        self.pow_img = pow_img
        self.image = pow_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.y > HEIGHT:
            self.kill()