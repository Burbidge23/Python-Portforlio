from game_object import *
from settings import *

class Player(Game_object):

    def __init__(self, x, y, w, h, path, speed):
        super(Player, self).__init__(x, y, w, h, path)
        self.speed = speed
        self.lives = player_lives
        self.score = 0
        self.dir = 0

    def move(self):
        if (self.y <= 0 and self.dir < 0) or (self.y >= HEIGHT - self.h and self.dir > 0):
            return
        self.y += (self.dir*self.speed)

    def die(self):
        self.lives -= 1
        self.reset()

    def move_up(self):
        self.dir = -1

    def move_down(self):
        self.dir = 1

    def move_stop(self):
        self.dir = 0

    def reset(self):
        self.x = player_start_x
        self.y = player_start_y

    def score_up(self, amount):
        self.score += amount
        if self.score % 7 == 0:
            self.lives += 1

    def replay(self):
        self.move_stop()
        self.reset()
        self.lives = 3
        self.score = 0
