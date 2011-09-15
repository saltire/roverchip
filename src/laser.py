import pygame

import laserbeam
import mob

class Laser(mob.Mob):

    def __init__(self, map, pos, dir):
        mob.Mob.__init__(self, map, pos, dir)
        self.colour = (192, 64, 0)
        
        self.is_solid = 1
        
        self.beam = pygame.sprite.RenderUpdates()

        
    def calculate_path(self):
        self.map.beams.empty()
        cell = self.pos
        out_dir = self.dir
        
        while 1:
            cell = self.map.get_neighbour(cell, out_dir)
            in_dir = out_dir
            out_dir = self.find_out_dir(cell, in_dir)
            if out_dir is False:
                break
                
            beam = laserbeam.Laserbeam(cell, (in_dir, out_dir))
            self.map.beams.add(beam)
        
        
    def find_out_dir(self, cell, in_dir):
        if not self.map.is_empty(cell):
            return False
        
        if self.map.is_mob_type_in(cell, 'Mirror'):
            mirror = self.map.get_mobs_in(cell, 'Mirror')[0]
            return mirror.get_out_dir(in_dir)
            
        for mob in self.map.get_mobs_touching(cell):
            if mob.is_solid and mob not in self.map.get_mobs_touching(self.map.get_neighbour(cell, in_dir)):
                return False
        
        return in_dir
