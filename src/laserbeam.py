import pygame

import sprite

class Laserbeam(sprite.Sprite):
    
    def __init__(self, map, pos, dirs):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (192, 64, 0, 128)
        self.layer = 2

        self.dirs = dirs


    def check_collisions(self):
        for object in pygame.sprite.spritecollide(self, self.map.destructibles, 1):
            if object.get_type() == 'Laser':
                for beam in object.beams:
                    beam.kill()
        
