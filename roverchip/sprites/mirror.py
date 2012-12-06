import sprite


class Mirror(sprite.Sprite):
    def __init__(self, level, pos, facing):
        sprite.Sprite.__init__(self, level, pos, facing)
        
        self.tile = 7, 1
        self.is_movable = True
        self.is_solid = True
        
        # facing = diagonal dir the mirror is facing: 0-3, clockwise from northeast
        # self.dirs = the two cardinal dirs the mirror is facing
        self.dirs = (facing, (facing + 1) % 4)
        
        
    def get_out_dir(self, in_dir):
        # we want to know if the mirror is facing the opposite of in_dir
        # so let's reverse in_dir and see if it's one of the mirror's two dirs
        in_dir = (in_dir + 2) % 4
        return self.dirs[(self.dirs.index(in_dir) + 1) % 2] if in_dir in self.dirs else None
    
    
    def after_move(self):
        if self.level.get_cell(self.pos).get_type() == 'Fire':
            self.to_move = 1

        elif (self.level.get_cell(self.pos).get_type() == 'Water'
              and not self.level.get_sprites_in(self.pos, False, 'SunkenCrate')):
            self.kill()
        
