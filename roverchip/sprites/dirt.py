from movable import Movable


class Dirt(Movable):   
    def __init__(self, level, pos):
        Movable.__init__(self, level, pos)
        
        self.tile = 8, 1


    def start_turn(self):
        # if it's entirely on a water cell, remove and turn that cell to mud
        if (len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
            self.level.set_cell(self.pos, 'Mud')
