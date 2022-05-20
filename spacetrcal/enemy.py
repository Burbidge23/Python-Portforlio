import random

import pygame as pg
from settings import *
import math
from bullet import *

vec = pg.math.Vector2


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, image):
        super(Enemy, self).__init__()
        self.game = game
        self.image = image
        self.image = pg.transform.scale(self.image, (80, 80))
        self.image = pg.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH + 50, random.randint(50, HEIGHT- 50))
        # self.rect.center = (random.randint(WIDTH/2 + 50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        self.game.all_sprites.add(self)
        self.game.enemy_sprites.add(self)
        self.fire_rate = random.randint(1500, 2200)
        self.last_shot = pg.time.get_ticks()
        self.speedx = random.randint(4, 8)
        self.speedy = random.randint(4, 8)
        self.offscreenx = random.randint(-10, -5)
        self.offscreeny = 0
        self.onscreen = False

    def shoot_at(self):
        self.game.shootsnd.play()
        target_x = self.game.player.rect.centerx
        target_y = self.game.player.rect.centery
        angle = math.atan2(target_y - self.rect.centery, target_x - self.rect.centerx)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
        dir = vec(self.dx, self.dy)
        b = Enemy_bullet(self.game, self.rect.center, dir, self.game.bullet_img)

    def fire(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            self.shoot_at()

    def bounds(self):
        if self.rect.right > WIDTH:
            self.speedx = self.speedx * -1
        if self.rect.bottom > HEIGHT:
            self.speedy = self.speedy * -1
        if self.rect.left < WIDTH/2:
            self.speedx = self.speedx * -1
        if self.rect.top < 0:
            self.speedy = self.speedy * -1

    def dir_change(self):
        num = random.randint(0, 100)
        if num == 100 and not (self.rect.right > WIDTH - 50 or self.rect.left < WIDTH/2 + 50):
            self.speedx = self.speedx * -1
        num = random.randint(0, 100)
        if num == 100 and not (self.rect.top < 50 or self.rect.bottom > HEIGHT - 50):
            self.speedy = self.speedy * -1

    def move(self):
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

    def move_off(self):
        self.rect.centerx += self.offscreenx
        self.rect.centery += self.offscreeny

    def screencheck(self):
        if self.rect.right < WIDTH - 50:
            self.onscreen = True

    def update(self):
        self.screencheck()
        self.bounds()
        if self.onscreen:
            self.fire()
            self.dir_change()
            self.move()
        else:
            self.move_off()