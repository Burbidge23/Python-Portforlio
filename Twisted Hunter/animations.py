from settings import *
import pygame as pg


class Falling(pg.sprite.Sprite):
    def __init__(self, fall_anim, center, game):
        super(Falling, self).__init__()
        self.game = game
        self.frame = 0
        self.fall_anim = fall_anim
        self.image = self.game.dead_duckimg
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        self.fall_speed = 5
        self.first = True
        self.first_time = 200

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.first_time and self.first:
            self.last_update = now
            self.first = False
        if now - self.last_update > self.frame_rate and not self.first:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.fall_anim):
                self.frame = 0

            center = self.rect.center
            self.image = self.fall_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
        if not self.first:
            self.rect.centery += self.fall_speed

