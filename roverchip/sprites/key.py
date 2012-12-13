from item import Item


class Key(Item):
    def __init__(self, level, pos, colour):
        Item.__init__(self, level, pos)
        
        self.tile = 6, colour + 2
        self.size = 0.5
        
        self.colour = colour
