import pygame

from sprite import Sprite


class Laser(Sprite):
    def __init__(self, level, pos, facing):
        Sprite.__init__(self, level, pos, facing)
        
        level.destructibles.add(self)
        level.solids.add(self)
        
        self.tile = 4, 1
        self.layer = 3
        self.rotate = True
        
        self.beams = pygame.sprite.Group()

        
    def end_turn(self):
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
        
        
    def find_out_dir(self, pos, in_dir):
        """When a laser beam enters a cell, find out which in direction it exits."""
        if not self.level.object_can_enter(pos):
            return None
        
        mirror = self.level.get_sprites_in(pos, True, 'Mirror')
        if mirror:
            return mirror[0].get_out_dir(in_dir)
        
        # stop beam if a solid object is in the cell, but not in the next one
        # if it's in the next cell, the beam will stop there
        for sprite in self.level.get_solid_sprites_in(pos, False):
            if (sprite not in self.level.get_solid_sprites_in(self.level.get_neighbour(pos, in_dir), True)
                and not self.level.destructibles.has(sprite)):
                return None
        
        return in_dir
    
        
        
class Laserbeam(Sprite):    
    def __init__(self, level, pos, dirs):
        Sprite.__init__(self, level, pos)
        
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
        
