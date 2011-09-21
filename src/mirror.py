import sprite

class Mirror(sprite.Sprite):

    def __init__(self, map, pos, facing):
        sprite.Sprite.__init__(self, map, pos)
        self.colour = (128, 128, 255)
        self.is_movable = 1
        self.is_solid = 1
        
        # facing = diagonal dir the mirror is facing: 0-3, clockwise from northwest
        # self.dirs = the two cardinal dirs the mirror is facing
        self.dirs = [facing, (facing - 1) % 4]
        
        
    def get_out_dir(self, in_dir):
        # we want to know if the mirror is facing the opposite of in_dir
        # so let's reverse in_dir and see if it's one of the mirror's two dirs
        in_dir = (in_dir + 2) % 4
        return self.dirs[(self.dirs.index(in_dir) + 1) % 2] if in_dir in self.dirs else False
    
    
    def after_move(self):
        if self.map.is_fire(self.pos):
            self.to_move = 1

        elif self.map.is_water(self.pos) and not self.map.get_objects_in(self.pos, 0, 'SunkenCrate'):
            self.kill()
        
