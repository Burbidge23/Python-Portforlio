import pygame as pg
from settings import *
import random
import math


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, sprite):
        super(Enemy, self).__init__()
        self.game = game
        self.frame = 0
        self.fly_anim = self.game.enemy_anim
        self.image = self.fly_anim[self.frame]
        # self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.top = HEIGHT - 200
        self.rect.centerx = random.randint(20, WIDTH - 20)
        self.game.allsprites.add(self)
        self.game.enemysprites.add(self)
        self.duck_speed = random.randint(4, 7)
        self.duck_speedo = self.duck_speed
        self.hit_peak = False
        self.xspeed = random.randint(-3, 3)
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100



    def update(self):
        self.rect.centerx += self.xspeed
        if self.hit_peak:
            self.rect.top -= self.duck_speedo * 2
        else:
            self.rect.top -= self.duck_speed
            if self.rect.left < 10 or self.rect.right > WIDTH:
                self.xspeed = self.xspeed * -1
            if self.rect.top < 0:
                self.duck_speed = self.duck_speed * -1
            if self.rect.bottom > HEIGHT-250:
                self.duck_speed = self.duck_speedo
        if self.rect.bottom < 0:
            self.kill()

        self.anim()

    def missed(self):
        self.hit_peak = True
        self.game.ammo = 3
        if len(self.game.enemysprites) <= 1:
            self.game.enemy = Enemy(self.game, self.game.enemy_img)

    def anim(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.fly_anim):
                self.frame = 0

            center = self.rect.center
            if self.xspeed < 0:
                self.image = pg.transform.flip(self.fly_anim[self.frame], True, False)
            else:
                self.image = self.fly_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
#workspace
#
# class Raccoon(pg.sprite.Sprite):
#     def __init__(self, game):
#         super(Raccoon, self).__init__()
#         self.frame = 0
#         self.game = game
#         self.walk_anim = self.game.walk_anim
#         self.jump_anim = self.game.jump_anim
#         self.image = self.game.raccoonwalk_anim[self.frame]
#         self.image = pg.transform.scale(self.image, (100, 100))
#         self.rect = self.image.get_rect()
#         self.rect.centerx = 700
#         self.rect.centery = HEIGHT * 13/16
#         self.raccoonSpeed = 4
#         self.game.allsprites.add(self)
#         self.game.racconsprite.add(self)
#         self.last_update = pg.time.get_ticks()
#         self.frame_rate = 100

#workspace

class Dogintro(pg.sprite.Sprite):
    def __init__(self, game):
        super(Dogintro, self).__init__()
        self.frame = 0
        self.game = game
        self.walk_anim = self.game.walk_anim
        self.jump_anim = self.game.jump_anim
        self.image = self.game.walk_anim[self.frame]
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = -20
        self.rect.centery = HEIGHT * 13/16
        self.dogSpeed = 4
        self.game.allsprites.add(self)
        self.game.dogsprite.add(self)
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        self.jump_rate = 200

    def update(self):
        if not self.rect.right > ((WIDTH / 2) -150):
            self.rect.centerx += self.dogSpeed
            self.animwalk()
        else:
            self.animjump()
            self.rect.centery -= 10


    def animwalk(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.walk_anim):
                self.frame = 0

            center = self.rect.center
            self.image = self.walk_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def animjump(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if self.frame == len(self.jump_anim) - 1:
                self.kill()
            center = self.rect.center
            self.image = self.jump_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame += 1

    def animfall(self):
        center = self.rect.center
        self.image = self.jump_anim[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame += 1


class MouseSprite(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        super(MouseSprite, self).__init__()
        self.game = game
        self.image = self.game.crosshair_img
        self.image = pg.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.game.allsprites.add(self)
        self.game.mousesprites.add(self)

    def update(self):
        x, y = pg.mouse.get_pos()
        self.rect.center = x, y

class EndDog(pg.sprite.Sprite):
    def __init__(self, game, mean=False):
        super(EndDog, self).__init__()
        self.frame = 0
        self.game = game
        self.mean = mean
        self.frame = 0
        self.lose_anim = self.game.dog_lose_anim
        if self.mean:
            self.image = self.lose_anim[self.frame]
        else:
            self.image = self.game.dog_win_img
        self.image = pg.transform.scale(self.image, (150, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 - 100
        self.rect.centery = HEIGHT * 3/4 + 50
        self.game.allsprites.add(self)
        self.game.dogwinsprite.add(self)
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 100
        self.dogspeed = 4
        self.dogpeak = HEIGHT * 3/4


    def update(self):
        if self.rect.bottom > self.dogpeak:
            self.rect.centery -= self.dogspeed
        if self.mean:
            self.anim()


    def anim(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.lose_anim):
                self.frame = 0

            center = self.rect.center
            self.image = self.lose_anim[self.frame]
            self.image = pg.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect.center = center

class DeadDog(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        super(DeadDog, self).__init__()
        self.game = game
        self.image = self.game.dead_dog
        self.image = pg.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 10
        self.rect.centery = y - 10
        self.game.allsprites.add(self)
        self.game.dogwinsprite.add(self)
        self.last_update = pg.time.get_ticks()
        self.dogspeed = 4
        self.dog_transform = 5
        self.dog_transformc = 150

    def update(self):
        self.rect.centery += self.dogspeed
        self.dog_transformc -= self.dog_transform
        if self.dog_transformc > 20:
            self.image = pg.transform.scale(self.image, (200, self.dog_transformc))



