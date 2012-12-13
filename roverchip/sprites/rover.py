from sprite import Sprite


class Rover(Sprite):
    def __init__(self, level, pos, facing=0):
        Sprite.__init__(self, level, pos, facing)
        
        self.tile = 1, 2
        self.facing = 2
        self.layer = 1
        self.rotate = True
        self.is_solid = True
        self.is_destructible = True

