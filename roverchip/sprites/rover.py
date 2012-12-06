import pygame

import sprite


class Rover(sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.tile = 1, 2
        self.layer = 1
        self.is_solid = True
        self.is_destructible = True

