import sprite


class Key(sprite.Sprite):
    def __init__(self, level, pos, colour):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 6, colour + 2
        self.layer = 2
        self.is_item = True
        
        self.colour = colour
