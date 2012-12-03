import sunkencrate
import sprite

class Crate(sprite.Sprite):
    
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (128, 128, 128)
        self.is_movable = 1
        self.is_solid = 1
        
        
    def after_move(self):
        if self.level.get_cell(self.pos).get_type() == 'Fire':
            self.to_move = 1
        
        elif (self.level.get_cell(self.pos).get_type() == 'Water'
              and not self.level.get_sprites_in(self.pos, 0, 'SunkenCrate')):
            self.kill()
            
            sunken = sunkencrate.SunkenCrate(self.level, self.pos)
            self.level.sprites.add(sunken)
            sunken.after_move()
