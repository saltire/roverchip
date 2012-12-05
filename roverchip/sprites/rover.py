import pygame

import sprite


class Rover(sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 255, 255, 0
        self.layer = 1
        self.is_solid = True
        self.is_destructible = True

