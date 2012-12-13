from movable import Movable


class Mirror(Movable):
    def __init__(self, level, pos, facing):
        Movable.__init__(self, level, pos, facing)
        
        self.tile = 7, 1
        
        # facing = diagonal dir the mirror is facing: 0-3, clockwise from northeast
        # out_dirs = the two cardinal dirs the mirror is facing
        self.out_dirs = facing, (facing + 1) % 4
        
        
    def get_out_dir(self, in_dir):
        # we want to know if the mirror is facing the opposite of in_dir
        # so let's reverse in_dir and see if it's one of the mirror's two dirs
        from_dir = (in_dir + 2) % 4
        return (self.out_dirs[(self.out_dirs.index(from_dir) + 1) % 2]
                if from_dir in self.out_dirs else None)
