import pygame

import sprite

class Shooter(sprite.Sprite):
    
    def __init__(self, map, pos, dir):
        sprite.Sprite.__init__(self, map, pos, dir)
        self.colour = (255, 128, 0)
        
        self.is_solid = 1
        self.is_enemy = 1
        
    
    def start_turn(self):
        self.path = []
        cell = self.pos
        while 1:
            cell = self.map.get_neighbour(cell, self.dir)
            if not cell or not self.map.is_open(cell) or self.map.get_solid_objects_in(cell):
                break
            self.path.append(cell)

        
    def check_collisions(self):
        if pygame.sprite.spritecollideany(self, self.map.beams):
            self.kill()
