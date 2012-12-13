from sprite import Sprite


class Movable(Sprite):
    def __init__(self, level, pos, facing=0):
        Sprite.__init__(self, level, pos, facing)
        
        self.layer = 1
        self.is_movable = True
        self.is_solid = True
        
        self.is_sinkable = True
        self.moves_continuously = False
        
        
    def start_turn(self):
        # if it's entirely on a water cell, destroy it
        if (self.is_sinkable and len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
        
    
    def after_move(self):
        # trigger object enter hook
        self.level.get_cell(self.pos).object_inside()

        # continue movement
        nextcell = self.level.get_neighbour(self.pos, self.move_dir)
        if (self.level.object_can_enter(nextcell)
            and not self.level.get_solid_sprites_in(nextcell, False)
            and (self.moves_continuously
                 or self.level.get_cell(self.pos).get_type() == 'Fire')):
            self.to_move = 1

