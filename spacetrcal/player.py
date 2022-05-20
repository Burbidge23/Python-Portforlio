import pygame as pg
from settings import *
import random


class Player(pg.sprite.Sprite):
    def __init__(self, sprite, bullet_img, game):
        super(Player, self).__init__()
        self.image = sprite
        self.image = pg.transform.scale(self.image, (80, 80))
        self.image = pg.transform.rotate(self.image, 270)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * 0.8) / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = 30
        self.rect.bottom = HEIGHT / 2 + 40
        self.speed_x = 0
        self.speed_y = 0
        self.moveSpeed = 8
        self.health = 100
        self.game = game
        self.bullet_img = bullet_img
        self.last_shot = pg.time.get_ticks()
        self.shoot_delay = 200
        self.right_shot = True
        self.ammo = 20
        self.alive = True

    def update(self):
        # Set speed back to 0
        self.speed_x = 0
        self.speed_y = 0
        # Get player movement and keys
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speed_x = -self.moveSpeed
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speed_x = self.moveSpeed
        if keystate[pg.K_UP] or keystate[pg.K_w]:
            self.speed_y = -self.moveSpeed
        if keystate[pg.K_DOWN] or keystate[pg.K_s]:
            self.speed_y = self.moveSpeed
        if keystate[pg.K_SPACE]:
            self.shoot()
        # Bind the player to the screen
        if self.rect.right > WIDTH / 2:
            self.rect.right = WIDTH / 2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        # Update the players movement and/or postion
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def shoot(self):
        if self.ammo > 0:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.ammo -= 1
                self.game.shootsnd.play()
                if self.right_shot:
                    bullet = Bullet(self.rect.centerx + 10, self.rect.centery + 5, self.bullet_img, self.game)
                    self.right_shot = False
                else:
                    bullet = Bullet(self.rect.centerx + 10, self.rect.centery + 15, self.bullet_img, self.game)
                    self.right_shot = True

    def hit(self):
        if self.health > 0:
            self.health -= 8
        if self.health <= 0:
            self.game.explosionsnd.play()
            self.alive = False
            self.kill()

    def regen(self):
        if self.health > 95:
            return
        else:
            self.health += 5
            self.ammo += 2


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, game, speed_y=0):
        super(Bullet, self).__init__()
        self.image = sprite
        self.image = pg.transform.rotate(self.image, 90)
        self.image = pg.transform.scale(self.image, (20, 10))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = speed_y
        self.speed_x = 12
        game.all_sprites.add(self)
        game.player_bullet_group.add(self)

    def update(self):
        self.rect.centery += self.speed_y
        self.rect.centerx += self.speed_x
        if self.rect.right > WIDTH:
            self.kill()
