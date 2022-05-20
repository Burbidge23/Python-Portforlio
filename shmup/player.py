import pygame as pg
from settings import *
import random


class Player(pg.sprite.Sprite):
    def __init__(self, sprite, bullet_sprite, all_sprites, bullet_group, shootsnd):
        super(Player, self).__init__()
        self.image = sprite
        self.image = pg.transform.scale(self.image, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width * 0.8) / 2
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - self.rect.height
        self.speed_x = 0
        self.speed_y = 0
        self.moveSpeed = 8
        self.shield = 100
        self.fuel = 100
        self.shoot_delay = 250
        self.shootsnd = shootsnd
        self.last_shot = pg.time.get_ticks()
        self.all_sprites = all_sprites
        self.bullet_group = bullet_group
        self.bullet_img = bullet_sprite
        self.lives = 3
        self.hidden = False
        self.gun_power = 6

    def update(self):
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - self.rect.height
        # Set speed back to 0
        self.speed_x = 0
        # Get player movement and keys
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT] or keystate[pg.K_a]:
            self.speed_x = -self.moveSpeed
        if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
            self.speed_x = self.moveSpeed
        if keystate[pg.K_SPACE]:
            self.shoot(self.bullet_img, self.all_sprites, self.bullet_group)
        # Bind the player to the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Update the players movement and/or postion
        self.rect.x += self.speed_x

    def takeDamage(self, hit):
        self.shield -= hit.radius
        self.gun_down()

    def die(self):
        self.lives -= 1
        self.hide()
        self.shield = 100
        self.gun_down()

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (self.rect.centerx, HEIGHT + 500)

    def addShield(self, amount):
        self.shield += amount
        if self.shield > 100:
            self.shield = 100

    def gun_up(self):
        self.gun_power += 1
        if self.gun_power < 0:
            self.gun_power = 0
        if self.gun_power > 7:
            self.gun_power = 7

    def gun_down(self):
        self.gun_power = 0
        self.shoot_delay = 250

    def shoot(self, sprite, all_sprites, bullet_group):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shootsnd.play()
            if self.gun_power == 0:
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
            elif self.gun_power == 1:
                self.shoot_delay = 175
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
            elif self.gun_power == 2:
                self.shoot_delay = 250
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group)
            elif self.gun_power == 3:
                self.shoot_delay = 250
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
            elif self.gun_power == 4:
                self.shoot_delay = 275
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -3)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 3)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
            elif self.gun_power == 5:
                self.shoot_delay = 100
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -3)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 3)
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -1)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 1)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, 2)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, -2)
            elif self.gun_power == 6:
                self.shoot_delay = 0
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -3)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 3)
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -1)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 1)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, 2)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, -2)
            elif self.gun_power == 7:
                self.shoot_delay = 0
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -3)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 3)
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -1)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 1)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, 2)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, -2)
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -4)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 4)
                bullet = Bullet(self.rect.left + 5, self.rect.top + 2, sprite, all_sprites, bullet_group, -2)
                bullet = Bullet(self.rect.right - 5, self.rect.top + 2, sprite, all_sprites, bullet_group, 2)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, 4)
                bullet = Bullet(self.rect.centerx, self.rect.top - 3, sprite, all_sprites, bullet_group, -4)


    # def move(self):
    #     # if self.rect.left > WIDTH:
    #     #     self.rect.right = 0
    #     # if self.rect.right < 0:
    #     #     self.rect.left = WIDTH
    #     # if self.rect.top > HEIGHT:
    #     #     self.rect.bottom = 0
    #     # if self.rect.bottom < 0:
    #     #     self.rect.top = 400
    #     # self.rect.y += 5
    #     # self.rect.x += 5
    #
    #     self.rect.x += self.dir_x
    #     self.rect.y += self.dir_y
    #     if self.rect.left > WIDTH:
    #         self.rect.right = 0
    #     if self.rect.right < 0:
    #         self.rect.left = WIDTH
    #     if self.rect.top > HEIGHT:
    #         self.rect.bottom = 0
    #     if self.rect.bottom < 0:
    #         self.rect.top = HEIGHT
    #
    # def testMove(self):
    #     # if self.direction == 'right':
    #     #     self.rect.x += 5
    #     # if self.rect.left > WIDTH:
    #     #     self.rect.centerx = 200
    #     #     self.rect.centery = 400
    #     #     self.direction = 'up'
    #     # if self.direction == 'up':
    #     #     self.rect.y -= 5
    #     # if self.rect.bottom < 0:
    #     #     self.rect.centerx = 0
    #     #     self.rect.centery = 200
    #     #     self.direction = 'right'
    #     # if self.direction == 'left':
    #     #     self.rect.x -= 5
    #     # if self.rect.right < 0:
    #     #     self.rect.centerx = 200
    #     #     self.rect.centery = 0
    #     #     self.direction = 'down'
    #     # if self.direction == 'down':
    #     #     self.rect.y += 5
    #     # if self.rect.top > HEIGHT:
    #     #     self.rect.centerx = 400
    #     #     self.rect.centery = 200
    #     #     self.direction = 'left'
    #
    #     self.rect.x += self.dir_x
    #     self.rect.y += self.dir_y
    #     if self.rect.left > WIDTH:
    #         self.dir_y = -5
    #         self.dir_x = 0
    #         self.rect.top = HEIGHT
    #         self.rect.centerx = WIDTH / 2
    #     if self.rect.bottom < 0:
    #         self.dir_y = 0
    #         self.dir_x = 5
    #         self.rect.right = 0
    #         self.rect.centery = HEIGHT / 2
    #     if self.rect.right < 0:
    #         self.dir_x = 0
    #         self.dir_y = 5
    #         self.rect.bottom = 0
    #         self.rect.centerx = WIDTH / 2
    #     if self.rect.top > HEIGHT:
    #         self.dir_y = 0
    #         self.dir_x = -5
    #         self.rect.left = WIDTH
    #         self.rect.centery = HEIGHT / 2
    #
    # def bouncemove(self):
    #     # if self.directionx == 'right':
    #     #     self.rect.x += 5
    #     # if self.directiony == 'up':
    #     #     self.rect.y -= 4
    #     # if self.directionx == 'left':
    #     #     self.rect.x -= 5
    #     # if self.directiony == 'down':
    #     #     self.rect.y += 4
    #     # if self.rect.left > WIDTH:
    #     #     self.directionx = 'left'
    #     # if self.rect.bottom < 0:
    #     #     self.directiony = 'down'
    #     # if self.rect.right < 0:
    #     #     self.directionx = 'right'
    #     # if self.rect.top > HEIGHT:
    #     #     self.directiony = 'up'
    #
    #     self.rect.x += self.dir_x
    #     self.rect.y += self.dir_y
    #     if self.rect.right >= WIDTH or self.rect.left <= 0:
    #         self.dir_x *= -1
    #     if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
    #         self.dir_y *= -1


