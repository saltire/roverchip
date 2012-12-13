from sprite import Sprite


class Item(Sprite):
    def __init__(self, level, pos):
        Sprite.__init__(self, level, pos)
        
        self.layer = 2
        self.is_item = True
