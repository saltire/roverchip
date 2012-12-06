import sprite


class Key(sprite.Sprite):
    def __init__(self, level, pos):
        sprite.Sprite.__init__(self, level, pos)
        
        self.tile = 6, 2
        self.layer = 2
        self.is_item = True
