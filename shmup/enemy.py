import random
from settings import *
import pygame as pg


class Mob(pg.sprite.Sprite):
    def __init__(self, sprite):
        super(Mob, self).__init__()
        self.image_orig = sprite
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        # self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * 0.8) / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = random.randint(20, WIDTH-20)
        self.rect.bottom = random.randint(-25, 0)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(4, 12)
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_img = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_img
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        # moving enemy position down the screen
        self.rect.centerx += self.speed_x
        self.rect.centery += self.speed_y

        # Wrap the enemy back up to the top after it goes off the bottom
        if self.rect.top > HEIGHT + random.randint(3, 20):
            self.rect.bottom = random.randint(0, 25)
            self.rect.centerx = random.randint(20, WIDTH-20)
            self.speed_x = random.randint(-3, 3)
            self.speed_y = random.randint(4, 12)
        # Wraps left and right sides
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH



