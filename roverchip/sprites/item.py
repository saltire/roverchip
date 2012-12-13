from sprite import Sprite


class Item(Sprite):
    def __init__(self, level, pos):
        Sprite.__init__(self, level, pos)
        
        level.items.add(self)
        
        self.layer = 2
