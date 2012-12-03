import pygame

import sprite

class Laserbeam(sprite.Sprite):
    
    def __init__(self, level, pos, dirs):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (192, 64, 0, 128)
        self.layer = 2

        self.dirs = dirs


    def check_collisions(self):
        for sprite in pygame.sprite.spritecollide(self, self.level.destructibles, 1):
            if sprite.get_type() == 'Laser':
                for beam in object.beams:
                    beam.kill()
        
