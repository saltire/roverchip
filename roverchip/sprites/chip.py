from sprite import Sprite


class Chip(Sprite):
    def __init__(self, level, pos):
        Sprite.__init__(self, level, pos)
        
        self.tile = 7, 2
        