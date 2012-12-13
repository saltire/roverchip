import sprite


class Boots(sprite.Sprite):
    def __init__(self, level, pos, colour):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 8, colour + 2
        self.layer = 2
        self.size = 0.75
        self.is_item = True
        
        self.colour = colour
