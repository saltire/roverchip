import sprite


class Chip(sprite.Sprite):
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 7, 2
        self.layer = 2
        self.is_item = True
        