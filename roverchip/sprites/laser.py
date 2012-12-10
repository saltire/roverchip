import pygame

import sprite


class Laser(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 4, 1
        self.layer = 3
        self.rotate = True
        self.is_solid = True
        self.is_destructible = True
        
        self.beams = pygame.sprite.Group()

        
    def start_turn(self):
        """Render the laser beams every turn."""
        for beam in self.beams:
            beam.kill()
        cell = self.pos
        out_dir = self.facing
        
        while True:
            cell = self.level.get_neighbour(cell, out_dir)
            in_dir = out_dir
            out_dir = self.find_out_dir(cell, in_dir)
            if out_dir is None:
                break
                
            beam = Laserbeam(self.level, cell, (in_dir, out_dir))
            self.beams.add(beam)
            
        self.level.sprites.add(self.beams, layer=3)
        self.level.beams.add(self.beams)
        
        
    def find_out_dir(self, cell, in_dir):
        """When a laser beam enters a cell, find out which in direction it exits."""
        if not self.level.object_can_enter(cell):
            return None
        
        mirror = self.level.get_sprites_in(cell, True, 'Mirror')
        if mirror:
            return mirror[0].get_out_dir(in_dir)
        
        for sprite in self.level.get_solid_sprites_in(cell, False):
            if not sprite.is_destructible and sprite not in self.level.get_solid_sprites_in(self.level.get_neighbour(cell, in_dir), 1):
                return None
        
        return in_dir
    
        
        
class Laserbeam(sprite.Sprite):    
    def __init__(self, level, pos, dirs):
        sprite.Sprite.__init__(self, level, pos)
        
        self.layer = 2
        self.rotate = True

        in_dir, out_dir = dirs
        beamtype = (in_dir - out_dir) % 4
        # beam goes straight
        if beamtype == 0:
            self.tile = 5, 1
            self.facing = out_dir
        # beam turns right
        elif beamtype == 3:
            self.tile = 6, 1
            self.facing = out_dir
        # beam turns left
        elif beamtype == 1:
            self.tile = 6, 1
            self.facing = (out_dir - 1) % 4


    def check_collisions(self):
        """Kill all destructible items touching the laserbeam (this is done
        automatically by the spritecollide method). Also remove laserbeams
        emitting from any lasers that are destroyed."""
        for sprite in pygame.sprite.spritecollide(self, self.level.destructibles, True):
            if sprite.get_type() == 'Laser':
                for beam in sprite.beams:
                    beam.kill()
        
