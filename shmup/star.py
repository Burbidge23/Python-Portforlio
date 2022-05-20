from settings import *
import random
import pygame as pg


class Star(pg.sprite.Sprite):
    def __init__(self, sprite):
        super(Star, self).__init__()
        self.image_orig = sprite
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.image = pg.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * 0.8) / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randint(20, WIDTH-20)
        self.rect.bottom = random.randint(-25, HEIGHT)
        self.speed_y = 10


    def update(self):
        self.rect.centery += self.speed_y

        # Wrap the enemy back up to the top after it goes off the bottom
        if self.rect.top > HEIGHT + random.randint(3, 20):
            self.rect.bottom = random.randint(0, 25)
            self.rect.centerx = random.randint(20, WIDTH - 20)