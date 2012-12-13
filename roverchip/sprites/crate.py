from movable import Movable
from sprite import Sprite


class Crate(Movable):   
    def __init__(self, level, pos):
        Movable.__init__(self, level, pos)
        
        self.tile = 2, 1
        
        
    def start_turn(self):
        # if it's entirely on a water cell, replace with a sunken crate
        if (len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
            
            sunken = SunkenCrate(self.level, self.pos)
            self.level.sprites.add(sunken)
            sunken.after_move()



class SunkenCrate(Sprite):
    def __init__(self, level, pos):
        Sprite.__init__(self, level, pos)
        self.tile = 3, 1
        self.speed = 250
        
        
    def after_move(self):
        flow_dir = self.level.get_cell(self.pos).flow_dir
        if (flow_dir is not None
            and not self.level.get_sprites_in(self.level.get_neighbour(self.pos, flow_dir), False, 'SunkenCrate')):
            self.move_dir = flow_dir
            self.to_move = 1