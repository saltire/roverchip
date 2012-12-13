from sprite import Sprite


class Rover(Sprite):
    def __init__(self, level, pos, facing=0):
        Sprite.__init__(self, level, pos, facing)
        
        level.destructibles.add(self)
        level.solids.add(self)
        
        self.tile = 1, 2
        self.facing = 2
        self.layer = 1
        self.rotate = True
