import sprite


class Mirror(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 7, 1
        self.is_movable = True
        self.is_solid = True
        
        # facing = diagonal dir the mirror is facing: 0-3, clockwise from northeast
        # out_dirs = the two cardinal dirs the mirror is facing
        self.out_dirs = facing, (facing + 1) % 4
        
        
    def start_turn(self):
        # if it's entirely on a water cell, destroy it
        if (len(self.cells_in()) == 1
            and self.level.get_cell(self.pos).get_type() == 'Water'
            and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')
            ):
            self.kill()
        
    
    def get_out_dir(self, in_dir):
        # we want to know if the mirror is facing the opposite of in_dir
        # so let's reverse in_dir and see if it's one of the mirror's two dirs
        from_dir = (in_dir + 2) % 4
        return (self.out_dirs[(self.out_dirs.index(from_dir) + 1) % 2]
                if from_dir in self.out_dirs else None)
    
    
    def after_move(self):
        # trigger object enter hook
        self.level.get_cell(self.pos).object_inside()

        # continue moving over fire
        nextcell = self.level.get_neighbour(self.pos, self.move_dir)
        if (self.level.object_can_enter(nextcell)
            and self.level.get_cell(self.pos).get_type() == 'Fire'):
            self.to_move = 1
