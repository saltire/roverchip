import sprite


class Dirt(sprite.Sprite):   
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 8, 1
        self.layer = 1
        self.is_movable = True
        self.is_solid = True
        
        
    def start_turn(self):
        # if it's entirely on a water cell, replace with a sunken crate
        if (len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
            self.level.set_cell(self.pos, 'Mud')

    
    def after_move(self):
        # trigger object enter hook
        self.level.get_cell(self.pos).object_inside()

        # continue moving over fire
        if self.level.get_cell(self.pos).get_type() == 'Fire':
            self.to_move = 1
