import pygame

import laserbeam
import sprite

class Laser(sprite.Sprite):

    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = (192, 64, 0)
        self.layer = 3
        self.is_solid = 1
        self.is_destructible = 1
        
        self.beams = pygame.sprite.Group()

        
    def start_turn(self):
        for beam in self.beams:
            beam.kill()
        cell = self.pos
        out_dir = self.facing
        
        while 1:
            cell = self.level.get_neighbour(cell, out_dir)
            in_dir = out_dir
            out_dir = self.find_out_dir(cell, in_dir)
            if out_dir is False:
                break
                
            beam = laserbeam.Laserbeam(self.level, cell, (in_dir, out_dir))
            self.beams.add(beam)
            
        self.level.sprites.add(self.beams, layer=3)
        self.level.beams.add(self.beams)
        
        
    def find_out_dir(self, cell, in_dir):
        if not self.level.object_can_enter(cell):
            return False
        
        mirrors = self.level.get_sprites_in(cell, 0, 'Mirror')
        if mirrors:
            return mirrors[0].get_out_dir(in_dir)
        
        for sprite in self.level.get_solid_sprites_in(cell, 1):
            if not sprite.is_destructible and sprite not in self.level.get_solid_sprites_in(self.level.get_neighbour(cell, in_dir), 1):
                return False
        
        return in_dir
    
        
        
