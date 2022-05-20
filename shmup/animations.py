from settings import *
import pygame as pg

class Explosion(pg.sprite.Sprite):
    def __init__(self, size, exp_anim, center):
        super(Explosion, self).__init__()
        self.size = size
        self.frame = 0
        self.exp_anim = exp_anim
        self.image = self.exp_anim[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 40

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.exp_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.exp_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
