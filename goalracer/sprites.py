import pygame as pg
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2


def collision_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, rot, num, sprite):
        self.groups = game.all_sprites, game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.sprite = sprite
        self.image = sprite
        self.image.set_colorkey(WHITE)
        self.image = pg.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = rot
        self.last_shot = 0
        self.boost = 100
        self.playernum = num
        self.score = 0
        # self.max_vel = vec(1, 1)

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        #if self.vel.x > self.max_vel.x:
        #    self.vel.x = self.max_vel.x
        #if self.vel.y > self.max_vel.y:
        #    self.vel.y = self.max_vel.y
        keys = pg.key.get_pressed()
        if self.playernum == 1:
            if keys[pg.K_a]:
                self.rot_speed = PLAYER_ROT_SPEED
            if keys[pg.K_d]:
                self.rot_speed = -PLAYER_ROT_SPEED
            if keys[pg.K_w]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            if keys[pg.K_s]:
                self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
            if keys[pg.K_SPACE]:
                if self.boost >= 0:
                    self.vel = vec(BOOST_SPEED, 0).rotate(-self.rot)
                    self.boost -= 0.5
        else:
            if keys[pg.K_LEFT]:
                self.rot_speed = PLAYER_ROT_SPEED
            if keys[pg.K_RIGHT]:
                self.rot_speed = -PLAYER_ROT_SPEED
            if keys[pg.K_UP]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            if keys[pg.K_DOWN]:
                self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
            if keys[pg.K_RCTRL]:
                if self.boost >= 0:
                    self.vel = vec(BOOST_SPEED, 0).rotate(-self.rot)
                    self.boost -= 0.5



    # def get_keys(self):
    #     self.rot_speed = 0
    #     self.vel = vec(0, 0)
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_a] or keys[pg.K_LEFT]:
    #         self.vel.x = -PLAYER_SPEED
    #     if keys[pg.K_d] or keys[pg.K_RIGHT]:
    #         self.vel.x = PLAYER_SPEED
    #     if keys[pg.K_w] or keys[pg.K_UP]:
    #         self.vel.y = -PLAYER_SPEED
    #     if keys[pg.K_s] or keys[pg.K_DOWN]:
    #         self.vel.y = PLAYER_SPEED
    #     if self.vel.x != 0 and self.vel.y != 0:
    #         self.vel *= 0.7071



    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.sprite, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collision_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collision_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Goal(pg.sprite.Sprite):
    def __init__(self, game, x, y, side):
        self.groups = game.all_sprites, game.goals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.side = side


class Ball(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.balls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = BALL_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE


    def update(self):

        self.vel += self.acc
        self.friction()
        # # if abs(self.vel.x) < 0.1:
        # #     self.vel = vec(0, 0)
        self.pos += (self.vel + 0.5 * self.acc)/TILESIZE
        self.hit_rect.centerx = self.pos.x
        self.collision_walls_bounce(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        self.collision_walls_bounce(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


    def friction(self):
        self.acc.x = self.vel.x * BAll_FRICTION
        self.acc.y = self.vel.y * BAll_FRICTION

    def bump(self, hit):
        self.acc += hit.vel

    def collision_walls_bounce(self, sprite, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if sprite.vel.x > 0:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if sprite.vel.x < 0:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x *= -1
                sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            if hits:
                if sprite.vel.y > 0:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if sprite.vel.y < 0:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y *= -1
                sprite.hit_rect.centery = sprite.pos.y



