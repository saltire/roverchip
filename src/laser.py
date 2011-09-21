import pygame

import laserbeam
import sprite

class Laser(sprite.Sprite):

    def __init__(self, map, pos, dir):
        sprite.Sprite.__init__(self, map, pos, dir)
        self.colour = (192, 64, 0)
        self.is_solid = 1
        
        self.beam = pygame.sprite.RenderUpdates()

        
    def start_turn(self):
        self.map.sprites.remove(self.map.beams)
        self.map.beams.empty()
        cell = self.pos
        out_dir = self.dir
        
        while 1:
            cell = self.map.get_neighbour(cell, out_dir)
            in_dir = out_dir
            out_dir = self.find_out_dir(cell, in_dir)
            if out_dir is False:
                break
                
            beam = laserbeam.Laserbeam(self.map, cell, (in_dir, out_dir))
            self.map.sprites.add(beam, layer='lasers')
            self.map.beams.add(beam)
        
        
    def find_out_dir(self, cell, in_dir):
        if not self.map.can_object_enter(cell):
            return False
        
        mirrors = self.map.get_objects_in(cell, 0, 'Mirror')
        if mirrors:
            return mirrors[0].get_out_dir(in_dir)
        
        for sprite in self.map.get_solid_objects_in(cell, 1):
            if sprite not in self.map.enemies and sprite not in self.map.get_solid_objects_in(self.map.get_neighbour(cell, in_dir), 1):
                return False
        
        return in_dir
