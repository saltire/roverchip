import pygame

import sprite


class Laser(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        self.colour = 192, 64, 0
        self.layer = 3
        self.is_solid = True
        self.is_destructible = True
        
        self.beams = pygame.sprite.Group()

        
    def start_turn(self):
        for beam in self.beams:
            beam.kill()
        cell = self.pos
        out_dir = self.facing
        
        while True:
            cell = self.level.get_neighbour(cell, out_dir)
            in_dir = out_dir
            out_dir = self.find_out_dir(cell, in_dir)
            if out_dir is False:
                break
                
            beam = Laserbeam(self.level, cell, (in_dir, out_dir))
            self.beams.add(beam)
            
        self.level.sprites.add(self.beams, layer=3)
        self.level.beams.add(self.beams)
        
        
    def find_out_dir(self, cell, in_dir):
        if not self.level.object_can_enter(cell):
            return False
        
        try:
            mirror = next(self.level.get_sprites_in(cell, False, 'Mirror'))
            return mirror.get_out_dir(in_dir)
        except StopIteration:
            pass
        
        for sprite in self.level.get_solid_sprites_in(cell, True):
            if not sprite.is_destructible and sprite not in self.level.get_solid_sprites_in(self.level.get_neighbour(cell, in_dir), 1):
                return False
        
        return in_dir
    
        
        
class Laserbeam(sprite.Sprite):    
    def __init__(self, level, pos, dirs):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = 192, 64, 0, 128
        self.layer = 2

        self.dirs = dirs


    def check_collisions(self):
        for sprite in pygame.sprite.spritecollide(self, self.level.destructibles, 1):
            if sprite.get_type() == 'Laser':
                for beam in sprite.beams:
                    beam.kill()
        
