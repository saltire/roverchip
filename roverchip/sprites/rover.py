import pygame

import sprite


class Rover(sprite.Sprite):
    def __init__(self, level, pos, facing=0):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 255, 255, 0
        self.layer = 1
        self.is_destructible = True


    def check_collisions(self):
        if self.pos in (pos for shooter in self.level.get_sprites('Shooter') for pos in shooter.path):
            self.kill()

        if pygame.sprite.spritecollideany(self, self.level.enemies):
            self.kill()
