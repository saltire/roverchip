import sprite


class Key(sprite.Sprite):
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        self.colour = (0, 255, 0)
        self.layer = 2
        self.size = 0.5
        
        self.is_item = 1
