import pygame as pg
from settings import *

class Enemy_bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, image):
        super(Enemy_bullet, self).__init__()
        self.game = game
        self.bullet_speed = 600
        self.game.all_sprites.add(self)
        self.game.enemy_bullet_group.add(self)
        self.image = image
        self.image = pg.transform.scale(self.image, (10, 20))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * self.bullet_speed
        self.life_time = 2500
        self.spawn_time = pg.time.get_ticks()


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        if pg.time.get_ticks() - self.spawn_time > self.life_time:
            self.kill()
