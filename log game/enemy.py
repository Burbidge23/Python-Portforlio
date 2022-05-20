import pygame as pg
from settings import *
from player import *
import random

class Enemy(Player):

    # Override move from player
    def move(self):
        if self.dir == 0:
            self.dir = random.choice([1, -1])
        if (self.x >= WIDTH - self.w - 100) or (self.x <= 100 ):
            self.dir *= -1
        self.x += self.speed * self.dir
