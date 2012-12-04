import pygame

import sprite


class Rover(sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 255, 255, 0
        self.layer = 1
        self.is_destructible = True


    def check_collisions(self):
        """Kill Rover if he is touching any enemies."""
        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.kill()