#
# class PlayerControlled(pg.sprite.Sprite):
#     def __init__(self):
#         super(PlayerControlled, self).__init__()
#         self.image = pg.Surface((50, 50))
#         self.image.fill(RED)
#         self.rect = self.image.get_rect()
#         self.rect.centerx = WIDTH / 2
#         self.rect.bottom = HEIGHT - 10
#         self.moveSpeed = 5
#         self.speed_x = 0
#         self.speed_y = 0
#
#     def update(self):
#         self.speed_x = 0
#         self.speed_y = 0
#         keystate = pg.key.get_pressed()
#         if keystate[pg.K_a]:
#             self.updatespeed_x(-1)
#         if keystate[pg.K_d]:
#             self.updatespeed_x(1)
#         if keystate[pg.K_w]:
#             self.updatespeed_y(-1)
#         if keystate[pg.K_s]:
#             self.updatespeed_y(1)
#
#         self.rect.x += self.speed_x
#         self.rect.y += self.speed_y
#
#         self.bound()
#
#     def updatespeed_x(self, dir):
#         self.speed_x = self.moveSpeed * dir
#
#     def updatespeed_y(self, dir):
#         self.speed_y = self.moveSpeed * dir
#
#     def bound(self):
#         if self.rect.left > WIDTH:
#             self.rect.right = 0
#         if self.rect.right < 0:
#             self.rect.left = WIDTH
#         if self.rect.top > HEIGHT:
#             self.rect.bottom = 0
#         if self.rect.bottom < 0:
#             self.rect.top = HEIGHT
#
#
# class PlayerMouseControlled(pg.sprite.Sprite):
#     def __init__(self, sprite):
#         super(PlayerMouseControlled, self).__init__()
#         self.image = sprite
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.centerx = WIDTH / 2
#         self.rect.bottom = HEIGHT - 10
#         self.moveSpeed = 5
#         self.speed_x = 0
#         self.speed_y = 0
#
#     def update(self):
#         mousex, mousey = pg.mouse.get_pos()
#         self.rect.center = ((mousex, mousey))


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, sprite, all_sprites, bullet_group, speed_x=0):
        super(Bullet, self).__init__()
        self.image = sprite
        self.image = pg.transform.scale(self.image, (10, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -12
        self.speed_x = speed_x
        all_sprites.add(self)
        bullet_group.add(self)

    def update(self):
        self.rect.centery += self.speed_y
        self.rect.centerx += self.speed_x
        if self.rect.bottom < -5:
            self.kill()
