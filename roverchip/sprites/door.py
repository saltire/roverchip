from sprite import Sprite


class Door(Sprite):
    def __init__(self, level, pos, facing, colour):
        Sprite.__init__(self, level, pos, facing)
        
        self.tile = 5, colour + 2
        self.rotate = True
        self.is_solid = True
        
        self.colour = colour
        